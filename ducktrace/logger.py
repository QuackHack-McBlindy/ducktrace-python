import os
import sys
import time
import logging
from datetime import datetime
from typing import Optional, Callable, Any

class DuckTraceFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[34m',        # 🦆 says ⮞ BLUE
        'INFO': '\033[0;32m',       # 🦆 says ⮞ GREEN
        'WARNING': '\033[33m',      # 🦆 says ⮞ YELLOW
        'ERROR': '\033[1;31m',      # 🦆 says ⮞ RED
        'CRITICAL': '\033[1;5;31m', # 🦆 says ⮞ BLINKY RED
        'RESET': '\033[0m',
        'BOLD': '\033[1m',
        'BLINK': '\033[5m',
        'DSAY': '\033[3m\033[38;2;0;150;150m',
        'GRAY': '\033[38;5;244m'
    }

    SYMBOLS = {
        'DEBUG': '⁉️',
        'INFO': '✅',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🚨'
    }

    def format(self, record):
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = self.COLORS.get(record.levelname, self.COLORS['INFO'])
        symbol = self.SYMBOLS.get(record.levelname, "")
        blink = self.COLORS['BLINK'] if record.levelname in ['ERROR', 'CRITICAL'] else ""

        message = super().format(record)
        formatted = (
            f"{color}{self.COLORS['BOLD']}{blink}[🦆📜] [{timestamp}] "
            f"{symbol}{record.levelname}{symbol} ⮞ {message}{self.COLORS['RESET']}"
        )

        if record.levelname in ['ERROR', 'CRITICAL']:
            formatted += (
                f"\n{self.COLORS['DSAY']}🦆 duck say {self.COLORS['BOLD']}"
                f"\033[38;2;255;255;0m⮞{self.COLORS['RESET']}{self.COLORS['DSAY']} "
                f"fuck ❌ {message}{self.COLORS['RESET']}"
            )

        return formatted


def setup_ducktrace_logging(name: Optional[str] = None,
                            level: Optional[str] = None) -> logging.Logger:
    """
    Configure the ducktrace logger.

    Args:
        name: Base name of the log file (without path). Defaults to env DT_LOG_FILE or 'PyDuckTrace.log'.
        level: Log level as string. Overrides DT_LOG_LEVEL env var.

    Returns:
        The root logger instance.
    """
    if level is None:
        env_level = os.environ.get('DT_LOG_LEVEL', 'INFO').upper()
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL,
        }
        log_level = level_map.get(env_level, logging.INFO)
    else:
        log_level = getattr(logging, level.upper(), logging.INFO)

    log_path = os.environ.get('DT_LOG_PATH', os.path.expanduser('~/.config/duckTrace/'))
    os.makedirs(log_path, exist_ok=True)

    if name is None:
        name = os.environ.get('DT_LOG_FILE', 'PyDuckTrace.log')

    log_file = os.path.join(log_path, name)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stderr)
    console_formatter = DuckTraceFormatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


def dt_debug(msg: str) -> None:
    logging.debug(msg)

def dt_info(msg: str) -> None:
    logging.info(msg)

def dt_warning(msg: str) -> None:
    logging.warning(msg)

def dt_error(msg: str) -> None:
    logging.error(msg)

def dt_critical(msg: str) -> None:
    logging.critical(msg)


def dt_timer(func_name: Optional[str] = None) -> Callable:
    """
    Decorator to measure and log execution time of a function.
    Logs at DEBUG level.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            logger = logging.getLogger()
            start_time = time.time()
            actual_name = func_name or func.__name__
            logger.debug(f"Starting {actual_name}...")
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.debug(f"Completed {actual_name} in {elapsed:.3f}s")
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"Failed {actual_name} after {elapsed:.3f}s: {str(e)}")
                raise
        return wrapper
    return decorator


class TranscriptionTimer:
    """
    A context manager for timing blocks of code.
    Usage:
        with TranscriptionTimer("my operation") as timer:
            ... do work ...
            timer.lap("first part")
    """
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time: Optional[float] = None
        self.logger = logging.getLogger()

    def __enter__(self):
        self.start_time = time.time()
        self.logger.debug(f"Starting {self.operation_name}...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        if exc_type is None:
            self.logger.debug(f"Completed {self.operation_name} in {elapsed:.3f}s")
        else:
            self.logger.error(f"Failed {self.operation_name} after {elapsed:.3f}s")

    def lap(self, lap_name: str) -> None:
        """Record a checkpoint within the timed operation."""
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.logger.debug(f"{self.operation_name} - {lap_name}: {elapsed:.3f}s")
