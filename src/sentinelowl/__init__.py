from .core.engine import SentinelOwl
from .config import AppConfig
from .cli import cli

__version__ = "0.1.0"
__all__ = ["SentinelOwl", "AppConfig"]


def main():
    """Entry point for the SentinelOwl CLI"""
    cli()


if __name__ == "__main__":
    main()
