#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${HOME}/.agents/skills"

mkdir -p "$TARGET_DIR"

for dir in "$SCRIPT_DIR"/*/; do
  # Skip .git and other hidden directories
  [[ "$(basename "$dir")" == .* ]] && continue
  dir="${dir%/}"
  name="$(basename "$dir")"
  dest="$TARGET_DIR/$name"
  echo "Linking $name -> $dest"
  rm -rf "$dest"
  ln -s "$dir" "$dest"
done

echo "Done. Skills mounted to $TARGET_DIR"
