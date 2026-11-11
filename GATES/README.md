# GATES — the four locks every unsupervised agent needs

An agent you watch is a tool. An agent you don't watch is a system, and a system
needs stops. These are the four, in the order you should build them.

None of them asks you a question. That is the whole point — a gate that needs
your attention is not a gate, it is a notification.

Gate one costs nothing and takes a minute. Build it before you leave the room.

---

## Gate 01 · Kill switch

**One file on disk. Every loop reads it first.**

```bash
# at the very top of every agent loop, before anything else runs
[ -f ~/.agents.disabled ] && exit 0
```

Stop the whole fleet from anywhere — another terminal, your phone over SSH, a
shortcut:

```bash
touch ~/.agents.disabled     # everything stops at its next check
rm ~/.agents.disabled        # everything resumes
```

Why a file and not a flag, an env var, or an API call: a file works when the
network is down, when the process is wedged, and when you are not at the
machine. It is the one stop that has no dependencies.

Put the check **first**, above the argument parsing and the logging setup. A
kill switch you reach after the expensive part is a receipt, not a switch.

---

## Gate 02 · Deny floor

**Some paths are never readable. Not "ask first" — never.**

Credentials should not be one prompt-injection away from an agent's context. In
Claude Code this lives in `settings.json` (see [`settings.deny.json`](settings.deny.json)
for a paste-able block):

```json
{
  "permissions": {
    "deny": [
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Read(**/secrets/**)",
      "Read(**/*credential*)",
      "Read(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Read(~/.config/gh/**)"
    ]
  }
}
```

Two rules that make the difference between a deny list and decoration:

- **Deny beats allow.** If your tool resolves an allow rule over a deny rule,
  you don't have a floor, you have a preference.
- **Write the rule for the file, not the folder.** `.env` files travel. Match
  them with `**/` wherever they land, not just at the repo root.

If your agent genuinely needs a secret, hand it the value through the
environment at launch. It never needs to *read the file*.

---

## Gate 03 · Daily cap

**A ceiling on the day. The bad night ends itself.**

The failure this catches is not the expensive task. It is the loop that retries,
each retry a little longer than the last, at 3am, while you sleep.

```bash
# a plain-text ledger, one number in it, reset by the date in the filename
SPEND_FILE=~/.agents.spend.$(date +%F)
CAP=10.00

spent=$(cat "$SPEND_FILE" 2>/dev/null || echo 0)
if awk -v s="$spent" -v c="$CAP" 'BEGIN{exit !(s>=c)}'; then
    echo "day cap reached: \$$spent — stopping"
    exit 0
fi

# ... run the agent, then add what it cost ...
awk -v s="$spent" -v r="$run_cost" 'BEGIN{printf "%.2f\n", s+r}' > "$SPEND_FILE"
```

`awk` rather than `bc`, because `bc` is not installed everywhere and a cap that
silently fails open is worse than no cap.

Set the cap at a number that would annoy you, not at a number that would ruin
you. A cap you never hit teaches you nothing; a cap you hit twice a month is
telling you something true about your workload.

The date in the filename is the reset. No cron job, no cleanup.

---

## Gate 04 · Parallel cap

**Two at once, not twenty.**

Concurrency is where a small mistake becomes a large one — same bug, running
nine times, against the same files.

```bash
MAX=2
running=$(pgrep -f 'my-agent-runner' 2>/dev/null | wc -l | tr -d ' ')
[ "$running" -ge "$MAX" ] && { echo "queue: $running already running"; exit 0; }
```

Count the lines rather than using `pgrep -c`: the `-c` flag is Linux-only, and
on macOS it fails with a usage error that a `|| echo 0` fallback turns into
`running=0`. That gate looks fine in the script and never fires. Test yours by
starting three dummy processes and watching it actually stop.

Queue rather than kill. A run that exits quietly and gets picked up on the next
tick is a delay; a run that dies halfway through a file edit is a mess.

If your agents write to a shared tree, this gate is also what stops two of them
editing the same file with two different ideas of what it should say.

---

## The order matters

Build them in this order, and stop whenever you run out of appetite:

| | Gate | Protects against | Time to build |
|---|---|---|---|
| 01 | Kill switch | Everything. It is the undo. | a minute |
| 02 | Deny floor | A leaked key, permanently | ten minutes |
| 03 | Daily cap | The 3am retry loop | an afternoon |
| 04 | Parallel cap | One bug, nine times | an afternoon |

One and two are worth having even if you never build three and four. Four
without one is a fleet you can't stop.

---

## What this is not

Not a sandbox, not a permission model, not a security boundary against a
determined attacker. It is the set of stops that turn "I left an agent running"
from a gamble into a decision you can reverse.

If the agent runs code you did not write, on a machine that matters, you want a
container as well. These four are the floor, not the ceiling.

---

MIT. Take it, change it, ship it.
