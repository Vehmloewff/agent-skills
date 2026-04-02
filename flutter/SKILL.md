---
name: flutter
description: Use Flutter MCP tools via `mcpc` to launch, inspect, reload, restart, and drive running Flutter apps, including `flutter_driver` automation for driver-enabled apps.
---

# Flutter MCP + `flutter_driver`

Use this skill when you need to inspect, reload, restart, or drive a running Flutter app through the local `mcpc` CLI and the Dart MCP server.

## Goal

Control a Flutter app through MCP tools, preferably without shelling out to raw Flutter commands once connected.

## When to use it

Use this skill when the task involves any of the following:
- launching a Flutter app through MCP
- connecting to a running app via the Dart Tooling Daemon
- inspecting the widget tree or app logs
- hot reloading or hot restarting a Flutter app
- automating UI interactions with `flutter_driver`
- debugging Flutter web automation issues

## Prerequisites

- `mcpc` is installed
- a Dart MCP server entry exists in `mcp.json`, for example `dart-mcp-server`
- Flutter SDK is installed
- if you need `flutter_driver`, the app must be launched with a special driver-enabled entrypoint

## Agent guidance

- Prefer MCP tool calls over raw `flutter` shell commands once connected.
- Prefer launching the app through MCP, because `launch_app` returns the DTD URI you need.
- Treat the DTD URI and the VM service URI as different things.
- For reliable automation, prefer `ValueKey`-based finders.
- On Flutter web, expect more flakiness from `flutter_driver` and use the recovery flow in this skill.

## 1. Connect the MCP server

Start by connecting the MCP server:

```bash
mcpc connect mcp.json:dart-mcp-server @flutter
```

Useful discovery commands:

```bash
mcpc @flutter tools-list
mcpc @flutter tools-list --full
mcpc @flutter tools-get <tool-name>
```

Important tools:

- `list_devices`
- `launch_app`
- `stop_app`
- `list_running_apps`
- `connect_dart_tooling_daemon`
- `hot_reload`
- `hot_restart`
- `get_widget_tree`
- `get_runtime_errors`
- `get_app_logs`
- `flutter_driver`

## 2. Understand DTD vs VM service

This is the first major gotcha.

### VM service URI is **not** the DTD URI

A Flutter run often prints something like:

- `Debug service listening on ws://...`
- `A Dart VM Service on Chrome is available at: http://...`

Those are **not** the Dart Tooling Daemon endpoint that MCP wants.

### What MCP needs

`connect_dart_tooling_daemon` requires the **DTD URI**.

Ways to get it:

- easiest: launch through MCP `launch_app`, which returns the DTD URI directly
- if the app is launched manually, run Flutter with:

```bash
flutter run --print-dtd
```

Then use the printed DTD URI with:

```bash
mcpc @flutter tools-call connect_dart_tooling_daemon '{"uri":"ws://127.0.0.1:PORT/TOKEN="}'
```

If you accidentally pass the VM service URI, MCP will tell you it connected to a VM service but expected a Dart Tooling Daemon service.

## 3. Preferred startup flow

If possible, let MCP launch the app.

### List devices

```bash
mcpc @flutter tools-call list_devices '{}'
```

### Launch app

```bash
mcpc @flutter tools-call launch_app '{"root":"/absolute/path/to/project","device":"chrome"}'
```

This returns:

- `pid`
- `dtdUri`

Then connect:

```bash
mcpc @flutter tools-call connect_dart_tooling_daemon '{"uri":"<DTD URI>"}'
```

Then verify:

```bash
mcpc @flutter tools-call list_running_apps '{}'
```

## 4. Useful non-driver MCP workflow

These worked reliably.

### Inspect widget tree

```bash
mcpc @flutter tools-call get_widget_tree '{"summaryOnly":true}'
```

Good for:

- understanding app structure
- discovering widget runtime types
- seeing text previews
- confirming `ValueKey`s appear in the tree

