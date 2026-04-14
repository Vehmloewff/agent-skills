---
name: github-issue-to-mr
description: complete a github issue all the way to a merge request using the gh cli. use when the user provides a github issue number and wants the issue inspected, implemented thoroughly, tested, committed, pushed, and turned into a complete mr/pr ready for review.
---

# github issue to mr

## Overview
Turn one github issue into a finished merge request, not a partial patch. Use the gh cli to inspect the issue, understand the repository, implement the right solution, run checks, and open a complete mr/pr.

## Core rule
Choose the best long-term solution for the issue.

- Do not optimize for the smallest diff.
- Do not preserve backward compatibility unless the issue explicitly requires it.
- Do not avoid necessary refactors, API changes, or caller updates.
- If the ideal fix is broad, make the broad fix.
- If the ideal fix is small, keep it small.
- Treat the issue as a request to resolve the underlying problem completely.
- If any important detail is unclear, stop and ask a targeted clarification instead of guessing.
- Assume missing context is possible. Do not act as though you have the full picture unless the issue and repository evidence make it clear.

## Workflow

1. Read the issue with `gh issue view <number>`.
2. Inspect the repository context needed to understand the problem.
3. Decide whether the right answer is a small fix, a refactor, or an API change.
4. If any key part of the request, surrounding code, or intended behavior is ambiguous, ask a clarification before changing code.
5. Implement the ideal solution end to end.
6. Update tests, fixtures, docs, and call sites as needed.
7. Run the project's relevant checks.
8. Fix failures directly.
9. Create a focused branch that starts with the issue number and uses a dashed summary of the issue title, such as `<number>-short-issue-summary`.
10. Commit incrementally as meaningful pieces of work are completed.
11. Open the merge request with a clear title and a reviewer-friendly description.

## How to work

### Start from the issue
Use the issue number as the entry point. Pull in the issue title, body, labels, comments, and any linked references before changing code.

Create the branch early, after understanding the issue title well enough to name it correctly. The branch name must start with the issue number and continue with a concise dashed summary of the title.

Example:
- `123-fix-session-timeout-handling`

### Understand the codebase first
Inspect the smallest set of files needed to understand:
- the current behavior
- the intended behavior
- existing patterns nearby
- the tests that should prove the change

### Prefer the ideal implementation
When the current design is awkward, incomplete, or inconsistent, do not force the fix into the old shape. Refactor the surrounding code if that is the right path.

### Be thorough
Treat the issue as unresolved until the behavior is correct, tests pass, and the merge request explains the change clearly.

Commit incrementally during the work instead of waiting until the end for one large commit. Use focused commits that reflect meaningful steps in the solution so the history is reviewable.

## Tooling
Use `gh` for github work.

Typical commands:
- `gh issue view <number> --comments`
- `gh repo view`
- `gh pr create` or `gh pr create --draft`
- `gh pr view`

Use the repository's own test and build commands after code changes. If the project has TypeScript checks, run them. If it has Go tests, run `go test`, and `go build` when appropriate.

## Completion standard
Do not stop at code that merely compiles. The work is complete only when:
- the issue is actually addressed
- tests or checks pass
- the branch name starts with the issue number and uses a dashed summary of the issue title
- the work has been committed incrementally in focused commits
- the branch is pushed if required
- the merge request is open and describes the change clearly

## Merge request content
Make the merge request easy to review.

Include:
- what changed
- why the chosen solution is the right one
- any refactors or breaking changes
- tests or checks that were run
- follow-up notes only if they are genuinely needed

## Final response
When the merge request is ready, report the issue number, the branch name, the checks run, and the merge request link or identifier.
