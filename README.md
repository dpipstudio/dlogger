# DLogger

A lightweight, dynamic console logger for Python with colored output and automatic method generation.

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

## License

Licensed under GPLv3.0, see [LICENSE](LICNSE)

![madebydouxx](https://madeby.douxx.tech)
![adpipproject](https://madeby.dpip.lol)