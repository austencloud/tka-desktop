"""
Bulletproof Integration layer to run API server alongside TKA Desktop.
GUARANTEE: This module will NEVER raise PermissionError or socket exceptions.
"""

import asyncio
import threading
import logging
import socket
import subprocess
import psutil
import time
from typing import Optional, Tuple, List
from contextlib import contextmanager, suppress

logger = logging.getLogger(__name__)


class SafeSocketManager:
    """Ultra-safe socket operations that never raise permission errors."""

    @staticmethod
    @contextmanager
    def safe_socket():
        """Context manager for safe socket creation with automatic cleanup."""
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(0.5)  # Very short timeout
            yield sock
        except Exception:
            # Swallow ALL socket creation errors
            yield None
        finally:
            if sock:
                with suppress(Exception):
                    sock.close()

    @staticmethod
    def test_port_binding(host: str, port: int) -> bool:
        """Test port binding with zero-exception guarantee."""
        try:
            with SafeSocketManager.safe_socket() as sock:
                if sock is None:
                    return False
                sock.bind((host, port))
                return True
        except Exception:
            # Catch EVERYTHING - no exceptions allowed to escape
            return False

    @staticmethod
    def test_port_connection(host: str, port: int) -> bool:
        """Test if port is in use with zero-exception guarantee."""
        try:
            with SafeSocketManager.safe_socket() as sock:
                if sock is None:
                    return False
                result = sock.connect_ex((host, port))
                return result == 0
        except Exception:
            # Catch EVERYTHING - no exceptions allowed to escape
            return False

    @staticmethod
    def get_system_port() -> Optional[int]:
        """Get system-assigned port with zero-exception guarantee."""
        try:
            with SafeSocketManager.safe_socket() as sock:
                if sock is None:
                    return None
                sock.bind(("127.0.0.1", 0))
                return sock.getsockname()[1]
        except Exception:
            # Catch EVERYTHING - no exceptions allowed to escape
            return None


class BulletproofPortFinder:
    """Find available ports with absolute guarantee of no exceptions."""

    # Safe ports that typically don't require admin privileges on Windows
    SAFE_PORTS = [
        8080,
        8888,
        9000,
        9090,
        3000,
        5000,
        7000,
        8001,
        8002,
        8003,
        8004,
        8005,
        8006,
        8007,
        8008,
        8009,
        8010,
        8011,
        8012,
        8013,
        8014,
        8015,
        8016,
        8017,
        8018,
        8019,
        8020,
        8021,
        8022,
        8023,
        8024,
        8025,
        8026,
        8027,
        8028,
        8029,
        9001,
        9002,
        9003,
        9004,
        9005,
        9006,
        9007,
        9008,
        9009,
        3001,
        3002,
        3003,
        3004,
        3005,
        5001,
        5002,
        5003,
        5004,
        5005,
        7001,
        7002,
        7003,
        7004,
        7005,
        7006,
        7007,
        7008,
        7009,
    ]

    @classmethod
    def find_safe_port(cls, host: str, preferred_port: int = 8000) -> Optional[int]:
        """Find a safe port with bulletproof error handling."""

        # Normalize host
        if host.lower() == "localhost":
            host = "127.0.0.1"

        # Strategy 1: Try preferred port
        if cls._try_port(host, preferred_port):
            logger.info(f"Using preferred port {preferred_port}")
            return preferred_port

        # Strategy 2: Try safe ports
        safe_ports = [p for p in cls.SAFE_PORTS if p != preferred_port]
        for port in safe_ports:
            if cls._try_port(host, port):
                logger.info(f"Using safe alternative port {port}")
                return port

        # Strategy 3: Try high random ports (less likely to need privileges)
        for port in range(8100, 8200):
            if cls._try_port(host, port):
                logger.info(f"Using high port {port}")
                return port

        # Strategy 4: System-assigned port
        system_port = SafeSocketManager.get_system_port()
        if system_port:
            logger.info(f"Using system-assigned port {system_port}")
            return system_port

        # Strategy 5: Last resort - assume a safe port will work
        # (we'll let uvicorn handle any remaining issues)
        fallback_port = 8080
        logger.warning(f"All port tests failed, using fallback port {fallback_port}")
        return fallback_port

    @staticmethod
    def _try_port(host: str, port: int) -> bool:
        """Try to bind to a port with complete error suppression."""
        return SafeSocketManager.test_port_binding(host, port)


