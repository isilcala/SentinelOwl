import click
from sentinelowl.config import AppConfig  # 改为绝对导入
from sentinelowl.core.engine import SentinelOwl  # 改为绝对导入
import asyncio

@click.group()
def cli():
    """SentinelOwl - Your 3D Printing Guardian"""
    pass

@cli.command()
@click.option("--camera-url", default="http://localhost:8080/?action=stream",
              help="URL of the camera stream (MJPEG or RTSP)")
@click.option("--interval", default=5, type=int,
              help="Detection interval in seconds")
def start(camera_url, interval):
    """Start the SentinelOwl monitoring service"""
    config = AppConfig(
        camera={"url": camera_url},
        detection={"interval": interval}
    )

    owl = SentinelOwl(config)
    print("🦉 Starting SentinelOwl...")
    try:
        asyncio.run(owl.run())
    except KeyboardInterrupt:
        print("\n🦉 SentinelOwl stopped.")

@cli.command()
def version():
    """Show the version of SentinelOwl"""
    from sentinelowl import __version__
    print(f"SentinelOwl version: {__version__}")

if __name__ == "__main__":
    cli()