### Logs and runtime errors

```bash
mcpc @flutter tools-call get_runtime_errors '{"clearRuntimeErrors":false}'
mcpc @flutter tools-call get_app_logs '{"pid":12345,"maxLines":50}'
```

### Reload and restart

```bash
mcpc @flutter tools-call hot_reload '{"clearRuntimeErrors":true}'
mcpc @flutter tools-call hot_restart '{}'
```

Observed behavior:

- hot reload updates UI/code while preserving state
- hot restart resets state
- after some broken `flutter_driver` operations on web, `hot_restart` helped restore normal behavior

## 5. Getting `flutter_driver` working

This was the hardest part.

## Important lesson

For this Flutter web project, `flutter_driver` did **not** work by default.

It also did **not** work by simply importing `package:flutter_driver/driver_extension.dart` in `lib/main.dart` unless the package was added and the app was launched correctly.

The reliable setup was:

1. add `flutter_driver` in `dev_dependencies`
2. create a dedicated driver entrypoint in `test_driver/`
3. launch that entrypoint with MCP using `target`

### `pubspec.yaml`

Add:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_driver:
    sdk: flutter
```

Then run:

```bash
flutter pub get
```

### Create a driver entrypoint

Create `test_driver/flutter_driver_main.dart`:

```dart
import 'package:flutter_driver/driver_extension.dart';

import 'package:your_package_name/main.dart' as app;

void main() {
  enableFlutterDriverExtension();
  app.main();
}
```

Replace `your_package_name` with the package name from `pubspec.yaml`.

### Launch the driver target through MCP

```bash
mcpc @flutter tools-call launch_app '{"root":"/absolute/path/to/project","device":"chrome","target":"test_driver/flutter_driver_main.dart"}'
```

Then connect to the returned DTD URI.

## 6. Basic `flutter_driver` usage through MCP

The `flutter_driver` MCP tool wraps classic Flutter Driver commands.

### Read text by key

```bash
mcpc @flutter tools-call flutter_driver '{"command":"get_text","finderType":"ByValueKey","keyValueString":"counter_text","keyValueType":"String"}'
```

### Tap by key

```bash
mcpc @flutter tools-call flutter_driver '{"command":"tap","finderType":"ByValueKey","keyValueString":"increment_fab","keyValueType":"String"}'
```

### Wait for a widget

```bash
mcpc @flutter tools-call flutter_driver '{"command":"waitFor","finderType":"ByValueKey","keyValueString":"increment_fab","keyValueType":"String","timeout":"5000"}'
```

### Wait for text to disappear

```bash
mcpc @flutter tools-call flutter_driver '{"command":"waitForAbsent","finderType":"ByText","text":"Old Text","timeout":"3000"}'
```

### Wait for tappable

```bash
mcpc @flutter tools-call flutter_driver '{"command":"waitForTappable","finderType":"ByValueKey","keyValueString":"liked_switch","keyValueType":"String"}'
```

### Read widget position

```bash
mcpc @flutter tools-call flutter_driver '{"command":"get_offset","finderType":"ByValueKey","keyValueString":"increment_fab","keyValueType":"String","offsetType":"center"}'
```

### Read diagnostics tree for one widget

```bash
mcpc @flutter tools-call flutter_driver '{"command":"get_diagnostics_tree","finderType":"ByValueKey","keyValueString":"counter_text","keyValueType":"String","diagnosticsType":"widget","subtreeDepth":"2","includeProperties":"true"}'
```

### Check driver health

```bash
mcpc @flutter tools-call flutter_driver '{"command":"get_health"}'
```

## 7. Text entry gotcha on Flutter web

This is the second major gotcha.

On Flutter web, `enter_text` was flaky unless text entry emulation was enabled first.

### Working sequence

1. tap the field
2. enable text entry emulation
3. enter text

Example:

```bash
mcpc @flutter tools-call flutter_driver '{"command":"tap","finderType":"ByValueKey","keyValueString":"name_field","keyValueType":"String"}'