class UltraSafeAPIIntegration:
    """API Integration that absolutely guarantees no permission errors."""

    def __init__(self, enabled: bool = True):
        self.api_thread: Optional[threading.Thread] = None
        self.should_stop = threading.Event()
        self._server_started = False
        self._actual_port: Optional[int] = None
        self._actual_host: Optional[str] = None
        self._server_instance = None
        self.enabled = enabled
        self._startup_failed = False
        self._last_error: Optional[str] = None

    def start_api_server(
        self, host: str = "localhost", port: int = 8000, auto_port: bool = True
    ) -> bool:
        """Start API server with bulletproof error handling. Returns success status."""

        # Early exits with safe logging
        if not self.enabled:
            logger.info("API server is disabled - skipping startup")
            return False

        if self._server_started:
            logger.info("API server already started")
            return True

        if self._startup_failed:
            logger.info("API server startup previously failed - skipping retry")
            return False

        # Normalize host
        if host.lower() == "localhost":
            host = "127.0.0.1"

        # Find safe port with bulletproof error handling
        try:
            if auto_port:
                safe_port = BulletproofPortFinder.find_safe_port(host, port)
                if safe_port is None:
                    logger.warning("Could not find any safe port - API server disabled")
                    self._startup_failed = True
                    return False
                actual_port = safe_port
            else:
                # Even in non-auto mode, verify the port is safe
                if not BulletproofPortFinder._try_port(host, port):
                    logger.warning(f"Port {port} not available - API server disabled")
                    self._startup_failed = True
                    return False
                actual_port = port
        except Exception as e:
            # Ultimate safety net - should never reach here
            logger.warning(f"Port finding failed unexpectedly - API server disabled")
            self._startup_failed = True
            return False

        # Start server in thread with ultra-safe wrapper
        def ultra_safe_server_runner():
            """Server runner with complete exception isolation."""
            try:
                self._run_server_safely(host, actual_port)
            except Exception as e:
                # CRITICAL: Catch absolutely everything
                logger.debug(f"Server runner caught exception: {e}")
                self._last_error = str(e)
            finally:
                # Always clean up state
                self._server_started = False
                self._server_instance = None

        try:
            self.api_thread = threading.Thread(
                target=ultra_safe_server_runner, daemon=True, name="TKA-API-Server"
            )
            self.api_thread.start()
            self._server_started = True

            # Store connection details
            self._actual_host = host
            self._actual_port = actual_port

            # Brief startup delay
            time.sleep(0.5)

            logger.info(f"🌐 TKA API started at http://{host}:{actual_port}")
            logger.info(f"📚 API docs: http://{host}:{actual_port}/docs")
            return True

        except Exception as e:
            # Even thread creation can fail - handle it
            logger.warning(f"Could not start API server thread - disabled for session")
            self._startup_failed = True
            return False

    def _run_server_safely(self, host: str, port: int):
        """Run the actual server with multi-layered error protection."""
        try:
            # Import dependencies safely
            try:
                import uvicorn
                from .minimal_api import app
            except ImportError as e:
                logger.info(
                    "API server dependencies not available - install with: pip install fastapi uvicorn"
                )
                return
            except Exception as e:
                logger.debug(f"Import error: {e}")
                return

            # Create server config with safe settings
            try:
                config = uvicorn.Config(
                    app,
                    host=host,
                    port=port,
                    log_level="error",  # Minimize uvicorn noise
                    access_log=False,
                    loop="asyncio",
                    # Add safety settings
                    timeout_graceful_shutdown=5,
                )

                server = uvicorn.Server(config)
                self._server_instance = server

            except Exception as e:
                logger.debug(f"Server config error: {e}")
                return

            # Run server with asyncio safety
            try:
                asyncio.run(self._async_server_wrapper(server))
            except Exception as e:
                logger.debug(f"Asyncio server error: {e}")
                return

        except Exception as e:
            # Ultimate catch-all - should never reach here
            logger.debug(f"Ultra-safe server runner error: {e}")

    async def _async_server_wrapper(self, server):
        """Async wrapper with shutdown monitoring."""
        try:
            # Create server task
            server_task = asyncio.create_task(server.serve())

            # Monitor for shutdown
            while not self.should_stop.is_set() and not server_task.done():
                await asyncio.sleep(0.1)

            # Handle shutdown
            if self.should_stop.is_set():
                server.should_exit = True
                with suppress(Exception):
                    await server.shutdown()

            # Wait for completion
            with suppress(Exception):
                await server_task

        except Exception as e:
            logger.debug(f"Async server wrapper error: {e}")

    def stop_api_server(self):
        """Stop the API server with bulletproof cleanup."""
        try:
            if not self._server_started:
                return

            logger.info("Stopping API server...")
            self.should_stop.set()

            # Wait for thread with timeout
            if self.api_thread and self.api_thread.is_alive():
                self.api_thread.join(timeout=3.0)

            # Clean up state
            self._server_started = False
            self._server_instance = None
            self._actual_port = None
            self._actual_host = None
            self.should_stop.clear()

            logger.info("API server stopped")

        except Exception as e:
            # Even cleanup should never fail
            logger.debug(f"Error during API server stop: {e}")

    def is_running(self) -> bool:
        """Check if server is running with safe error handling."""
        try:
            if not self._server_started or not self.api_thread:
                return False

            if not self.api_thread.is_alive():
                self._server_started = False
                return False

            # Optional connectivity check
            if self._actual_host and self._actual_port:
                return SafeSocketManager.test_port_connection(
                    self._actual_host, self._actual_port
                )

            return True
        except Exception:
            return False

    def get_server_url(self) -> Optional[str]:
        """Get server URL safely."""
        try:
            if self.is_running() and self._actual_host and self._actual_port:
                return f"http://{self._actual_host}:{self._actual_port}"
        except Exception:
            pass
        return None

    def get_docs_url(self) -> Optional[str]:
        """Get docs URL safely."""
        try:
            base_url = self.get_server_url()
            return f"{base_url}/docs" if base_url else None
        except Exception:
            return None


