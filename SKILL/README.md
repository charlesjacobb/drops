# SKILL: the one-page template I start every skill with

The rule: **if you have typed the same explanation twice, it is not a prompt
anymore. It is a routine you are running by hand.**

Once is fine, not everything deserves a file. Twice is the sign. Write it down
once, give it a name, and never type it again.

The whole thing is one file. [`SKILL.md`](SKILL.md) is the template. Copy it,
fill it in, done.

---

## Where it goes

```
~/.claude/skills/
└── your-skill-name/
    └── SKILL.md
```

One folder, one file. The folder name and the `name:` in the file should match.
Per-project instead of global: `.claude/skills/` inside the project.

---

## The two lines that matter

Everything below the frontmatter is instructions to a competent colleague. The
frontmatter is the part that decides whether they ever get read.

```yaml
---
name: session-close
description: Close the day: update the notes, write the log. Use when the
  user says they are done, wraps up, or heads off.
---
```

**`name`** is the handle. Lowercase, hyphenated.

**`description` is not a label. It is the trigger.** This is the part people get
wrong. The description is what gets matched against what the user actually said,
so it has two jobs in one sentence:

1. What the skill does.
2. **When to use it**, in the words a real person would type.

"Closes the session" describes it and triggers on nothing. "Use when the user
says they are done, wraps up, or heads off" triggers on the way people
actually talk. Write the second kind.

---

## Then you stop calling it

You never type the skill's name. That's the payoff.

```
you say      "I'm done for today"
it matches   the description fits
it opens     the steps enter the chat
it runs      notes updated, log written
```

A prompt dies with the chat. A skill doesn't.

---

## What makes a good one

**Write the steps, not the theory.** Plain words, in order. If a step needs a
reason, give the reason in half a line. The reason is usually the thing that
stops someone skipping the step next month.

**Write the "done when".** If you can't state what finished looks like in a way
someone else could check, the routine isn't ready to be a file yet.

**Keep it to a page.** A skill that needs ten pages is either two skills or a
document that a skill should point at.

**Say what not to do, sparingly.** Only where doing the wrong thing is
genuinely tempting. A list of prohibitions nobody was going to violate is
noise, and noise is what gets skipped.

**Let it change.** The best ones get edited the week after you write them,
usually because something went wrong in a way you can now name. That edit is
the actual value. The file is just where it lives.

---

## What not to make a skill

- Something you have done exactly once. Wait for the second time.
- Something the project's README or config already says. Point at it instead.
- A wrapper around a single command you can type from memory.

The test is not "could this be a skill." It is "have I now explained this
twice."

---

MIT. Take it, change it, ship it.