mcpc @flutter tools-call flutter_driver '{"command":"set_text_entry_emulation","enabled":"true"}'

mcpc @flutter tools-call flutter_driver '{"command":"enter_text","text":"Bob"}'
```

Without that, `enter_text` sometimes failed on web with an error involving:

- `Unsupported operation: StdIOUtils._getStdioOutputStream`

## 8. Other web-specific driver gotchas

These issues were observed on Chrome/web:

- `scrollIntoView` timed out in at least one case
- `tap` via `BySemanticsLabel` timed out in at least one case
- `screenshot` triggered a web runtime error involving stderr / stdio

What worked more reliably:

- `ByValueKey` finders
- `scroll` on a known scrollable widget using a key
- `get_text`
- `tap`
- `waitFor`
- `get_offset`
- `get_diagnostics_tree`

### Prefer `ValueKey`s

If you need robust automation, add stable `ValueKey`s in the app code and drive by those.

Examples:

- `counter_text`
- `status_text`
- `increment_fab`
- `name_field`
- `apply_name_button`
- `liked_switch`
- `main_list`
- `bottom_card`

## 9. Hot reload / restart behavior with driver-enabled apps

When driving the app launched from `test_driver/flutter_driver_main.dart`:

- `hot_reload` still worked
- after some reloads, the driver sometimes stopped responding temporarily
- `hot_restart` restored driver responsiveness

So if `flutter_driver` starts timing out after code changes:

1. check logs and runtime errors
2. try `hot_restart`
3. retry the driver command

## 10. Recommended debugging sequence when driver commands fail

1. confirm app is still running:

```bash
mcpc @flutter tools-call list_running_apps '{}'
```

2. inspect errors:

```bash
mcpc @flutter tools-call get_runtime_errors '{"clearRuntimeErrors":false}'
mcpc @flutter tools-call get_app_logs '{"pid":PID,"maxLines":80}'
```

3. verify driver extension is really active by trying:

```bash
mcpc @flutter tools-call flutter_driver '{"command":"get_health"}'
```

4. if commands start timing out after reloads, try:

```bash
mcpc @flutter tools-call hot_restart '{}'
```

5. if needed, stop and relaunch the app with the driver target

## 11. Minimal end-to-end recipe

### One-time app setup

- add `flutter_driver` to `dev_dependencies`
- create `test_driver/flutter_driver_main.dart`
- run `flutter pub get`

### Session setup

```bash
mcpc connect mcp.json:dart-mcp-server @flutter
mcpc @flutter tools-call launch_app '{"root":"/absolute/path/to/project","device":"chrome","target":"test_driver/flutter_driver_main.dart"}'
mcpc @flutter tools-call connect_dart_tooling_daemon '{"uri":"<DTD URI returned by launch_app>"}'
```

### First checks

```bash
mcpc @flutter tools-call flutter_driver '{"command":"get_health"}'
mcpc @flutter tools-call get_widget_tree '{"summaryOnly":true}'
```

### Example interaction

```bash
mcpc @flutter tools-call flutter_driver '{"command":"tap","finderType":"ByValueKey","keyValueString":"increment_fab","keyValueType":"String"}'
mcpc @flutter tools-call flutter_driver '{"command":"get_text","finderType":"ByValueKey","keyValueString":"counter_text","keyValueType":"String"}'
```

## 12. What to remember most

- DTD URI != VM service URI
- prefer launching through MCP because it returns the DTD URI directly
- `flutter_driver` needs explicit app setup
- on web, use a dedicated `test_driver` entrypoint
- add `flutter_driver` to `dev_dependencies`
- prefer `ByValueKey` over semantics/text when possible
- for text fields on web, enable text entry emulation before `enter_text`
- if driver becomes flaky after changes, `hot_restart` can recover it
