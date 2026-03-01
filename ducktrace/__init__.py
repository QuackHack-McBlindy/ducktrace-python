"""
ducktrace – a duck‑themed logging system for Python.
"""

from .logger import (
    dt_setup,
    dt_debug,
    dt_info,
    dt_warning,
    dt_error,
    dt_critical,
    dt_timer,
    TranscriptionTimer,
)

__all__ = [
    "dt_setup",
    "dt_debug",
    "dt_info",
    "dt_warning",
    "dt_error",
    "dt_critical",
    "dt_timer",
    "TranscriptionTimer",
]
