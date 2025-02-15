import click
from sentinelowl.config import AppConfig  # 改为绝对导入
from sentinelowl.core.engine import SentinelOwl  # 改为绝对导入


@click.group()
def cli():
    """SentinelOwl - Your 3D Printing Guardian"""
    pass

@cli.command()
@click.option("--camera-url", default="http://localhost:8080/?action=stream",
              help="URL of the camera stream (MJPEG or RTSP)")
@click.option("--interval", default=5, type=int,
              help="Detection interval in seconds")
@click.option("--warning-threshold", default=0.7, type=float,
              help="Confidence threshold for warnings (0.0 to 1.0)")
@click.option("--critical-threshold", default=0.85, type=float,
              help="Confidence threshold for critical alerts (0.0 to 1.0)")
def start(camera_url, interval, warning_threshold, critical_threshold):
    """Start the SentinelOwl monitoring service"""
    config = AppConfig(
        camera={"url": camera_url},
        detection={
            "interval": interval,
            "warning_threshold": warning_threshold,
            "critical_threshold": critical_threshold,
        }
    )

    owl = SentinelOwl(config)
    print("🦉 Starting SentinelOwl...")
    try:
        owl.run()
    except KeyboardInterrupt:
        print("\n🦉 SentinelOwl stopped.")

@cli.command()
def version():
    """Show the version of SentinelOwl"""
    from sentinelowl import __version__
    print(f"SentinelOwl version: {__version__}")

if __name__ == "__main__":
    cli()