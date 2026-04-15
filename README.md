# Agent Skills

A series of skills that I want my agents to have. You can use this too!

Current skills:
- `ask-user` — native macOS multiline prompt dialog backed by PyObjC
- `flutter` — Flutter MCP and `flutter_driver` guidance for launching, inspecting, and driving apps
- `github-issue-to-mr` — inspect a GitHub issue with `gh`, implement the full fix, run checks, commit, push, and open a review-ready PR/MR
- `receiving-code-review` — verify review feedback before implementing, clarify unclear items, and push back technically when suggestions are wrong for the codebase
- `rodney-browser-automation` — browser automation guidance for Rodney CLI
- `subagents` — delegate self-contained subtasks to fresh pi subagents in non-interactive mode

To configure your agent to use these skills, clone this repository somewhere to your machine, then run `sh mount.sh`. This will symlink each skill to `~/.agents/skills`.
