---
name: subagents
description: Spawn a fresh pi subagent in non-interactive print mode for any self-contained subtask that can be delegated with a prompt. Use this much more often than you think; research, investigation, implementation on isolated files, drafting, summarization, validation, option generation, and other bounded tasks are usually good candidates.
---

# Subagents

Use this skill to delegate work to a fresh pi agent running in non-interactive mode.

The mechanism is intentionally simple. The value of this skill is not the shell command itself; it is recognizing that **delegation should be a default move** for many tasks.

## Core rule

If a task is **self-contained** and you can describe it clearly in a prompt, you should strongly consider spawning a subagent.

Use subagents **more than your first instinct suggests**. Agents often wait too long and keep too much work in a single thread. That is a mistake. If a subtask might hide additional complexity, uncertainty, or exploration, delegate it.

Good default: when you notice a subtask that could reasonably be handed to "another competent agent with a prompt," spawn a subagent.

## What a subagent is good for

A subagent is ideal when you want a fresh context to handle one bounded piece of work, then return a result.

Common high-value uses:
- investigating a bug and summarizing the root cause
- reading a part of the codebase and reporting findings
- drafting a plan before implementation
- implementing a change in a small, isolated area
- generating options, tradeoffs, or alternative designs
- validating an approach against docs or local files
- reviewing a diff or a file for problems
- summarizing logs, test failures, or command output
- extracting requirements from a long document
- doing a first pass on migrations or refactors

## Use subagents aggressively

You should usually spawn a subagent when the task is any of the following:
- **bounded**: has a clear goal and finish line
- **inspectable**: mostly reading, reasoning, or changing a contained set of files
- **parallelizable in principle**: could be done independently from the rest of the task
- **potentially deeper than it looks**: might reveal hidden complexity once explored
- **easy to specify**: you can write a crisp prompt with success criteria

This includes many tasks that seem "small." A task does **not** need to be huge to justify delegation.

Examples of tasks agents should delegate more often:
- "Read these three files and explain how auth works"
- "Inspect the failing test and identify the most likely cause"
- "Draft a minimal implementation plan for this feature"
- "Add the helper function in this isolated module"
- "Compare two approaches and recommend one"
- "Summarize the API surface of this package"

## When not to use a subagent

Avoid spawning a subagent only when:
- the task is truly trivial and faster to do directly
- the work depends on extremely tight back-and-forth with the current chain of thought
- multiple subagents would likely edit the same files and conflict
- the task cannot be described well enough yet to delegate safely

Even then, revisit the decision. Many tasks that feel tightly coupled can still be split into: investigate first, then continue.

## How to invoke a subagent

Run the helper script from this skill directory by passing the prompt on stdin:

```bash
cat <<'EOF' | ./spawn-subagent.sh
Inspect src/auth.ts and src/session.ts, explain the login flow, and note any risky assumptions. Do not change files.
EOF
```

Another example:

```bash
cat <<'EOF' | ./spawn-subagent.sh
Read the local code related to billing retries. Summarize how retries are scheduled, where backoff is defined, and any obvious bugs or edge cases. Do not modify files.
EOF
```

The helper runs `pi` in print mode with no session carryover, so the subagent gets a fresh, focused context.

The script reads stdin into a shell variable, prefixes it with the delegation instruction, and passes the combined result as a **single argv value** to `pi`. That means quotes inside the delegated prompt are handled safely and are not re-parsed by the shell.

## Important: use a very long command timeout

The script itself does **not** enforce a timeout.

When invoking it through the agent's command-execution tool, you should give that command a **very long timeout**. Subagents are often used for tasks that look simple but expand into deeper investigation or implementation.

Do not use a short timeout out of habit. Prefer something generous whenever you spawn a subagent.

Examples:
- investigation or summarization: 15–30 minutes
- implementation or refactoring in an isolated area: 30–60 minutes
- deeper research or multi-step validation: 60+ minutes

The key point is simple: **if you spawn a subagent, also remember to give the command that launches it a long timeout.**

## Prompting guidance

Write subagent prompts like mini task briefs.

Include:
- the exact goal
- relevant files, directories, or commands
- whether code changes are allowed
- expected output format
- constraints, such as "do not edit files" or "touch only these files"

A good prompt is specific enough to bound the task, but not overloaded with irrelevant context.

## Recommended prompt template

Use a structure like this:

```text
Goal: <what the subagent should accomplish>
Context: <relevant files, directories, or facts>
Constraints: <what it may or may not change>
Output: <what you want back>
```

Example:

```text
Goal: Find why the dashboard totals render as zero on first load.
Context: Inspect src/dashboard/* and any related data-loading hooks.
Constraints: Do not edit files.
Output: Give the root cause, the specific file(s) involved, and the smallest likely fix.
```

## Examples

### 1. Investigation only

```bash
cat <<'EOF' | ./spawn-subagent.sh
Read the test failure output in /tmp/test.log and the files under src/cache. Explain the likely root cause and propose a minimal fix. Do not edit files.
EOF
```

Use this when you need understanding before acting.

### 2. Isolated implementation

```bash
cat <<'EOF' | ./spawn-subagent.sh
Add a small helper in src/lib/formatDuration.ts that formats milliseconds as mm:ss, update only the directly related tests, and summarize the changes.
EOF
```

Use this when the change is local and unlikely to conflict with other work.

### 3. Planning before coding

```bash
cat <<'EOF' | ./spawn-subagent.sh
Inspect the existing notification system and produce a concise implementation plan for adding browser push notifications. Do not edit files.
EOF
```

Use this when a short planning pass will reduce mistakes.

### 4. Option generation

```bash
cat <<'EOF' | ./spawn-subagent.sh
Compare two ways to implement CSV export in this codebase: client-side generation vs server-side streaming. Use the local codebase as context and recommend one approach with tradeoffs. Do not edit files.
EOF
```

Use this when you want a fresh recommendation instead of carrying all analysis yourself.

### 5. Focused documentation pass

```bash
cat <<'EOF' | ./spawn-subagent.sh
Read package.json and the files under scripts/. Summarize the developer workflows available in this repo, including test, lint, build, and release commands. Do not edit files.
EOF
```

Use this when you need a quick map of part of the project.

## Practical delegation patterns

### Pattern: investigate, then act

1. Spawn a subagent to inspect and summarize.
2. Read the result.
3. Continue with implementation yourself, or spawn another subagent for the isolated fix.

This is often better than trying to reason and implement in one uninterrupted thread.

### Pattern: plan, then implement

1. Spawn a subagent for a short implementation plan.
2. If the plan looks good, either execute it yourself or delegate the isolated parts.

### Pattern: divide independent work

If a task naturally splits into independent parts, delegate them separately.

Examples:
- one subagent maps the relevant code
- one subagent checks tests and failures
- one subagent drafts the implementation approach

Do this only when their work products will not conflict.

## Important cautions

- Prefer **read-only** delegation first when the situation is unclear.
- If letting a subagent edit files, keep the scope narrow and explicit.
- Avoid simultaneous subagents editing the same files.
- Ask for concise, structured output so you can quickly integrate the result.
- Treat subagents as force multipliers, not rare special-case tools.
- When running `./spawn-subagent.sh` through a command tool, remember to set a very long command timeout.

## Final guidance

When you are unsure whether to spawn a subagent, the answer is usually **yes**.

If a subtask is self-contained, potentially deeper than it appears, or simply easier to specify than to hold in working memory, delegate it.

Use this skill early and often.
