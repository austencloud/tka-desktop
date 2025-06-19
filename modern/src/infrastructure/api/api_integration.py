"""
Integration layer to run API server alongside TKA Desktop.
"""

import asyncio
import threading
import logging
import socket
import subprocess
import psutil
import time
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def find_free_port(start_port: int = 8000, max_attempts: int = 100) -> int:
    """Find a free port starting from start_port."""
    # First try: let the system find a free port
    if start_port == 0:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", 0))  # Let system choose port
                return s.getsockname()[1]
        except Exception:
            pass

    # Second try: check ports sequentially
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                # Use 127.0.0.1 instead of 'localhost' to avoid DNS resolution issues
                s.bind(("127.0.0.1", port))
                return port
        except (OSError, socket.error):
            continue

    # Last resort: let system choose any port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
            logger.warning(f"Using system-assigned port {port}")
            return port
    except Exception:
        pass

    raise RuntimeError(f"Could not find free port after {max_attempts} attempts")


def is_port_in_use(host: str, port: int) -> bool:
    """Check if a port is already in use."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(1)
            # Convert localhost to 127.0.0.1 for consistency
            if host.lower() == "localhost":
                host = "127.0.0.1"
            result = s.connect_ex((host, port))
            return result == 0
    except Exception:
        return False


class TKAAPIIntegration:
    """Manages API server integration with TKA Desktop."""

    def __init__(self):
        self.api_thread: Optional[threading.Thread] = None
        self.should_stop = threading.Event()
        self._server_started = False
        self._actual_port: Optional[int] = None
        self._actual_host: Optional[str] = None
        self._server_instance = None

    def start_api_server(
        self, host: str = "localhost", port: int = 8000, auto_port: bool = True
    ):
        """Start API server in background thread."""
        if self._server_started:
            logger.warning("API server already started")
            return

        # Convert localhost to 127.0.0.1 for consistency on Windows
        if host.lower() == "localhost":
            host = "127.0.0.1"  # Find available port if requested port is in use
        actual_port = port
        if auto_port:
            try:
                # Test if we can bind to the requested port
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
                    test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    test_socket.bind((host, port))
                    # If we get here, port is available
                    actual_port = port
            except PermissionError as e:
                # Windows permission error - try alternative ports
                logger.warning(f"Permission denied for port {port}: {e}")
                logger.info(
                    "Trying alternative ports due to Windows permission restrictions..."
                )
                try:
                    # Try some common safe ports that usually don't require elevated permissions
                    safe_ports = [8080, 8888, 9000, 9090, 3000, 5000, 7000]
                    actual_port = None
                    for safe_port in safe_ports:
                        try:
                            with socket.socket(
                                socket.AF_INET, socket.SOCK_STREAM
                            ) as test_socket:
                                test_socket.setsockopt(
                                    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
                                )
                                test_socket.bind((host, safe_port))
                                actual_port = safe_port
                                logger.info(
                                    f"Using safe port {actual_port} instead of {port}"
                                )
                                break
                        except (OSError, PermissionError):
                            continue

                    if actual_port is None:
                        logger.error(
                            "Could not find any available port due to permission restrictions"
                        )
                        logger.info(
                            "Try running as administrator or check Windows Firewall/Antivirus settings"
                        )
                        return
                except Exception as fallback_error:
                    logger.error(f"Failed to find alternative port: {fallback_error}")
                    return
            except (OSError, socket.error):
                # Port is in use, find alternative
                try:
                    actual_port = find_free_port(port + 1)  # Start from next port
                    logger.info(f"Port {port} in use, using port {actual_port} instead")
                except RuntimeError as e:
                    # Check what's using the port
                    process_info = get_process_using_port(port)
                    if process_info:
                        pid, name = process_info
                        logger.error(
                            f"Port {port} is being used by {name} (PID: {pid})"
                        )
                        logger.info(f"You can kill it with: taskkill /PID {pid} /F")
                    else:
                        logger.error(f"Could not find free port: {e}")
                    return

        def run_server():
            try:
                # Import here to avoid circular imports and ensure dependencies are available
                import uvicorn
                from .minimal_api import app

                logger.info(
                    f"🌐 Starting TKA API server at http://{host}:{actual_port}"
                )

                # Create uvicorn config for better control
                config = uvicorn.Config(
                    app,
                    host=host,
                    port=actual_port,
                    log_level="warning",
                    access_log=False,
                    loop="asyncio",
                )

                server = uvicorn.Server(config)
                self._server_instance = server

                # Store actual connection details
                self._actual_host = host
                self._actual_port = actual_port

                # Run server with graceful shutdown support
                try:
                    # Use asyncio.run for better control
                    asyncio.run(self._run_with_shutdown(server))
                except KeyboardInterrupt:
                    logger.info("API server shutdown requested")
                except Exception as e:
                    if not self.should_stop.is_set():
                        logger.error(f"API server error: {e}")

            except ImportError as e:
                logger.error(f"API server dependencies not available: {e}")
                logger.error(
                    "Please install FastAPI and uvicorn: pip install fastapi uvicorn"
                )
            except PermissionError as e:
                logger.error(f"Permission denied starting API server: {e}")
                logger.info(
                    "Try running as administrator or check Windows Firewall/Antivirus settings"
                )
            except OSError as e:
                if "Address already in use" in str(e) or "10048" in str(e):
                    logger.error(
                        f"Port {actual_port} is still in use. Try a different port or kill the process using it."
                    )
                    if auto_port:
                        logger.info(
                            "You can also disable auto_port and manually specify a different port"
                        )
                else:
                    logger.error(f"Network error starting API server: {e}")
            except Exception as e:
                logger.error(f"API server failed: {e}")
            finally:
                self._server_started = False
                self._server_instance = None

        self.api_thread = threading.Thread(target=run_server, daemon=True)
        self.api_thread.start()
        self._server_started = True

        # Wait a moment to see if server starts successfully
        time.sleep(0.5)

        if self._server_started:
            logger.info(f"🌐 TKA API started at http://{host}:{actual_port}")
            logger.info(f"📚 API docs: http://{host}:{actual_port}/docs")

    async def _run_with_shutdown(self, server):
        """Run server with shutdown monitoring."""
        # Start server in background task
        server_task = asyncio.create_task(server.serve())

        # Monitor shutdown signal
        while not self.should_stop.is_set() and not server_task.done():
            await asyncio.sleep(0.1)

        if self.should_stop.is_set():
            # Graceful shutdown
            logger.info("Shutting down API server...")
            server.should_exit = True
            await server.shutdown()

        # Wait for server task to complete
        try:
            await server_task
        except asyncio.CancelledError:
            pass

    def stop_api_server(self):
        """Stop the API server gracefully."""
        if not self._server_started:
            logger.info("API server not running")
            return

        logger.info("Stopping API server...")
        self.should_stop.set()

        # Give server time to shutdown gracefully
        if self.api_thread and self.api_thread.is_alive():
            self.api_thread.join(timeout=5.0)

        self._server_started = False
        self._server_instance = None
        self._actual_port = None
        self._actual_host = None

        # Reset stop event for future use
        self.should_stop.clear()

        logger.info("API server stopped")

    def is_running(self) -> bool:
        """Check if the API server is running."""
        if not self._server_started or not self.api_thread:
            return False

        # Check thread is alive
        if not self.api_thread.is_alive():
            self._server_started = False
            return False

        # Optionally check if port is still bound (more reliable)
        if self._actual_host and self._actual_port:
            return is_port_in_use(self._actual_host, self._actual_port)

        return True

    def get_server_url(self) -> Optional[str]:
        """Get the actual server URL if running."""
        if self.is_running() and self._actual_host and self._actual_port:
            return f"http://{self._actual_host}:{self._actual_port}"
        return None

    def get_docs_url(self) -> Optional[str]:
        """Get the API documentation URL if running."""
        base_url = self.get_server_url()
        return f"{base_url}/docs" if base_url else None


# Global instance
_api_integration: Optional[TKAAPIIntegration] = None


def get_api_integration() -> TKAAPIIntegration:
    """Get the global API integration instance."""
    global _api_integration
    if _api_integration is None:
        _api_integration = TKAAPIIntegration()
    return _api_integration


def start_api_server(
    host: str = "localhost", port: int = 8000, auto_port: bool = True
) -> bool:
    """Convenience function to start the API server."""
    try:
        integration = get_api_integration()

        # Check if port is in use before starting
        if host.lower() == "localhost":
            host = "127.0.0.1"

        if not auto_port:
            process_info = get_process_using_port(port)
            if process_info:
                pid, name = process_info
                logger.error(
                    f"Cannot start API server: Port {port} is being used by {name} (PID: {pid})"
                )
                logger.info(f"Either kill the process with: taskkill /PID {pid} /F")
                logger.info(f"Or enable auto_port to find an alternative port")
                return False

        integration.start_api_server(host, port, auto_port)

        # Give it a moment to start
        time.sleep(1)
        return integration.is_running()

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


def get_api_url() -> Optional[str]:
    """Get the current API server URL."""
    try:
        integration = get_api_integration()
        return integration.get_server_url()
    except Exception:
        return None


def get_process_using_port(port: int) -> Optional[Tuple[int, str]]:
    """Get the process ID and name using a specific port."""
    try:
        for conn in psutil.net_connections():
            if (
                conn.laddr.port == port
                and conn.status == psutil.CONN_LISTEN
                and conn.pid is not None
            ):
                try:
                    process = psutil.Process(conn.pid)
                    return conn.pid, process.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        return None
    except Exception:
        return None


def kill_process_on_port(port: int) -> bool:
    """Kill any process using the specified port (Windows)."""
    try:
        # Find process using the port
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                try:
                    process = psutil.Process(conn.pid)
                    logger.info(
                        f"Killing process {process.name()} (PID: {conn.pid}) on port {port}"
                    )
                    process.terminate()
                    process.wait(timeout=5)
                    return True
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.TimeoutExpired,
                ):
                    continue
        return False
    except Exception as e:
        logger.error(f"Error killing process on port {port}: {e}")
        return False
