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

- `'%H:%M:%S'` → `14:30:45`
- `'%Y-%m-%d %H:%M:%S'` → `2024-03-15 14:30:45`
- `'%I:%M:%S %p'` → `02:30:45 PM`
- `'%b %d %H:%M:%S'` → `Mar 15 14:30:45`
- `'%Y-%m-%d'` → `2024-03-15`

### Runtime Control

```python
# Enable/disable timestamps dynamically
Log.enable_time(True)   # Enable timestamps
Log.enable_time(False)  # Disable timestamps

# Change format on the fly
Log.set_time_format('%Y-%m-%d %H:%M:%S')
```

## Available Colors

DLogger supports the following color styles:

### Standard Colors
- `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`

### Bright Colors
- `bright_red`, `bright_green`, `bright_yellow`, `bright_blue`
- `bright_magenta`, `bright_cyan`, `bright_white`

### Text Styles
- `bold`, `underline`, `reset`

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
    time_format='%H:%M:%S'
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
```

## Requirements

- Python >= 3.8

## License

Licensed under GPL-3.0, see [LICENSE](LICENSE)

---

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

- `'%H:%M:%S'` → `14:30:45`
- `'%Y-%m-%d %H:%M:%S'` → `2024-03-15 14:30:45`
- `'%I:%M:%S %p'` → `02:30:45 PM`
- `'%b %d %H:%M:%S'` → `Mar 15 14:30:45`
- `'%Y-%m-%d'` → `2024-03-15`


## Available Colors

DLogger supports the following color styles:

### Standard Colors
- `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`

### Bright Colors
- `bright_red`, `bright_green`, `bright_yellow`, `bright_blue`
- `bright_magenta`, `bright_cyan`, `bright_white`

### Text Styles
- `bold`, `underline`, `reset`

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

You can create any method names you want: DLogger dynamically generates them at initialization!

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
    time_format='%H:%M:%S'
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
```

## Requirements

- Python >= 3.8

## License

Licensed under GPL-3.0, see [LICENSE](LICENSE)

---


![madebydouxx](https://madeby.douxx.tech)
![adpipproject](https://madeby.dpip.lol)