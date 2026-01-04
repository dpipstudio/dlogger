# DLogger

A lightweight, dynamic console logger for Python with colored output, automatic method generation, and optional timestamps.

## Installation

```bash
pip install dlogger
```

Or just copy `dlogger.py` into your project.


## Quick Start

```python
from dlogger import DLogger

# Create your logger with custom icons and colors
Log = DLogger(
    icons={
        'success': 'OK',
        'error': 'ERR',
        'warning': 'WARN',
        'info': 'INFO',
    },
    styles={
        'success': 'bright_green',
        'error': 'bright_red',
        'warning': 'bright_yellow',
        'info': 'bright_cyan',
    }
)

# Use the dynamically generated methods
Log.success("Operation completed!")
Log.error("Something went wrong!")
Log.warning("Be careful!")
Log.info("Just so you know...")
```

**Output:**
```
[OK] Operation completed!        # in bright green
[ERR] Something went wrong!      # in bright red
[WARN] Be careful!               # in bright yellow
[INFO] Just so you know...       # in bright cyan
```

## Timestamps (Optional)

Enable timestamps with customizable formats:

```python
Log = DLogger(
    icons={'info': 'INFO', 'error': 'ERR'},
    styles={'info': 'bright_cyan', 'error': 'bright_red'},
    show_time=True,                      # Enable timestamps (default: False)
    time_format='%H:%M:%S',              # Customize format (default: '%H:%M:%S')
    time_style='bright_white'            # Timestamp color (default: 'bright_white')
)

Log.info("Application started")
Log.error("Connection failed")
```

**Output:**
```
[14:30:45] [INFO] Application started
[14:30:47] [ERR] Connection failed
```

### Common Time Formats

- `'%H:%M:%S'` -> `14:30:45`
- `'%Y-%m-%d %H:%M:%S'` -> `2024-03-15 14:30:45`
- `'%I:%M:%S %p'` -> `02:30:45 PM`
- `'%b %d %H:%M:%S'` -> `Mar 15 14:30:45`
- `'%Y-%m-%d'` -> `2024-03-15`

## Custom Delimiters

Customize the brackets around icons and timestamps:
```python
Log = DLogger(
    icons={'info': 'INFO', 'error': 'ERR'},
    styles={'info': 'bright_cyan', 'error': 'bright_red'},
    delimiters='()' # Use parentheses instead of brackets
)

Log.info("Message with parentheses")
```

**Output:**
```
(INFO) Message with parentheses
```

**Available delimiter styles:**
- `'[]'` -> `[INFO]` (default)
- `'()'` -> `(INFO)`
- `'{}'` -> `{INFO}`
- `'<>'` -> `<INFO>`
- `'||'` -> `|INFO|`
- `'--'` -> `-INFO-`
> Those are only examples, you can use any character you want as a delimiter.

Note: Delimiters must have an even number of characters. The first half becomes the left delimiter, the second half becomes the right delimiter.

## Output Stream
Output stream for console logging (default: sys.stdout).
Use sys.stdout for regular output or sys.stderr for diagnostics/logs.

## Available Colors

DLogger supports the following color styles:

### Standard Colors
`black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, `gray`

### Bright Colors
`bright_red`, `bright_green`, `bright_yellow`, `bright_blue`, `bright_magenta`, `bright_cyan`, `bright_white`

### Special Colors
`orange`, `purple`, `pink`

### Text Styles
`bold`, `dim`, `italic`, `underline`, `blink`, `reverse`, `hidden`, `strikethrough`

### Background Colors
`bg_black`, `bg_red`, `bg_green`, `bg_yellow`, `bg_blue`, `bg_magenta`, `bg_cyan`, `bg_white`, `bg_gray`, `bg_orange`, `bg_purple`, `bg_pink`

### Bright Background Colors
`bg_bright_red`, `bg_bright_green`, `bg_bright_yellow`, `bg_bright_blue`, `bg_bright_magenta`, `bg_bright_cyan`, `bg_bright_white`

## Advanced Color Options

### True Color (RGB)

Use 16 million colors with RGB values:
```python
# Create a custom RGB color
coral = Log.rgb(255, 127, 80)
Log.print("Beautiful coral text", style=coral, icon='RGB')

# Background colors
bg_color = Log.rgb(50, 50, 50, background=True)
Log.print("Text with custom background", style=bg_color, icon='BG')

# Combine with other styles
Log.print("Bold coral", style=f'bold {coral}', icon='MIX')
```

### 256-Color Palette

Access the 256-color terminal palette:
```python
# Use 256-color codes (0-255)
orange = Log.c256(208)
Log.print("Orange text", style=orange, icon='256')

# Background colors
bg = Log.c256(234, background=True)
Log.print("Dark background", style=bg, icon='BG')
```

### Combining Styles

Mix multiple styles together:
```python
# Multiple styles with spaces
Log.print("Bold + Underline + Color", 
          style='bold underline bright_green', 
          icon='MIX')

