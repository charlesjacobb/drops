# BILL — where the money in your AI coding bill actually goes

One command. It reads the transcripts your coding agent already writes to your
own disk and tells you which part of the bill is doing the work.

```bash
python3 bill.py
```

No dependencies, no install, no account. It only reads. Nothing leaves your machine.

---

## What you get

```
                          of cost  of words         tokens
  --------------------------------------------------------
  re-reading the chat       ...%      ...%        ...
  saving the chat           ...%      ...%        ...
  the answers it wrote      ...%      ...%        ...
  what you typed            ...%      ...%        ...
```

Four buckets, two ways of looking at them.

**Of words** is how much text moved. **Of cost** is what you paid for it. They
are not the same, and the gap is the whole story: the answers are a rounding
error by volume, and the chat you dragged along behind them is not.

---

## How to read it

**"The answers it wrote"** is the part you asked for. On most setups it is a
small slice of the money and almost none of the words.

**"Re-reading the chat"** is the model having no memory. Every message, it reads
the entire conversation again from the top. You pay for that re-read every
single time. It is cheap per token and enormous in aggregate, because it grows
with the length of the chat and you send it on every turn.

**"Saving the chat"** is the flip side — writing that conversation into the
cache so the next re-read is cheap. It is billed at a premium over plain input.
Short-lived caches expire and get re-written; a chat you return to after a
break pays this twice.

**"What you typed"** is your actual prompts. It is usually the smallest line on
the page, which is the uncomfortable part: the thing you spend your time on is
not the thing you spend your money on.

---

## What to do about it

In rough order of how much they pay off.

**1. Start a new chat at the topic change, not at the end of the day.**
The cost of a message is set by how long the chat already is. A fresh chat is
the single biggest lever, and it costs you nothing but the habit.

**2. Don't leave the huge-context mode on by default.**
Most tools have a setting for a much larger context window. Switch it on for the
job that needs it, not for every job. Left on, chats grow because nothing stops
them, and long chats are where the money is.

**3. Do one thing per chat.**
Two unrelated problems in one chat means every message about the second one is
also paying to re-read the first one.

**4. Re-measure after a week.**
Run this again. If the shape didn't move, the habit didn't stick — that is
useful to know, and it is the reason this is a script and not a blog post.

---

## Honest caveats

- **Prices move.** The rate table at the top of `bill.py` was checked on
  2026-08-17 against the published list price. Check it before quoting a number
  from this: <https://platform.claude.com/docs/en/pricing>
- **Subscription users are not billed per token.** If you are on a plan, this
  shows what the same work would have cost on the API. The shape is the same;
  the dollar total is hypothetical.
- **The cache-write number is the optimistic one.** The script assumes the
  short-lived cache. If your sessions run long enough to use the longer-lived
  one, that line is billed higher than shown — so the real cost of carrying the
  chat is *worse* than this prints, never better.
- **It reads Claude Code's transcript location.** Another tool, another path —
  change `TRANSCRIPTS` at the top of the file.

---

MIT. Take it, change it, ship it.
