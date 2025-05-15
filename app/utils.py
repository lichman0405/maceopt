# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/utils.py
# This file contains utility functions and classes for logging and other common tasks.
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from rich.console import Console
from rich.traceback import install

install(show_locals=True)


class RichLogger:
    def __init__(self):
        self.console = Console()

    def info(self, message: str):
        self.console.print(f"[cyan][INFO] {message}[/]")

    def success(self, message: str):
        self.console.print(f"[green][SUCCESS] {message}[/]")

    def error(self, message: str):
        self.console.print(f"[bold red][ERROR] {message}[/]")

    def warning(self, message: str):
        self.console.print(f"[yellow][WARNING] {message}[/]")

    def rule(self, message: str):
        self.console.rule(message)

    def print(self, *args, **kwargs):
        self.console.print(*args, **kwargs)


# 全局统一日志器
logger = RichLogger()
