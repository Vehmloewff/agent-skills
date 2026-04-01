"""Show a native macOS prompt and print the user's response."""

from __future__ import annotations

import argparse
import sys

from AppKit import (
    NSAlert,
    NSAlertFirstButtonReturn,
    NSApplication,
    NSApplicationActivationPolicyAccessory,
    NSMakeRect,
    NSMakeSize,
    NSRunningApplication,
    NSScrollView,
    NSTextView,
)

TITLE = "Ask User"
SUBMIT_BUTTON = "Submit"
CANCEL_BUTTON = "Cancel"
TEXTAREA_WIDTH = 520
TEXTAREA_HEIGHT = 220


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Show a macOS system dialog for the supplied prompt and print the "
            "entered response to stdout."
        )
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Prompt text to show. If omitted, stdin is used.",
    )
    return parser.parse_args()


def resolve_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        prompt = " ".join(args.prompt).strip()
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    else:
        raise SystemExit("error: provide a prompt as arguments or via stdin")

    if not prompt:
        raise SystemExit("error: prompt must not be empty")

    return prompt


def ask(prompt: str) -> str:
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
    NSRunningApplication.currentApplication().activateWithOptions_(1 << 1)

    alert = NSAlert.alloc().init()
    alert.setMessageText_(TITLE)
    alert.setInformativeText_(prompt)
    alert.addButtonWithTitle_(SUBMIT_BUTTON)
    alert.addButtonWithTitle_(CANCEL_BUTTON)

    scroll_view = NSScrollView.alloc().initWithFrame_(
        NSMakeRect(0, 0, TEXTAREA_WIDTH, TEXTAREA_HEIGHT)
    )
    scroll_view.setHasVerticalScroller_(True)
    scroll_view.setHasHorizontalScroller_(False)
    scroll_view.setAutohidesScrollers_(True)

    text_view = NSTextView.alloc().initWithFrame_(
        NSMakeRect(0, 0, TEXTAREA_WIDTH, TEXTAREA_HEIGHT)
    )
    text_view.setRichText_(False)
    text_view.setImportsGraphics_(False)
    text_view.setHorizontallyResizable_(False)
    text_view.setVerticallyResizable_(True)
    text_view.setMinSize_(NSMakeSize(0, TEXTAREA_HEIGHT))
    text_view.setMaxSize_(NSMakeSize(1_000_000, 1_000_000))
    text_container = text_view.textContainer()
    text_container.setContainerSize_(NSMakeSize(TEXTAREA_WIDTH, 1_000_000))
    text_container.setWidthTracksTextView_(True)
    text_view.setString_("")

    scroll_view.setDocumentView_(text_view)
    alert.setAccessoryView_(scroll_view)

    text_view.window().makeFirstResponder_(text_view) if text_view.window() else None
    response = alert.runModal()

    if response != NSAlertFirstButtonReturn:
        raise SystemExit(1)

    return str(text_view.string()).rstrip("\n")


def main() -> int:
    args = parse_args()
    prompt = resolve_prompt(args)
    answer = ask(prompt)
    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
