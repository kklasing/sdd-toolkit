---
name: sdd-grill-with-docs
description: Grill the user relentlessly about a plan, decision, or idea while capturing docs (ADRs and glossary) as you go. Use when the user wants to stress-test their thinking, uses any 'grill' trigger phrases, or when a spec/plan needs interrogating before it is written.
---

Interview the user relentlessly until you reach a shared understanding, and capture the durable outcomes as docs while you go. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Each question should be formatted like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it — don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report — ask the rest of the frontier now. The _decisions_ are the user's — put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Capture docs as you go

Use the `sdd-domain-modeling` skill throughout, not just at the end:

- When the grilling sharpens a fuzzy term or settles a naming conflict, record it in the project glossary (`CONTEXT.md`).
- When a round produces a decision that is hard to reverse, surprising, and a real trade-off, offer to write an ADR under `docs/adr/` — don't manufacture ADRs for routine choices.

Keep the docs a by-product of the interview, written lazily and only when there is something worth writing.
