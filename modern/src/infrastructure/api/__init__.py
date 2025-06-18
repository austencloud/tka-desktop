"""
TKA Desktop API Infrastructure

Provides multi-language access to TKA functionality through:
- REST API for CRUD operations
- WebSocket API for real-time events
- Auto-generated client libraries
- Production-grade fault tolerance
"""

# Minimal API exports for Phase 1
try:
    from .minimal_api import app as minimal_app
    from .api_integration import (
        TKAAPIIntegration,
        get_api_integration,
        start_api_server,
        stop_api_server,
        is_api_running,
    )

    __all__ = [
        "minimal_app",
        "TKAAPIIntegration",
        "get_api_integration",
        "start_api_server",
        "stop_api_server",
        "is_api_running",
    ]
except ImportError:
    # Dependencies not available
    __all__ = []

# Future exports for later phases
# from .rest_api import app as rest_app
# from .websocket_api import WebSocketConnectionManager, websocket_endpoint
# from .api_models import *
# from .fault_tolerance import CircuitBreaker, RetryPolicy, HealthChecker
# from .client_generator import ClientGenerator
# from .api_server import TKAAPIServer
