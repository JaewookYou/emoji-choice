#!/usr/bin/env python3
"""
Unified logging utility for OpenClaw scripts and skills.
Usage:
    from lib.logger import get_logger
    logger = get_logger("script-name")
    logger.info("message")
    logger.error("error message")

Logs to: ~/.openclaw/workspace/logs/<script-name>/<date>.log
Also prints to stdout.
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

LOGS_DIR = Path.home() / ".openclaw" / "workspace" / "logs"


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Create a logger that writes to both file and stdout.
    
    Args:
        name: Script/skill name (used for log subdirectory)
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    # Create log directory
    log_dir = LOGS_DIR / name
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Log file with date
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"{date_str}.log"
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Format: [2026-02-01 22:59:30] INFO: message
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # File handler (append mode)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(level)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    
    return logger


def log_exception(logger: logging.Logger, e: Exception, context: str = ""):
    """Log exception with traceback."""
    import traceback
    msg = f"{context}: {e}" if context else str(e)
    logger.error(msg)
    logger.debug(traceback.format_exc())


# Convenience: run script with automatic logging
if __name__ == "__main__":
    # Test
    logger = get_logger("test")
    logger.info("Logger initialized")
    logger.warning("This is a warning")
    logger.error("This is an error")
    print(f"\nLog file: {LOGS_DIR}/test/{datetime.now().strftime('%Y-%m-%d')}.log")
