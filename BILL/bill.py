#!/usr/bin/env python3
"""
Where does the money in your AI coding bill actually go?

Reads the transcripts Claude Code already writes to disk and splits your usage
into four buckets: what you typed, what it wrote back, and the two costs nobody
looks at — re-reading the chat and saving the chat.

    python3 bill.py

No dependencies. Nothing is uploaded. Nothing is written. It only reads.

If you are on a subscription, you are not billed per token — this shows what the
same work would have cost on the API. The *shape* is the same either way, and
the shape is the point.
"""

import glob
import json
import os
import sys

# Published list prices, US dollars per million tokens, checked 2026-08-17.
#   input | output | cache read | cache write (5-minute)
# Cache read is ~0.1x input. Cache write is 1.25x input on the 5-minute cache
# and 2x on the 1-hour cache — this script assumes the 5-minute one, so if you
# run long sessions the real re-reading cost is *higher* than what you see here.
# Prices move. Current list: https://platform.claude.com/docs/en/pricing
RATES = {
    "opus":   (5.00, 25.00, 0.50, 6.25),
    "sonnet": (3.00, 15.00, 0.30, 3.75),
    "haiku":  (1.00,  5.00, 0.10, 1.25),
}
DEFAULT = "opus"

TRANSCRIPTS = "~/.claude/projects/**/*.jsonl"

BUCKETS = [
    # label                    usage field                       rate index
    ("what you typed",         "input_tokens",                   0),
    ("the answers it wrote",   "output_tokens",                  1),
    ("re-reading the chat",    "cache_read_input_tokens",        2),
    ("saving the chat",        "cache_creation_input_tokens",    3),
]


def family(model):
    """Map a model id onto a price tier."""
    model = (model or "").lower()
    for name in RATES:
        if name in model:
            return name
    return DEFAULT


def main():
    paths = glob.glob(os.path.expanduser(TRANSCRIPTS), recursive=True)
    if not paths:
        sys.exit(
            "No transcripts found at %s\n"
            "This script reads what Claude Code writes locally. If you use a\n"
            "different tool, point TRANSCRIPTS at its logs." % TRANSCRIPTS
        )

    cost = {label: 0.0 for label, _, _ in BUCKETS}
    tokens = {label: 0 for label, _, _ in BUCKETS}
    turns = 0

    for path in paths:
        try:
            handle = open(path, errors="ignore")
        except OSError:
            continue
        with handle:
            for line in handle:
                if '"usage"' not in line:
                    continue
                try:
                    record = json.loads(line)
                except ValueError:
                    continue
                message = record.get("message") or {}
                usage = message.get("usage")
                if not usage:
                    continue
                turns += 1
                rates = RATES[family(message.get("model"))]
                for label, field, index in BUCKETS:
                    count = usage.get(field) or 0
                    tokens[label] += count
                    cost[label] += count / 1_000_000 * rates[index]

    if not turns:
        sys.exit("Found transcript files but no usage records in them.")

    total_cost = sum(cost.values())
    total_tokens = sum(tokens.values())
    order = sorted(cost, key=cost.get, reverse=True)

    print()
    print("  %-22s %8s %9s %14s" % ("", "of cost", "of words", "tokens"))
    print("  " + "-" * 56)
    for label in order:
        print("  %-22s %7.1f%% %8.1f%% %14s" % (
            label,
            100 * cost[label] / total_cost,
            100 * tokens[label] / total_tokens,
            "{:,}".format(tokens[label]),
        ))
    print("  " + "-" * 56)
    print("  %-22s %8s %9s %14s" % (
        "total", "$%.2f" % total_cost, "", "{:,}".format(total_tokens)))
    print()

    chat = cost["re-reading the chat"] + cost["saving the chat"]
    print("  %d turns across %d transcript files." % (turns, len(paths)))
    print("  Answering you cost %.0f%% of the money." % (
        100 * cost["the answers it wrote"] / total_cost))
    print("  Carrying the chat around cost %.0f%%." % (100 * chat / total_cost))
    print()


if __name__ == "__main__":
    main()
