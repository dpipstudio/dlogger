#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DLogger: Dynamic Console Logger for Python

A lightweight, dynamic logger with colored output, custom icons, and
automatic method generation. Includes progress bars, headers, and sections.

A DPIP Studio project - See https://dpip.lol

Author: Douxxtech
Email: douxx@douxx.tech
GitHub: https://github.com/dpipstudio/dlogger
License: GPL-3.0
Python: >=3.6

Example:
    >>> from dlogger import DLogger
    >>> Log = DLogger(
    ...     icons={'success': 'OK', 'error': 'ERR'},
    ...     styles={'success': 'bright_green', 'error': 'bright_red'},
    ...     show_time=True,
    ...     time_format='%Y-%m-%d %H:%M:%S'
    ... )
    >>> Log.success("Operation completed!")
    >>> Log.error("Something went wrong!")
"""

import os
import sys
from datetime import datetime
from typing import Dict, Optional, Callable, TextIO

if os.name == 'nt':
    import msvcrt
else:
    import fcntl

class DLogger:
    """
    Dynamic logger that generates methods based on icon configuration.
    
    This class automatically creates logging methods (e.g., `success()`, `error()`)
    based on the icons dictionary provided during initialization. Each method
    will print a message with its corresponding icon and style.
    
    Attributes:
        COLORS (Dict[str, str]): ANSI color codes for terminal styling.
        ICONS (Dict[str, str]): User-defined mapping of method names to icon strings.
        
    Example:
        >>> Log = DLogger(
        ...     icons={'info': 'INFO', 'warn': 'WARN'},
        ...     styles={'info': 'cyan', 'warn': 'yellow'}
        ... )
        >>> Log.info("This is informational")  # Prints: [INFO] This is informational
        >>> Log.warn("This is a warning")      # Prints: [WARN] This is a warning
    """
    
    COLORS: Dict[str, str] = {
        'reset': '\033[0m',
        
        'bold': '\033[1m',
        'dim': '\033[2m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        'blink': '\033[5m',
        'reverse': '\033[7m',
        'hidden': '\033[8m',
        'strikethrough': '\033[9m',
        
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'gray': '\033[90m',
        'orange': '\033[38;5;208m',
        'purple': '\033[38;5;129m',
        'pink': '\033[38;5;213m',
        'bg_orange': '\033[48;5;208m',
        'bg_purple': '\033[48;5;129m',
        'bg_pink': '\033[48;5;213m',
        
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        
        'bg_black': '\033[40m',
        'bg_red': '\033[41m',
        'bg_green': '\033[42m',
        'bg_yellow': '\033[43m',
        'bg_blue': '\033[44m',
        'bg_magenta': '\033[45m',
        'bg_cyan': '\033[46m',
        'bg_white': '\033[47m',
        'bg_gray': '\033[100m',

        'bg_bright_red': '\033[101m',
        'bg_bright_green': '\033[102m',
        'bg_bright_yellow': '\033[103m',
        'bg_bright_blue': '\033[104m',
        'bg_bright_magenta': '\033[105m',
        'bg_bright_cyan': '\033[106m',
        'bg_bright_white': '\033[107m',
    }
    
    def __init__(self, icons: Dict[str, str] = None, styles: Optional[Dict[str, str]] = None,
                 show_time: bool = False, time_format: str = '%H:%M:%S',
                 time_style: str = 'bright_white', delimiters: str = '[]', save: bool = False, single_file: bool = False, save_to: str = ".", stream: TextIO = sys.stdout) -> None:
        """
        Initialize logger with icons and optional style mappings.
        
        Dynamically generates methods for each icon key. For example, if you pass
        `icons={'success': 'OK'}`, a `Log.success(message)` method will be created.
        
        Args:
            icons: Dictionary mapping method names to icon strings.
                   Example: {'success': 'OK', 'error': 'ERR', 'info': 'INFO'}
            styles: Optional dictionary mapping method names to color styles.
                    Must use keys from COLORS dict. Supports multiple styles
                    separated by spaces (e.g., 'bold bright_green').
                    Example: {'success': 'bright_green', 'error': 'bright_red'}
            show_time: Whether to display timestamp before messages (default: False).
            time_format: strftime format string for timestamp (default: '%H:%M:%S').
                    Common formats:
                    - '%H:%M:%S' -> 14:30:45
                    - '%Y-%m-%d %H:%M:%S' -> 2025-11-16 16:52:45
                    - '%I:%M:%S %p' -> 04:52:45 PM
                    - '%b %d %H:%M:%S' -> Mar 15 16:52:45
            time_style: Color style for timestamp (default: 'bright_white').
            delimiters: String of characters to use as delimiters around icons and
                    timestamps. Must have an even number of characters. The first
                    half becomes the left delimiter, the second half becomes the
                    right delimiter. Examples: '[]' (default), '()', '{}', '<>',
                    '||', '--'.
            save: Enable saving logs to file(s). When True, all log messages will be
                    written to disk in addition to console output (default: False).
            single_file: If True, all logs are saved to a single file specified by
                    save_to. If False, logs are saved to separate files based on
                    their icon names (e.g., 'success.log', 'error.log') in the
                    save_to directory (default: False).
            save_to: File or directory path for saved logs. If single_file is True,
                    this should be a file path (e.g., 'app.log'). If single_file is
                    False, this should be an existing directory path where separate
                    log files will be created (default: '.').
            stream: Output stream for console logging (default: sys.stdout).
                    
        Raises:
            ValueError: If delimiters string has an odd number of characters.
            
        Example:
            >>> Log = DLogger(
            ...     icons={'success': 'OK', 'error': 'ERR'},
            ...     styles={'success': 'bright_green', 'error': 'bright_red'},
            ...     show_time=True,
            ...     time_format='%Y-%m-%d %H:%M:%S',
            ...     delimiters='()'
            ... )
            >>> # This creates Log.success() and Log.error() methods automatically
        """

        if len(delimiters) % 2 != 0:
            raise ValueError("'delimiters' argument must be a string of an even count of characters.")
            Hi :3

        if save:
            if single_file:
                save_dir = os.path.dirname(save_to) or '.'

                if not os.path.exists(save_dir):
                    raise ValueError(f"Directory '{save_dir}' does not exist for save_to file path.")
                
                if os.path.isdir(save_to):
                    raise ValueError("'save_to' must be a file path when 'single_file' is True.")
                
            else:
                if not os.path.isdir(save_to):
                    raise ValueError(f"'save_to' must be an existing directory when 'single_file' is False.")

        self._icons: Dict[str, str] = icons or {}
        self._styles: Dict[str, str] = styles or {}
        self._show_time: bool = show_time
        self._time_format: str = time_format
        self._time_style: str = time_style
        self._left_delimiter, self._right_delimiter = delimiters[:len(delimiters)//2 + len(delimiters)%2], delimiters[len(delimiters)//2 + len(delimiters)%2:]
        self._save: bool = save
        self._single_file: bool = single_file
        self._save_path: str = save_to
        self._stream: TextIO = stream
        self._generate_methods()
    
    def print(self, message: str, style: str = '', icon: str = '', end: str = '\n') -> None:
        """
        Core print method with styling and icon support.
        
        Supports multiple styles combined with spaces (e.g., 'bold bright_green').
        Uses custom delimiters if configured during initialization.
        
        Args:
            message: The text message to print.
            style: Color style from COLORS dict (e.g., 'bright_green', 'red').
                   Can combine multiple styles with spaces (e.g., 'bold underline green').
            icon: Icon text to display in delimiters before the message.
            end: String appended after the message (default: newline).
            
        Example:
            >>> Log = DLogger(icons={})
            >>> Log.print("Hello", style='green', icon='MSG')
            [MSG] Hello
            >>> Log.print("Important", style='bold bright_red', icon='ALERT')
            [ALERT] Important
        """
        color = self._parse_style(style)
        icon_char = icon
        timestamp = self._get_timestamp()
        
        # output parts
        parts = []
        
        if timestamp:
            time_color = self._parse_style(self._time_style)
            if time_color:
                parts.append(f"{time_color}{self._left_delimiter}{timestamp}{self._right_delimiter}\033[0m")
            else:
                parts.append(f"{self._left_delimiter}{timestamp}{self._right_delimiter}")
        
        if icon_char:
            if color:
                parts.append(f"{color}{self._left_delimiter}{icon_char}{self._right_delimiter}\033[0m")
            else:
                parts.append(f"{self._left_delimiter}{icon_char}{self._right_delimiter}")
        
        if color and not icon_char:
            parts.append(f"{color}{message}\033[0m")
        else:
            parts.append(message)
        
        output_str = ' '.join(parts) + end
        self._stream.write(output_str)
        self._stream.flush()

        try:
            if self._save:
                if self._single_file:
                    if self._single_file:
                        timestamp_part = f"{self._left_delimiter}{timestamp}{self._right_delimiter} " if timestamp else ''
                        self._save_to(f"{timestamp_part}{self._left_delimiter}{icon_char}{self._right_delimiter} {message} {end}", self._save_path)
                else:
                    timestamp_part = f"{self._left_delimiter}{timestamp}{self._right_delimiter} " if timestamp else ''
                    self._save_to(f"{timestamp_part}{self._left_delimiter}{icon_char}{self._right_delimiter} {message} {end}", os.path.join(self._save_path, f"{icon_char if icon else 'default'}.log"))
        except:
            ... # maybe do something one time
    
    def header(self, text: str, style: str = 'bright_blue') -> None:
        """
        Print a header message with extra spacing.
        
        Args:
            text: The header text to display.
            
        Example:
            >>> Log = DLogger(icons={})
            >>> Log.header("Application Started")
            Application Started
            
        """
        self.print(text, style, end='\n\n')
        sys.stdout.flush()
    
    def section(self, text: str, style: str = 'bright_blue', bar_sytle: str = 'blue') -> None:
        """
        Print a section divider with decorative line.
        
        Creates a visual separator with the section name followed by a line of
        dashes matching the length of the text.
        
        Args:
            text: The section title to display.
            
        Example:
            >>> Log = DLogger(icons={})
            >>> Log.section("Configuration")
             Configuration ────────────────
            
        """
        self.print(f" {text} ", style, end='')
        self.print("─" * (len(text) + 2), bar_sytle, end='\n\n')
        sys.stdout.flush()
    
    def progress_bar(self, iteration: int, total: int, prefix: str = '', 
                 suffix: str = '', length: int = 30, fill: str = '#', 
                 style: str = 'bright_cyan', icon: str = '', 
                 auto_clear: bool = True) -> None:
        """
        Display a progress bar in the terminal.
        
        Shows a visual progress indicator that updates in place. Automatically
        adds a newline when reaching 100% if auto_clear is True.
        
        Args:
            iteration: Current iteration/progress value.
            total: Total iterations/maximum value.
            prefix: Text to display before the progress bar.
            suffix: Text to display after the progress bar.
            length: Character length of the progress bar (default: 30).
            fill: Character used to fill the completed portion (default: '#').
            style: Color style for the progress bar.
            icon: Optional icon to display before the progress bar.
            auto_clear: If True, adds newline when reaching 100% (default: True).
            
        Example:
            >>> Log = DLogger(icons={})
            >>> for i in range(101):
            ...     Log.progress_bar(i, 100, prefix='Loading:', suffix='Complete')
            Loading: [##########--------------------] 50.0% Complete
        """
        
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        color = self._parse_style(style)
        
        if icon:
            if color:
                self._stream.write(f"\r{color}[{icon}]\033[0m {prefix} [{bar}] {percent}% {suffix}")
            else:
                self._stream.write(f"\r[{icon}] {prefix} [{bar}] {percent}% {suffix}")
        else:
            if color:
                self._stream.write(f"\r{color}{prefix} [{bar}] {percent}% {suffix}\033[0m")
            else:
                self._stream.write(f"\r{prefix} [{bar}] {percent}% {suffix}")
        self._stream.flush()

        if auto_clear and iteration >= total:
            self._stream.write('\n')
            self._stream.flush()

    
    def clear_progress_bar(self) -> None:
        """
        Manually clear the progress bar line by printing a newline.
        
        Useful when auto_clear is False or when you need to manually
        clear the progress bar before completion.
        
        Example:
            >>> Log = DLogger(icons={})
            >>> Log.progress_bar(50, 100, auto_clear=False)
            >>> Log.clear_progress_bar()
        """
        sys.stdout.write('\n')
        sys.stdout.flush()

    def rgb(self, r: int, g: int, b: int, background: bool = False) -> str:
       """
        Generate ANSI escape code for 24-bit RGB color.
        
        Creates a color code string for true color (16 million colors) support
        in compatible terminals. The returned string can be used in print statements.
        
        Args:
            r: Red component (0-255).
            g: Green component (0-255).
            b: Blue component (0-255).
            background: If True, applies color to background instead of foreground
                       (default: False).
        
        Returns:
            ANSI escape code string for the specified RGB color.
            
        Example:
            >>> Log = DLogger(icons={})
            >>> custom_color = Log.rgb(255, 100, 50)
            >>> Log.print("Hello!", style=custom_color, icon="WLC")
        """
       
       return f'\033[{48 if background else 38};2;{r};{g};{b}m'
    
    def c256(self, code: int, background: bool = False) -> str:
        """
        Generate ANSI escape code for 256-color palette.
        
        Creates a color code string using the 256-color palette supported by
        most modern terminals. The returned string can be used in print statements.
        
        Args:
            code: Color code from the 256-color palette (0-255).
                  Standard colors: 0-15
                  216 color cube: 16-231 (6x6x6 RGB cube)
                  Grayscale: 232-255
            background: If True, applies color to background instead of foreground
                       (default: False).
        
        Returns:
            ANSI escape code string for the specified palette color.
            
        Example:
            >>> Log = DLogger(icons={})
            >>> orange = Log.c256(208)
            >>> Log.print(":3", style=orange, icon="ORG")
        """

        return f'\033[{48 if background else 38};5;{code}m'
    
    def _generate_methods(self) -> None:
        """
        Generate convenience methods for each icon dynamically.
        
        For each key in the icons dictionary, this creates a method on the
        instance that calls `self.print()` with the appropriate icon and style.
        
        For example, if icons={'success': 'OK'} and styles={'success': 'green'},
        this will create a method `self.success(message)` that prints the message
        with the 'OK' icon in green color.
        
        Note:
            This is called automatically during __init__. You should not need
            to call this method manually.
        """
        for method_name, icon_text in self._icons.items():
            style = self._styles.get(method_name, '')
            
            def make_method(icon_val: str, style_val: str) -> Callable[[str], None]:
                def method(message: str) -> None:
                    """
                    Dynamically generated logging method.
                    
                    Args:
                        message: The message to log.
                    """
                    self.print(message, style_val, icon_val)
                return method
            
            # Bind the method to this instance
            setattr(self, method_name, make_method(icon_text, style))

    def _parse_style(self, style: str) -> str:
        """
        Parse style string and convert to ANSI codes.
        
        Supports:
        - Named colors: 'green', 'bold bright_red'
        - RGB format: 'rgb(255, 100, 50)' or 'rgb(255,100,50,bg)'
        - 256-color format: 'c256(208)' or 'c256(208,bg)'
        - Direct ANSI codes: returned from rgb() and c256() functions
        - Combinations: 'bold rgb(255,100,50) underline'
        
        Args:
            style: Style string with one or more color/style specifications,
                or direct ANSI escape codes.
        
        Returns:
            Combined ANSI escape code string, or empty string if style is invalid.
            
        Example:
            >>> Log._parse_style('green')
            >>> Log._parse_style('bold rgb(255,100,50)')
            >>> custom = Log.rgb(255, 100, 50)
            >>> Log._parse_style(custom)
        """
        if not style:
            return ''
        
        if style.startswith('\033['):
            return style
        
        if ' ' not in style and '(' not in style:
            return self.COLORS.get(style, '')
        
        style_parts = [s.strip() for s in style.split()]
        codes = []
        
        for part in style_parts:
            if part.startswith('\033['):
                codes.append(part)
                continue
            
            # rgb format: rgb(r,g,b) or rgb(r,g,b,bg)
            if part.startswith('rgb(') and part.endswith(')'):
                try:
                    params = part[4:-1].split(',')
                    params = [p.strip() for p in params]
                    
                    if len(params) == 3:
                        r, g, b = int(params[0]), int(params[1]), int(params[2])
                        codes.append(self.rgb(r, g, b, background=False))
                    elif len(params) == 4 and params[3].lower() == 'bg':
                        r, g, b = int(params[0]), int(params[1]), int(params[2])
                        codes.append(self.rgb(r, g, b, background=True))
                except (ValueError, IndexError):
                    pass
            
            # 256-color format: c256(code) or c256(code,bg)
            elif part.startswith('c256(') and part.endswith(')'):
                try:
                    params = part[5:-1].split(',')
                    params = [p.strip() for p in params]
                    
                    if len(params) == 1:
                        code = int(params[0])
                        codes.append(self.c256(code, background=False))
                    elif len(params) == 2 and params[1].lower() == 'bg':
                        code = int(params[0])
                        codes.append(self.c256(code, background=True))
                except (ValueError, IndexError):
                    pass
            
            elif part in self.COLORS:
                codes.append(self.COLORS[part])
        
        return ''.join(codes)
    
    def _get_timestamp(self) -> str:
        """
        Get formatted timestamp string.
        
        Returns:
            Formatted timestamp string according to time_format setting.
        """
        if not self._show_time:
            return ''
        try:
            return datetime.now().strftime(self._time_format)
        except ValueError:
            # fallback if format string is invalid
            return datetime.now().strftime('%H:%M:%S')
        
    def _save_to(self, content, path):
        """
        Save content to file with proper file locking.
        
        Writes log content to the specified file path using file locking
        to prevent corruption from concurrent writes. Automatically creates
        the file if it doesn't exist, or appends to existing files.
        
        Args:
            content: Text content to save to the file.
            path: Full file path where content should be saved.
        
        Raises:
            IOError: If file operations fail due to permissions, disk space,
                    or other I/O errors.
                    
        Note:
            Uses platform-specific locking (msvcrt on Windows, fcntl on Unix).
        """
        try:
            with open(path, "a", encoding='utf-8') as f:
                self._lock_file(f)
                try:
                    f.write(content)
                    f.flush()
                finally:
                    self._unlock_file(f)
        except Exception as e:
            raise IOError(f"Failed to write to {path}: {e}")

    if os.name == 'nt':
        def _lock_file(self, f):
            """
            Locks a file, on Windows systems
            
            :param f: File object to lock
            """
            msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)

        def _unlock_file(self, f):
            """
            Unlocks a file, on Windows systems
            
            :param f: File object to unlock
            """
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)

    else:
        def _lock_file(self, f):
            """
            Locks a file, on other systems
            
            :param f: File object to lock
            """
            fcntl.flock(f, fcntl.LOCK_EX)

        def _unlock_file(self, f):
            """
            Unlocks a file, on other systems
            
            :param f: File object to unlock
            """
            fcntl.flock(f, fcntl.LOCK_UN)


if __name__ == "__main__":
    Log = DLogger(
        icons={
            'welcome': 'WLC',
            'info': 'INFO',
            'example': 'CODE',
            'output': 'OUT',
            'demo': 'DEMO'
        },
        styles={
            'welcome': 'bright_cyan',
            'info': 'white',
            'example': 'yellow',
            'output': 'bright_green',
            'demo': 'magenta'
        }
    )

    Log.header("DLogger", 'bold bright_magenta')
    Log.welcome("Dynamic Console Logger for Python\n")
    
    Log.section("Overview")
    Log.info("DLogger is a simple logging tool with colors, icons, and progress bars.")
    Log.info("Define your icons once, get custom methods automatically.\n")
    
    Log.section("Basic Usage")
    Log.example("from dlogger import DLogger")
    Log.example("")
    Log.example("Log = DLogger(")
    Log.example("    icons={'success': 'OK', 'error': 'ERR'},")
    Log.example("    styles={'success': 'green', 'error': 'red'}")
    Log.example(")")
    Log.example("")
    Log.example("Log.success('Connected to database')")
    Log.example("Log.error('Connection failed')")
    print()
    
    Log.output("Output:")
    demo_log = DLogger(
        icons={'success': 'OK', 'error': 'ERR'},
        styles={'success': 'bright_green', 'error': 'bright_red'}
    )
    demo_log.success("Connected to database")
    demo_log.error("Connection failed")
    print()
    
    Log.section("Available Colors")
    for color in Log.COLORS:
        Log.print('', style=color, icon=color, end=' ')
    Log.header("")
    
    
    Log.section("Custom Colors")
    Log.example("# RGB colors (16 million options)")
    Log.example("custom = Log.rgb(255, 100, 50)")
    Log.example("Log.print('Message', style=custom)")
    print()
    
    Log.example("# 256-color palette")
    Log.example("orange = Log.c256(208)")
    Log.example("Log.print('Message', style=orange)")
    print()

    Log.example("# 256-color palette + underline")
    Log.example("Log.print('Message', style='underline c256(208)')")
    
    Log.output("Output:")
    coral = Log.rgb(255, 127, 80)
    Log.print("RGB color example", style=coral, icon='RGB')
    orange = Log.c256(208)
    Log.print("256-color example", style=orange, icon='256')
    Log.print('Underlined + 256-color example', style='underline c256(208)', icon="MIX")
    print()
    
    Log.section("Links")
    Log.info("GitHub: https://github.com/dpipstudio/dlogger")
    Log.info("DPIP Studio: https://dpip.lol")
    print()
    
    Log.header("Happy Logging!", 'bright_green')