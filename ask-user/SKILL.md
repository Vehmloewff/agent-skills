---
name: ask-user
description: Ask the user quick task-related questions with a native macOS dialog and capture their response on stdout
---

# Ask User

Use this skill when you need to ask the local user a quick question related to the current task with a **native macOS dialog** and capture a multiline response.

## How to use it

Run the helper script from this skill directory:

```bash
./run-ask-user.sh "I need the password in order to log in, what is it?"
```

Or pipe the prompt in via stdin:

```bash
printf 'I need the deployment URL to continue this task. What is it?' | ./run-ask-user.sh
```

## Guidance for agents

- Use this when you need a quick answer from the user to continue the current task.
- Ask direct, specific questions that help you unblock yourself.
- Prefer passing the prompt as a shell argument when practical.
- Use stdin for long prompts or prompts with difficult quoting.
- Read stdout as the user's response.
- Check the exit code to detect cancellation.
- The script sets up its virtual environment automatically if needed.