# RGB with text styles
custom = Log.rgb(255, 100, 50)
Log.print("Bold custom color", style=f'bold {custom}', icon='RGB')

# Inline style definitions
Log.print("Inline RGB", style='rgb(255, 100, 50)', icon='RGB')
Log.print("Inline 256", style='c256(208)', icon='256')
Log.print("Combined", style='bold underline rgb(255,100,50)', icon='ALL')
```

**Inline Style Formats:**
- RGB: `'rgb(r,g,b)'` or `'rgb(r,g,b,bg)'` for background
- 256-color: `'c256(code)'` or `'c256(code,bg)'` for background

## Additional Features

### Headers and Sections

```python
Log.header("My Application")
Log.section("Configuration")
```

### Progress Bars

```python
for i in range(101):
    Log.progress_bar(i, 100, prefix='Loading:', suffix='Complete')
```

**Output:**
```
Loading: [#####################---------] 70.0% Complete
```

### Manual Printing

```python
# Print without using generated methods
Log.print("Custom message", style='magenta', icon='CUSTOM')
```

## Saving Logs to Files

DLogger can save logs to files in addition to displaying them in the console:

### Single File Mode

Save all logs to a single file:
```python
Log = DLogger(
    icons={'info': 'INFO', 'error': 'ERR', 'success': 'OK'},
    styles={'info': 'bright_cyan', 'error': 'bright_red', 'success': 'bright_green'},
    save=True,
    single_file=True,
    save_to='app.log'  # File path
)

Log.info("Application started")
Log.error("Connection failed")
Log.success("Recovered successfully")
```

**Result:** All logs saved to `app.log`:
```
[INFO] Application started
[ERR] Connection failed
[OK] Recovered successfully
```

### Multiple Files Mode

Save logs to separate files based on their icon names:
```python
Log = DLogger(
    icons={'info': 'INFO', 'error': 'ERR', 'success': 'OK'},
    styles={'info': 'bright_cyan', 'error': 'bright_red', 'success': 'bright_green'},
    save=True,
    single_file=False,
    save_to='./logs'  # Directory path
)

Log.info("Application started")
Log.error("Connection failed")
Log.success("Recovered successfully")
```

**Result:** Creates separate files:
- `./logs/INFO.log` -> `[INFO] Application started`
- `./logs/ERR.log` -> `[ERR] Connection failed`
- `./logs/OK.log` -> `[OK] Recovered successfully`

### Save Options
```python
Log = DLogger(
    icons={'info': 'INFO'},
    save=True,              # Enable saving (default: False)
    single_file=True,       # One file vs. multiple files (default: False)
    save_to='app.log',      # File or directory path (default: '.')
    strip_ansi=True         # Remove color codes from files (default: True)
)
```

**Parameters:**
- `save`: Enable or disable file saving
- `single_file`: If `True`, all logs go to one file. If `False`, separate files per icon
- `save_to`: File path (single file mode) or directory path (multiple files mode)
- `strip_ansi`: If `True`, removes color codes from saved logs for clean text files

### With Timestamps

Timestamps are automatically included in saved logs when enabled:
```python
Log = DLogger(
    icons={'info': 'INFO'},
    show_time=True,
    time_format='%Y-%m-%d %H:%M:%S',
    save=True,
    save_to='app.log'
)

Log.info("Server started")
```

**Saved to file:**
```
[2024-03-15 14:30:45] [INFO] Server started
```

## How It Works

DLogger automatically generates methods based on your `icons` dictionary. Each key becomes a method name:

```python
Log = DLogger(
    icons={'database': 'DB', 'api': 'API', 'cache': 'CACHE'},
    styles={'database': 'green', 'api': 'blue', 'cache': 'yellow'}
)

Log.database("Connected to PostgreSQL")  # [DB] Connected to PostgreSQL
Log.api("Request received")              # [API] Request received
Log.cache("Cache hit!")                  # [CACHE] Cache hit!
```

You can create any method names you want - DLogger dynamically generates them at initialization!

## Complete Example

```python
from dlogger import DLogger
import time

# Initialize with timestamps
Log = DLogger(
    icons={
        'start': '▶',
        'done': '✓',
        'fail': '✗',
        'info': 'ℹ'
    },
    styles={
        'start': 'bright_blue',
        'done': 'bright_green',
        'fail': 'bright_red',
        'info': 'bright_cyan'
    },
    show_time=True,
    time_format='%H:%M:%S',
    save=True,
    single_file=True,
    save_to='application.log'
)

Log.header("Application Startup")
Log.start("Initializing...")

Log.section("Database Connection")
Log.info("Connecting to database...")
time.sleep(1)
Log.done("Database connected successfully")

Log.section("Loading Configuration")
for i in range(101):
    Log.progress_bar(i, 100, prefix='Loading:', suffix='Complete', 
                     fill='█', style='bright_green')
    time.sleep(0.02)

Log.done("Application ready!")
# All logs are now saved to 'application.log' without color codes
```

## Requirements

- Python >= 3.6

## License

Licensed under GPL-3.0, see [LICENSE](LICENSE)