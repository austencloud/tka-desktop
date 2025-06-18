"""
Integration layer to run API server alongside TKA Desktop.
"""

import asyncio
import threading
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TKAAPIIntegration:
    """Manages API server integration with TKA Desktop."""
    
    def __init__(self):
        self.api_thread: Optional[threading.Thread] = None
        self.should_stop = False
        self._server_started = False

    def start_api_server(self, host: str = "localhost", port: int = 8000):
        """Start API server in background thread."""
        if self._server_started:
            logger.warning("API server already started")
            return
            
        def run_server():
            try:
                # Import here to avoid circular imports and ensure dependencies are available
                import uvicorn
                from .minimal_api import app
                
                logger.info(f"🌐 Starting TKA API server at http://{host}:{port}")
                uvicorn.run(
                    app, 
                    host=host, 
                    port=port, 
                    log_level="warning",
                    access_log=False  # Reduce noise in logs
                )
            except ImportError as e:
                logger.error(f"API server dependencies not available: {e}")
                logger.error("Please install FastAPI and uvicorn: pip install fastapi uvicorn")
            except Exception as e:
                logger.error(f"API server failed: {e}")

        self.api_thread = threading.Thread(target=run_server, daemon=True)
        self.api_thread.start()
        self._server_started = True
        
        logger.info(f"🌐 TKA API started at http://{host}:{port}")
        logger.info(f"📚 API docs: http://{host}:{port}/docs")

    def stop_api_server(self):
        """Stop the API server."""
        self.should_stop = True
        self._server_started = False
        # Note: uvicorn doesn't have a clean shutdown mechanism when run this way
        # For production, you'd want a more sophisticated approach

    def is_running(self) -> bool:
        """Check if the API server is running."""
        return self._server_started and self.api_thread and self.api_thread.is_alive()


# Global instance
_api_integration: Optional[TKAAPIIntegration] = None


def get_api_integration() -> TKAAPIIntegration:
    """Get the global API integration instance."""
    global _api_integration
    if _api_integration is None:
        _api_integration = TKAAPIIntegration()
    return _api_integration


def start_api_server(host: str = "localhost", port: int = 8000) -> bool:
    """Convenience function to start the API server."""
    try:
        integration = get_api_integration()
        integration.start_api_server(host, port)
        return True
    except Exception as e:
        logger.error(f"Failed to start API server: {e}")
        return False


def stop_api_server():
    """Convenience function to stop the API server."""
    try:
        integration = get_api_integration()
        integration.stop_api_server()
    except Exception as e:
        logger.error(f"Failed to stop API server: {e}")


def is_api_running() -> bool:
    """Check if the API server is running."""
    try:
        integration = get_api_integration()
        return integration.is_running()
    except Exception:
        return False
