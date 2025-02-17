from moonraker import MoonrakerAPI


class PrinterController:
    """Wrapper for printer control commands"""

    def __init__(self, host="localhost", port=7125):
        self.api = MoonrakerAPI(f"http://{host}:{port}")

    def pause_print(self):
        """Pause current print job"""
        return self.api.send_gcode("PAUSE")

    def resume_print(self):
        """Resume paused print job"""
        return self.api.send_gcode("RESUME")

    def get_print_status(self) -> Dict[str, Any]:
        """Get current print status"""
        return self.api.get("printer/objects/query?print_stats")
