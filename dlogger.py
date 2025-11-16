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
Python: >=3.8

Example:
    >>> from dlogger import DLogger
    >>> Log = DLogger(
    ...     icons={'success': 'OK', 'error': 'ERR'},
    ...     styles={'success': 'bright_green', 'error': 'bright_red'}
    ... )
    >>> Log.success("Operation completed!")
    >>> Log.error("Something went wrong!")
"""

import sys
from typing import Dict, Optional, Callable


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
        'underline': '\033[4m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
    }
    
    def __init__(self, icons: Dict[str, str], styles: Optional[Dict[str, str]] = None) -> None:
        """
        Initialize logger with icons and optional style mappings.
        
        Dynamically generates methods for each icon key. For example, if you pass
        `icons={'success': 'OK'}`, a `Log.success(message)` method will be created.
        
        Args:
            icons: Dictionary mapping method names to icon strings.
                   Example: {'success': 'OK', 'error': 'ERR', 'info': 'INFO'}
            styles: Optional dictionary mapping method names to color styles.
                    Must use keys from COLORS dict.
                    Example: {'success': 'bright_green', 'error': 'bright_red'}
                    
        Example:
            >>> Log = DLogger(
            ...     icons={'success': 'OK', 'error': 'ERR'},
            ...     styles={'success': 'bright_green', 'error': 'bright_red'}
            ... )
            >>> # This creates Log.success() and Log.error() methods automatically
        """
        self.ICONS: Dict[str, str] = icons
        self._styles: Dict[str, str] = styles or {}
        self._generate_methods()
    
    def print(self, message: str, style: str = '', icon: str = '', end: str = '\n') -> None:
        """
        Core print method with styling and icon support.
        
        Args:
            message: The text message to print.
            style: Color style from COLORS dict (e.g., 'bright_green', 'red').
            icon: Icon text to display in brackets before the message.
            end: String appended after the message (default: newline).
            
        Example:
            >>> Log = DLogger(icons={})
            >>> Log.print("Hello", style='green', icon='MSG')
            [MSG] Hello
        """
        color = self.COLORS.get(style, '')
        icon_char = icon
        
        if icon_char:
            if color:
                print(f"{color}[{icon_char}]\033[0m {message}", end=end)
            else:
                print(f"[{icon_char}] {message}", end=end)
        else:
            if color:
                print(f"{color}{message}\033[0m", end=end)
            else:
                print(f"{message}", end=end)
        sys.stdout.flush()
    
    def header(self, text: str) -> None:
        """
        Print a header message in bright blue with extra spacing.
        
        Args:
            text: The header text to display.
            
        Example:
            >>> Log = DLogger(icons={})
            >>> Log.header("Application Started")
            Application Started
            
        """
        self.print(text, 'bright_blue', end='\n\n')
        sys.stdout.flush()
    
    def section(self, text: str) -> None:
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
        self.print(f" {text} ", 'bright_blue', end='')
        self.print("─" * (len(text) + 2), 'blue', end='\n\n')
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
        color = self.COLORS.get(style, '')
        
        if icon:
            if color:
                sys.stdout.write(f"\r{color}[{icon}]\033[0m {prefix} [{bar}] {percent}% {suffix}")
            else:
                sys.stdout.write(f"\r[{icon}] {prefix} [{bar}] {percent}% {suffix}")
        else:
            if color:
                sys.stdout.write(f"\r{color}{prefix} [{bar}] {percent}% {suffix}\033[0m")
            else:
                sys.stdout.write(f"\r{prefix} [{bar}] {percent}% {suffix}")
        sys.stdout.flush()

        if auto_clear and iteration >= total:
            sys.stdout.write('\n')
            sys.stdout.flush()
    
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
        for method_name, icon_text in self.ICONS.items():
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


if __name__ == "__main__":

    Log = DLogger(
        icons={
            'warning': 'WARN'
        },
        styles={
            'warning': 'bright_yellow'
        }
    )

    Log.warning("Please use this code as a module / library.")