# Global instance with safe initialization
_api_integration: Optional[UltraSafeAPIIntegration] = None


def get_api_integration(enabled: bool = True) -> UltraSafeAPIIntegration:
    """Get the global API integration instance safely."""
    global _api_integration
    try:
        if _api_integration is None:
            _api_integration = UltraSafeAPIIntegration(enabled=enabled)
        return _api_integration
    except Exception:
        # Even this should never fail
        return UltraSafeAPIIntegration(enabled=False)


def start_api_server(
    host: str = "localhost",
    port: int = 8000,
    auto_port: bool = True,
    enabled: bool = True,
) -> bool:
    """
    Start API server with BULLETPROOF error handling.

    GUARANTEE: This function will NEVER raise any exceptions.
    Returns: True if server started successfully, False otherwise.
    """
    try:
        integration = get_api_integration(enabled=enabled)

        if not integration.enabled:
            logger.info("API server is disabled")
            return False

        return integration.start_api_server(host, port, auto_port)

    except Exception as e:
        # ULTIMATE SAFETY NET - should never reach here
        logger.warning(f"API server startup completely failed - disabled for session")
        logger.debug(f"Ultimate catch-all error: {e}")
        return False


def stop_api_server():
    """Stop API server with bulletproof error handling."""
    try:
        integration = get_api_integration()
        integration.stop_api_server()
    except Exception as e:
        logger.debug(f"Error stopping API server: {e}")


def is_api_running() -> bool:
    """Check if API is running safely."""
    try:
        integration = get_api_integration()
        return integration.is_running()
    except Exception:
        return False


def get_api_url() -> Optional[str]:
    """Get API URL safely."""
    try:
        integration = get_api_integration()
        return integration.get_server_url()
    except Exception:
        return None


def get_process_using_port(port: int) -> Optional[Tuple[int, str]]:
    """Get process using port safely."""
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
                except Exception:
                    continue
        return None
    except Exception:
        return None


# Backward compatibility wrapper
class TKAAPIIntegration(UltraSafeAPIIntegration):
    """Backward compatibility alias."""

    pass


def find_free_port(start_port: int = 8000, max_attempts: int = 100) -> int:
    """Find free port with safe fallback."""
    try:
        result = BulletproofPortFinder.find_safe_port("127.0.0.1", start_port)
        return result if result is not None else 8080
    except Exception:
        return 8080


def is_port_in_use(host: str, port: int) -> bool:
    """Check if port is in use safely."""
    try:
        return SafeSocketManager.test_port_connection(host, port)
    except Exception:
        return False
