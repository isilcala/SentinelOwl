from fastapi import APIRouter, WebSocket
from typing import Dict, Any
import asyncio
from ..core.engine import SentinelOwl


class AIGuardPlugin:
    """Moonraker plugin for SentinelOwl"""

    def __init__(self, config):
        print("🦉 SentinelOwl plugin initialized!")  # 调试日志
        self.config = config
        self.router = APIRouter()
        self._setup_routes()
        self._clients = set()
        self.engine = SentinelOwl(config)

    def _setup_routes(self):
        """Register API and WebSocket routes"""
        self.router.add_api_route("/ai-guard/status", self.get_status, methods=["GET"])
        self.router.add_websocket_route("/ai-guard/ws", self.websocket_endpoint)

    async def get_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        return {
            "status": "active",
            "fps": self.engine.get_fps(),
            "confidence": self.engine.get_latest_confidence(),
            "defect_type": self.engine.get_latest_defect_type(),
        }

    async def websocket_endpoint(self, websocket: WebSocket):
        """WebSocket endpoint for real-time updates"""
        await websocket.accept()
        self._clients.add(websocket)
        try:
            while True:
                await asyncio.sleep(1)
                status = await self.get_status()
                await websocket.send_json(status)
        finally:
            self._clients.remove(websocket)

    async def notify_clients(self, message: Dict[str, Any]):
        """Notify all connected WebSocket clients"""
        for client in self._clients:
            await client.send_json(message)

    def load_plugin(config: Dict[str, Any]) -> AIGuardPlugin:
        """Entry point for Moonraker to load the plugin"""
        return AIGuardPlugin(config)
