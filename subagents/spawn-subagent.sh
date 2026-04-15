#!/usr/bin/env bash

set -euo pipefail

PROMPT="$(cat)"

if [[ -z "${PROMPT//[[:space:]]/}" ]]; then
  echo "Usage: printf 'your prompt' | ./spawn-subagent.sh" >&2
  echo "   or: cat prompt.txt | ./spawn-subagent.sh" >&2
  exit 2
fi

PREFIX="Execute the delegated task below. Follow it exactly.\n\n"
printf -v FULL_PROMPT '%s%s' "$PREFIX" "$PROMPT"

pi --print --no-session "$FULL_PROMPT"
