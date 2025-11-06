# Todu Menu Bar App

macOS menu bar application for at-a-glance task visibility.

## Overview

This app provides a macOS menu bar icon that displays your current task counts and provides quick access to task management functions. It reads directly from the todu cache (`~/.local/todu/issues/*.json`) and updates automatically as tasks change.

## Features

### Icon Display

- Shows count of "Now" tasks (in-progress) in menu bar (e.g., "📋 5")
- Updates dynamically as tasks change

### Menu Structure

```text
Now: X tasks
Next: X tasks
───────────
High Priority: X
Due Today: X
Overdue: X (if any)
───────────
Projects:
  • project1 (X open)
  • project2 (X open)
───────────
⟳ Sync Now
📊 Open Full Report
───────────
Quit
```

## Installation

### Dependencies

The app uses `uv` for dependency management. Dependencies are specified in the script headers:

- `rumps>=0.4.0` - Menu bar app framework
- `watchdog>=3.0.0` - File system event monitoring

### Running

```bash
# From the todu project root
./menubar/app.py

# Or using uv directly
uv run menubar/app.py
```

### Launch on Startup (Optional)

To launch the app automatically when you log in:

1. Open **System Settings** → **General** → **Login Items**
2. Click the **+** button under "Open at Login"
3. Navigate to and select the `menubar/app.py` script

Alternatively, create a LaunchAgent plist file at `~/Library/LaunchAgents/com.todu.menubar.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.todu.menubar</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/todu/menubar/app.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Then load it:

```bash
launchctl load ~/Library/LaunchAgents/com.todu.menubar.plist
```

## Usage

### Menu Actions

#### ⟳ Sync Now

Triggers an immediate sync of all task systems via `core/scripts/sync_manager.py`. A notification will appear when sync starts, and the menu will update automatically when sync completes.

#### 📊 Open Full Report

Generates a daily task report using the same logic as `core/scripts/report.py` and opens it in your default markdown viewer.

### Task Counts

- **Now**: Tasks with `status:in-progress` label (actively being worked on)
- **Next**: Tasks with `priority:high` label
- **High Priority**: Same as "Next" - tasks marked as high priority
- **Due Today**: Tasks with due date = today
- **Overdue**: Tasks with due date < today
- **Projects**: Count of open tasks grouped by project nickname

## How It Works

### Data Source

The app reads task data from `~/.local/todu/issues/*.json` files. It reuses logic from `core/scripts/report.py` for task counting and categorization.

### Auto-Update

The app uses two mechanisms to detect changes:

1. **File System Events** (primary): Uses `watchdog` to monitor the cache directory for changes. Updates occur within 1 second of cache modifications.

2. **Timer Fallback** (secondary): Refreshes data every 60 seconds in case file system events are missed.

### Performance

- Low CPU usage (only processes events/timers)
- Low memory footprint (~50MB RAM typical)
- Efficient JSON parsing (only reads changed files)

## Testing

Run the test script to validate functionality without launching the GUI:

```bash
./menubar/test_app.py
```

This will:

- Verify all imports work
- Test data loading from cache
- Test task categorization logic
- Display current task counts

## Troubleshooting

### App doesn't show in menu bar

- Ensure you're running on macOS
- Check that the script is executable: `chmod +x menubar/app.py`
- Try running with `uv run menubar/app.py` to see error messages

### Task counts are wrong

- Run `./menubar/test_app.py` to see current counts
- Verify cache files exist in `~/.local/todu/issues/`
- Run a manual sync to refresh cache

### Sync doesn't work

- Verify `core/scripts/sync_manager.py` exists and is executable
- Check system notification settings allow todu notifications

### Menu doesn't update

- Check file permissions on `~/.local/todu/issues/`
- Try quitting and restarting the app
- The timer fallback will update every 60 seconds regardless

## Architecture

```text
menubar/app.py
├── ToduMenuBar (main app class)
│   ├── __init__: Setup menu, start watchers
│   ├── setup_file_watching: Start watchdog observer
│   ├── timer_callback: 60s fallback refresh
│   ├── update_task_data: Load and count tasks
│   ├── update_menu_items: Refresh menu display
│   ├── sync_now: Trigger manual sync
│   └── open_report: Generate and open report
├── TaskData: Task count container
└── CacheFileHandler: File system event handler

Dependencies on core/scripts:
├── report.py: Task loading and categorization
├── list-items.py: Cache file parsing
└── sync_manager.py: Multi-system sync (called by Sync Now)
```

## Future Enhancements

See issue #37 for planned future features:

- Notification support (toast when high-priority tasks appear)
- Click-through to open issues in browser
- Inline task completion from menu
- Custom filtering/sorting in menu
- Settings UI (currently uses hardcoded values)
