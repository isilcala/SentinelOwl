import click
from sentinelowl.config import AppConfig  # 改为绝对导入
from sentinelowl.core.engine import SentinelOwl  # 改为绝对导入
import asyncio


@click.group()
def cli():
    """SentinelOwl - Your 3D Printing Guardian"""
    pass


@cli.command()
@click.option(
    "--camera-url",
    default="http://localhost:8080/?action=stream",
    help="URL of the camera stream (MJPEG or RTSP)",
)
@click.option("--interval", default=5, type=int, help="Detection interval in seconds")
def start(camera_url, interval):
    """Start the SentinelOwl monitoring service"""
    config = AppConfig(camera={"url": camera_url}, detection={"interval": interval})

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


@cli.command()
@click.option("--camera-url", required=True, help="URL of the camera stream")
@click.option("--model-path", required=True, help="Path to the ONNX model")
def validate(camera_url, model_path):
    """Validate camera and model integration"""
    from sentinelowl.scripts.validate import main  # 修改为从 sentinelowl.scripts 导入

    main(camera_url, model_path)


if __name__ == "__main__":
    cli()
