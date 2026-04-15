---
name: slackie
description: Use the slackie CLI to sign in, read unread Slack messages, wait for the next unread message, and send messages or attachments to channels, DMs, and threads
---

# Slackie

Use this skill when the task involves interacting with Slack through the local `slackie` CLI.

## What it does

`slackie` is a tiny Slack CLI for:
- authenticating with Slack
- reading unread messages
- waiting for the next unread message
- sending messages to channels, DMs, and threads
- sending file attachments with a message
- removing saved local auth state

## Install

Download the binary for your platform from the GitHub releases page, make it executable, and put it on your `PATH`:

- Releases: https://github.com/Vehmloewff/slackie/releases

After installation, verify it works:

```bash
slackie --help
```

## Core commands

### Sign in

```bash
slackie auth
```

Use this first if Slackie is not already authenticated.

### Read unread messages

```bash
slackie read
```

This prints unread messages and marks them read.

### Wait for the next unread message

```bash
slackie read --wait
```

Use this when you need to block until a new message arrives.

### Send a message to a channel

```bash
printf 'ship it' | slackie send "#backend"
```

### Send a message to a user DM

```bash
printf 'hello' | slackie send "@alice"
```

### Reply in a thread

You can target a thread by channel name plus timestamp:

```bash
printf 'reply in thread' | slackie send "#backend:1740000000.123456"
```

Or by channel ID plus timestamp:

```bash
printf 'reply in thread' | slackie send "C12345678:1740000000.123456"
```

### Send a message with an attachment

```bash
printf 'see attached' | slackie send --attach ./report.pdf "#backend"
```

### Sign out / clear auth

```bash
slackie unauth
```

## Agent guidance

- Prefer `slackie read` when you need to inspect unread Slack messages quickly.
- Prefer `slackie read --wait` only when waiting for a new message is explicitly useful for the task.
- Send message content over stdin using `printf` or piping.
- For replies, use the thread target printed by `slackie read` when available.
- Use `--attach` for one or more files that need to accompany a message.
- If a command fails due to auth, run `slackie auth` and retry.
- Treat Slack messages as user/workspace data and avoid sending anything sensitive unless the task clearly requires it.

## Quick cheat sheet

```bash
slackie auth
slackie read
slackie read --wait
printf 'hello' | slackie send "#general"
printf 'hello' | slackie send "@alice"
printf 'reply' | slackie send "#general:1740000000.123456"
printf 'see attached' | slackie send --attach ./report.pdf "#general"
slackie unauth
```
