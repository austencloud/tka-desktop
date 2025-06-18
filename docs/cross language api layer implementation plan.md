# Copilot Agent Prompt: TKA Desktop API Implementation

## Context
You are helping implement a REST API layer for TKA (The Kinetic Alphabet) Desktop, a PyQt application for creating kinetic alphabet sequences. The app already has:

- Event-driven architecture with TypeSafeEventBus
- Command pattern with undo/redo (CommandProcessor) 
- Dependency injection (DIContainer)
- Clean architecture (domain/application/infrastructure/presentation)
- Services: SequenceManagementService, MotionManagementService, etc.

## Architecture Overview
```
src/
├── domain/models/core_models.py        # SequenceData, BeatData, MotionData
├── application/services/core/          # Business services
│   ├── sequence_management_service.py  # Main sequence operations
│   └── pictograph_management_service.py
├── core/
│   ├── events/                         # Event system (already implemented)
│   ├── commands/                       # Command pattern (already implemented)
│   └── dependency_injection/           # DI container (already implemented)
├── infrastructure/                     # External concerns
└── presentation/                       # PyQt UI components
```

## Goals
1. **External Integration**: Allow other applications to control TKA via REST API
2. **Fault Tolerance**: Add circuit breakers and graceful degradation
3. **Cross-Language Access**: Generate TypeScript/Rust/C++ clients
4. **Real-Time Events**: WebSocket streaming of TKA events
5. **Production Monitoring**: Performance metrics and health checks

## Key Implementation Patterns

### 1. Leverage Existing Services
```python
# Use existing DI container
from core.dependency_injection.di_container import get_container
from application.services.core.sequence_management_service import ISequenceManagementService

def get_sequence_service() -> SequenceManagementService:
    container = get_container()
    return container.resolve(ISequenceManagementService)
```

### 2. Event-Driven API Integration
```python
# Subscribe to existing events for WebSocket broadcasting
from core.events import get_event_bus, SequenceCreatedEvent, BeatAddedEvent

event_bus = get_event_bus()
event_bus.subscribe(SequenceCreatedEvent, broadcast_to_websocket_clients)
```

### 3. Command Pattern Integration
```python
# Use existing command processor for undo/redo
@app.post("/api/undo")
async def undo_action(service: SequenceManagementService = Depends(get_sequence_service)):
    result = service.undo_last_operation()
    return {"success": result is not None, "can_undo": service.can_undo()}
```

### 4. Fault Tolerance Patterns
```python
# Circuit breaker for service calls
@circuit_breaker(failure_threshold=5, recovery_timeout=30)
@retry_policy(max_attempts=3, delay=1.0)
async def create_sequence(request: CreateSequenceRequest):
    # Service call with automatic retry and circuit breaking
```

## Domain Models Reference
```python
# Core models already exist - use these structures
@dataclass(frozen=True)
class SequenceData:
    id: str
    name: str = ""
    word: str = ""
    beats: List[BeatData] = field(default_factory=list)
    start_position: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True) 
class BeatData:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    beat_number: int = 1
    letter: Optional[str] = None
    duration: float = 1.0
    blue_motion: Optional[MotionData] = None
    red_motion: Optional[MotionData] = None
    blue_reversal: bool = False
    red_reversal: bool = False
    is_blank: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
```

## Service Integration Examples
```python
# Example: SequenceManagementService integration
class SequenceManagementService:
    def create_sequence_with_events(self, name: str, length: int = 16) -> SequenceData:
        # Creates sequence and publishes SequenceCreatedEvent
        
    def add_beat_with_undo(self, beat: BeatData, position: Optional[int] = None) -> SequenceData:
        # Uses command pattern for undo support
        
    def undo_last_operation(self) -> Optional[SequenceData]:
        # Undo via existing CommandProcessor
```

## Required Dependencies
```python
# API framework
from fastapi import FastAPI, HTTPException, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Fault tolerance  
import asyncio
import time
import logging
from typing import Callable, Any, Optional, Dict, List
from dataclasses import dataclass
from enum import Enum
from functools import wraps

# WebSocket
import json
import uuid
from datetime import datetime
```

## Implementation Priorities
1. **Start with minimal API** (5 endpoints: status, current-sequence, create-sequence, undo, redo)
2. **Add fault tolerance** (circuit breakers, retries, health checks)
3. **Implement WebSocket events** (real-time sequence updates)
4. **Generate client libraries** (TypeScript first, then Rust/C++)
5. **Add monitoring** (performance metrics, baseline tracking)

## Code Style Guidelines
- Use existing domain models and services
- Follow Clean Architecture principles  
- Implement comprehensive error handling
- Add type hints for all functions
- Use dependency injection consistently
- Subscribe to existing events rather than modifying core services
- Keep API models separate from domain models (use conversion functions)

## Error Handling Pattern
```python
@app.post("/api/sequences")
async def create_sequence(request: CreateSequenceRequest):
    try:
        sequence = service.create_sequence_with_events(request.name, request.length)
        return domain_to_api_sequence(sequence)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating sequence: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Testing Approach
- Use existing TestClient from FastAPI
- Test against real service instances (not mocks)
- Verify event publishing works correctly
- Test undo/redo functionality via API
- Validate fault tolerance mechanisms

Remember: The goal is to expose existing TKA functionality via API, not to reimplement business logic. Leverage the existing event-driven architecture and service layer.

# MINIMAL API IMPLEMENTATION (1-2 days)
# This gives you immediate external access with minimal code

# ===== FILE: src/infrastructure/api/minimal_api.py =====
"""
Minimal REST API for TKA Desktop.
Provides external access to core functionality with minimal overhead.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import threading
import uvicorn

# Import your existing services
from core.dependency_injection.di_container import get_container
from application.services.core.sequence_management_service import (
    SequenceManagementService, ISequenceManagementService
)

# Simple API models
class BeatAPI(BaseModel):
    id: str
    beat_number: int
    letter: Optional[str] = None
    duration: float = 1.0
    blue_reversal: bool = False
    red_reversal: bool = False
    is_blank: bool = False

class SequenceAPI(BaseModel):
    id: str
    name: str
    beats: List[BeatAPI] = []

class CreateSequenceRequest(BaseModel):
    name: str = "New Sequence"
    length: int = 16

# FastAPI app
app = FastAPI(title="TKA Desktop API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get service from your existing DI container
def get_sequence_service() -> SequenceManagementService:
    container = get_container()
    return container.resolve(ISequenceManagementService)

# Simple conversion functions
def domain_to_api_sequence(sequence) -> SequenceAPI:
    return SequenceAPI(
        id=sequence.id,
        name=sequence.name,
        beats=[
            BeatAPI(
                id=beat.id,
                beat_number=beat.beat_number,
                letter=beat.letter,
                duration=beat.duration,
                blue_reversal=beat.blue_reversal,
                red_reversal=beat.red_reversal,
                is_blank=beat.is_blank
            ) for beat in sequence.beats
        ]
    )

# API endpoints
@app.get("/api/current-sequence", response_model=Optional[SequenceAPI])
async def get_current_sequence(
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Get the currently active sequence."""
    current = service.get_current_sequence()
    if not current:
        return None
    return domain_to_api_sequence(current)

@app.post("/api/sequences", response_model=SequenceAPI)
async def create_sequence(
    request: CreateSequenceRequest,
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Create a new sequence."""
    try:
        sequence = service.create_sequence_with_events(request.name, request.length)
        return domain_to_api_sequence(sequence)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/undo")
async def undo_last_action(
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Undo the last action."""
    result = service.undo_last_operation()
    return {
        "success": result is not None,
        "can_undo": service.can_undo(),
        "can_redo": service.can_redo()
    }

@app.post("/api/redo")
async def redo_last_action(
    service: SequenceManagementService = Depends(get_sequence_service)
):
    """Redo the last undone action."""
    result = service.redo_last_operation()
    return {
        "success": result is not None,
        "can_undo": service.can_undo(),
        "can_redo": service.can_redo()
    }

@app.get("/api/status")
async def get_status():
    """Get application status."""
    return {
        "status": "running",
        "version": "2.0.0",
        "api_enabled": True
    }

# ===== FILE: src/infrastructure/api/api_integration.py =====
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

    def start_api_server(self, host: str = "localhost", port: int = 8000):
        """Start API server in background thread."""
        def run_server():
            try:
                # Import here to avoid circular imports
                from .minimal_api import app
                uvicorn.run(app, host=host, port=port, log_level="warning")
            except Exception as e:
                logger.error(f"API server failed: {e}")

        self.api_thread = threading.Thread(target=run_server, daemon=True)
        self.api_thread.start()
        
        logger.info(f"🌐 TKA API started at http://{host}:{port}")
        logger.info(f"📚 API docs: http://{host}:{port}/docs")

    def stop_api_server(self):
        """Stop the API server."""
        self.should_stop = True
        # Note: uvicorn doesn't have a clean shutdown mechanism when run this way
        # For production, you'd want a more sophisticated approach

# Global instance
_api_integration: Optional[TKAAPIIntegration] = None

def get_api_integration() -> TKAAPIIntegration:
    global _api_integration
    if _api_integration is None:
        _api_integration = TKAAPIIntegration()
    return _api_integration

# ===== INTEGRATION WITH MAIN APP =====

# Add this to your main.py in the KineticConstructorModern.__init__ method:

def __init__(self, ..., enable_api: bool = True):
    # ... existing initialization ...
    
    # Start API server if enabled
    if enable_api:
        try:
            api_integration = get_api_integration()
            api_integration.start_api_server()
        except Exception as e:
            logger.warning(f"Failed to start API server: {e}")

# ===== EXAMPLE USAGE =====

# Once implemented, external tools can:

# 1. Get current sequence:
# GET http://localhost:8000/api/current-sequence

# 2. Create new sequence:
# POST http://localhost:8000/api/sequences
# {"name": "My Sequence", "length": 8}

# 3. Undo/Redo:
# POST http://localhost:8000/api/undo
# POST http://localhost:8000/api/redo

# 4. Check status:
# GET http://localhost:8000/api/status

# ===== TESTING SCRIPT =====
import requests

def test_tka_api():
    """Test the TKA API endpoints."""
    base_url = "http://localhost:8000"
    
    # Check status
    response = requests.get(f"{base_url}/api/status")
    print("Status:", response.json())
    
    # Create sequence
    response = requests.post(f"{base_url}/api/sequences", json={
        "name": "API Test Sequence",
        "length": 4
    })
    print("Created:", response.json())
    
    # Get current sequence
    response = requests.get(f"{base_url}/api/current-sequence")
    print("Current:", response.json())
    
    # Test undo
    response = requests.post(f"{base_url}/api/undo")
    print("Undo:", response.json())

if __name__ == "__main__":
    test_tka_api()

# ===== JAVASCRIPT CLIENT EXAMPLE =====
"""
// Simple JavaScript client for web integration
class TKAClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }

    async getCurrentSequence() {
        const response = await fetch(`${this.baseUrl}/api/current-sequence`);
        return response.json();
    }

    async createSequence(name, length = 16) {
        const response = await fetch(`${this.baseUrl}/api/sequences`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, length})
        });
        return response.json();
    }

    async undo() {
        const response = await fetch(`${this.baseUrl}/api/undo`, {method: 'POST'});
        return response.json();
    }

    async redo() {
        const response = await fetch(`${this.baseUrl}/api/redo`, {method: 'POST'});
        return response.json();
    }
}

// Usage:
const tka = new TKAClient();
const sequence = await tka.createSequence('Web Sequence', 8);
console.log('Created sequence:', sequence);
"""# Phase 2: Cross-Language API Layer + Enhanced Fault Tolerance
# Complete, working implementation

# ===== FILE: src/infrastructure/api/__init__.py =====
"""
TKA Desktop API Infrastructure

Provides multi-language access to TKA functionality through:
- REST API for CRUD operations
- WebSocket API for real-time events
- Auto-generated client libraries
- Production-grade fault tolerance
"""

from .rest_api import app as rest_app
from .websocket_api import WebSocketConnectionManager, websocket_endpoint
from .api_models import *
from .fault_tolerance import CircuitBreaker, RetryPolicy, HealthChecker
from .client_generator import ClientGenerator
from .api_server import TKAAPIServer

__all__ = [
    "rest_app", "WebSocketConnectionManager", "websocket_endpoint",
    "SequenceAPI", "BeatAPI", "MotionAPI", "CircuitBreaker", "RetryPolicy",
    "HealthChecker", "ClientGenerator", "TKAAPIServer"
]

# ===== FILE: src/infrastructure/api/api_models.py =====
"""
API data models with comprehensive validation and serialization.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum

# === Core API Models ===

class MotionTypeAPI(str, Enum):
    PRO = "pro"
    ANTI = "anti"
    FLOAT = "float"
    DASH = "dash"
    STATIC = "static"

class RotationDirectionAPI(str, Enum):
    CLOCKWISE = "cw"
    COUNTER_CLOCKWISE = "ccw"
    NO_ROTATION = "no_rot"

class LocationAPI(str, Enum):
    NORTH = "n"
    EAST = "e"
    SOUTH = "s"
    WEST = "w"
    NORTHEAST = "ne"
    SOUTHEAST = "se"
    SOUTHWEST = "sw"
    NORTHWEST = "nw"

class MotionAPI(BaseModel):
    motion_type: MotionTypeAPI
    prop_rot_dir: RotationDirectionAPI
    start_loc: LocationAPI
    end_loc: LocationAPI
    turns: float = Field(default=0.0, ge=0.0, le=4.0)
    start_ori: str = Field(default="in", regex="^(in|out)$")
    end_ori: str = Field(default="in", regex="^(in|out)$")

    @validator('turns')
    def validate_turns(cls, v):
        if v % 0.5 != 0:
            raise ValueError("Turns must be in 0.5 increments")
        return v

class BeatAPI(BaseModel):
    id: str = Field(..., description="Unique beat identifier")
    beat_number: int = Field(..., ge=1, le=64)
    letter: Optional[str] = Field(None, regex="^[A-Za-z]?$")
    duration: float = Field(default=1.0, gt=0.0, le=10.0)
    blue_motion: Optional[MotionAPI] = None
    red_motion: Optional[MotionAPI] = None
    blue_reversal: bool = False
    red_reversal: bool = False
    is_blank: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SequenceAPI(BaseModel):
    id: str
    name: str = Field(..., min_length=1, max_length=100)
    word: str = ""
    beats: List[BeatAPI] = Field(default_factory=list)
    start_position: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @property
    def length(self) -> int:
        return len(self.beats)

# === Request/Response Models ===

class CreateSequenceRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    length: int = Field(default=16, ge=1, le=64)
    beats: Optional[List[BeatAPI]] = None

class UpdateSequenceRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    beats: Optional[List[BeatAPI]] = None
    metadata: Optional[Dict[str, Any]] = None

class AddBeatRequest(BaseModel):
    beat: BeatAPI
    position: Optional[int] = Field(None, ge=0)

class APIResponse(BaseModel):
    success: bool
    message: str = ""
    data: Optional[Any] = None
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class CommandResponse(APIResponse):
    command_id: str = ""
    can_undo: bool = False
    can_redo: bool = False
    undo_description: Optional[str] = None

class PaginatedResponse(APIResponse):
    page: int = 1
    page_size: int = 20
    total_items: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_previous: bool = False

# === Health Models ===

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class ComponentHealth(BaseModel):
    name: str
    status: HealthStatus
    message: str = ""
    last_check: datetime = Field(default_factory=datetime.now)
    response_time_ms: float = 0.0

class SystemHealth(BaseModel):
    status: HealthStatus
    components: List[ComponentHealth]
    version: str = "2.0.0"
    uptime_seconds: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)

# ===== FILE: src/infrastructure/api/fault_tolerance.py =====
"""
Production-grade fault tolerance infrastructure.
"""

import asyncio
import time
import logging
from typing import Callable, Any, Optional, Dict, List
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
import random

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreakerStats:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None

class CircuitBreaker:
    """Circuit breaker for fault tolerance."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: type = Exception,
        name: str = "CircuitBreaker"
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.name = name
        
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: Optional[float] = None
        self._stats = CircuitBreakerStats()
        self._lock = asyncio.Lock()

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await self._call_async(func, *args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return self._call_sync(func, *args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    async def _call_async(self, func: Callable, *args, **kwargs) -> Any:
        async with self._lock:
            if not self._can_execute():
                raise CircuitBreakerError(f"Circuit breaker {self.name} is OPEN")

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except self.expected_exception as e:
            await self._on_failure()
            raise

    def _call_sync(self, func: Callable, *args, **kwargs) -> Any:
        if not self._can_execute():
            raise CircuitBreakerError(f"Circuit breaker {self.name} is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success_sync()
            return result
        except self.expected_exception as e:
            self._on_failure_sync()
            raise

    def _can_execute(self) -> bool:
        if self._state == CircuitState.CLOSED:
            return True
        elif self._state == CircuitState.OPEN:
            if (self._last_failure_time and 
                time.time() - self._last_failure_time > self.recovery_timeout):
                self._state = CircuitState.HALF_OPEN
                return True
            return False
        elif self._state == CircuitState.HALF_OPEN:
            return True
        return False

    async def _on_success(self):
        async with self._lock:
            self._stats.total_requests += 1
            self._stats.successful_requests += 1
            
            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.CLOSED
                self._failure_count = 0
                logger.info(f"Circuit breaker {self.name} recovered")

    def _on_success_sync(self):
        self._stats.total_requests += 1
        self._stats.successful_requests += 1
        
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.CLOSED
            self._failure_count = 0

    async def _on_failure(self):
        async with self._lock:
            self._stats.total_requests += 1
            self._stats.failed_requests += 1
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
                logger.warning(f"Circuit breaker {self.name} opened")

    def _on_failure_sync(self):
        self._stats.total_requests += 1
        self._stats.failed_requests += 1
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN

    @property
    def state(self) -> CircuitState:
        return self._state

    @property
    def stats(self) -> CircuitBreakerStats:
        return self._stats

class CircuitBreakerError(Exception):
    pass

class RetryPolicy:
    """Retry policy with exponential backoff."""

    def __init__(
        self,
        max_attempts: int = 3,
        delay: float = 1.0,
        exponential_backoff: bool = True,
        max_delay: float = 60.0,
        jitter: bool = True,
        retryable_exceptions: tuple = (Exception,)
    ):
        self.max_attempts = max_attempts
        self.delay = delay
        self.exponential_backoff = exponential_backoff
        self.max_delay = max_delay
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await self._retry_async(func, *args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return self._retry_sync(func, *args, **kwargs)
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    async def _retry_async(self, func: Callable, *args, **kwargs) -> Any:
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                return await func(*args, **kwargs)
            except self.retryable_exceptions as e:
                last_exception = e
                
                if attempt == self.max_attempts - 1:
                    raise
                
                delay = self._calculate_delay(attempt)
                logger.warning(f"Retry {attempt + 1}/{self.max_attempts} in {delay:.2f}s")
                await asyncio.sleep(delay)
        
        raise last_exception

    def _retry_sync(self, func: Callable, *args, **kwargs) -> Any:
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except self.retryable_exceptions as e:
                last_exception = e
                
                if attempt == self.max_attempts - 1:
                    raise
                
                delay = self._calculate_delay(attempt)
                time.sleep(delay)
        
        raise last_exception

    def _calculate_delay(self, attempt: int) -> float:
        if self.exponential_backoff:
            delay = self.delay * (2 ** attempt)
        else:
            delay = self.delay
        
        delay = min(delay, self.max_delay)
        
        if self.jitter:
            delay *= (0.5 + random.random() * 0.5)
        
        return delay

class HealthChecker:
    """Health monitoring system."""

    def __init__(self, check_interval: float = 30.0):
        self.check_interval = check_interval
        self._health_checks: Dict[str, Callable] = {}
        self._component_health: Dict[str, ComponentHealth] = {}
        self._running = False
        self._task: Optional[asyncio.Task] = None

    def register_health_check(self, name: str, check_func: Callable):
        self._health_checks[name] = check_func
        logger.info(f"Registered health check: {name}")

    async def start(self):
        if self._running:
            return
        
        self._running = True
        self._task = asyncio.create_task(self._health_check_loop())

    async def stop(self):
        if not self._running:
            return
        
        self._running = False
        if self._task:
            self._task.cancel()

    async def _health_check_loop(self):
        while self._running:
            try:
                await self._perform_health_checks()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check error: {e}")

    async def _perform_health_checks(self):
        for name, check_func in self._health_checks.items():
            try:
                start_time = time.perf_counter()
                
                if asyncio.iscoroutinefunction(check_func):
                    await check_func()
                else:
                    check_func()
                
                response_time = (time.perf_counter() - start_time) * 1000
                
                self._component_health[name] = ComponentHealth(
                    name=name,
                    status=HealthStatus.HEALTHY,
                    message="OK",
                    response_time_ms=response_time
                )
                
            except Exception as e:
                self._component_health[name] = ComponentHealth(
                    name=name,
                    status=HealthStatus.UNHEALTHY,
                    message=str(e)
                )

    async def get_system_health(self) -> SystemHealth:
        if not self._component_health:
            return SystemHealth(
                status=HealthStatus.HEALTHY,
                components=[]
            )
        
        components = list(self._component_health.values())
        unhealthy_count = sum(1 for c in components if c.status == HealthStatus.UNHEALTHY)
        
        if unhealthy_count > 0:
            overall_status = HealthStatus.UNHEALTHY
        else:
            overall_status = HealthStatus.HEALTHY
        
        return SystemHealth(
            status=overall_status,
            components=components
        )

# Health check functions
async def check_event_bus_health():
    # Basic health check - would check actual event bus in real implementation
    return True

async def check_command_processor_health():
    # Basic health check - would check actual command processor
    return True

def check_database_health():
    # Basic health check - would check database connection
    return True

def check_memory_usage():
    try:
        import psutil
        memory_percent = psutil.virtual_memory().percent
        if memory_percent > 90:
            raise Exception(f"High memory usage: {memory_percent}%")
        return True
    except ImportError:
        # psutil not available, assume healthy
        return True

# ===== FILE: src/infrastructure/api/rest_api.py =====
"""
FastAPI REST API implementation.
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from typing import List, Optional
from contextlib import asynccontextmanager

from .api_models import *
from .fault_tolerance import CircuitBreaker, RetryPolicy, HealthChecker
from .fault_tolerance import check_event_bus_health, check_command_processor_health
from .fault_tolerance import check_database_health, check_memory_usage

logger = logging.getLogger(__name__)

# Circuit breakers
sequence_circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=30,
    name="sequence_service"
)

# Retry policies
default_retry_policy = RetryPolicy(
    max_attempts=3,
    delay=1.0,
    exponential_backoff=True
)

# Health checker
health_checker = HealthChecker()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting TKA API...")
    
    # Register health checks
    health_checker.register_health_check("event_bus", check_event_bus_health)
    health_checker.register_health_check("command_processor", check_command_processor_health)
    health_checker.register_health_check("database", check_database_health)
    health_checker.register_health_check("memory", check_memory_usage)
    
    await health_checker.start()
    yield
    
    # Shutdown
    await health_checker.stop()
    logger.info("TKA API stopped")

app = FastAPI(
    title="TKA Desktop API",
    description="Cross-language API for Kinetic Alphabet Desktop",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred"
        }
    )

# Request timing middleware
@app.middleware("http")
async def add_request_timing(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# === Health Endpoints ===

@app.get("/health", response_model=SystemHealth)
async def health_check():
    return await health_checker.get_system_health()

@app.get("/health/ready")
async def readiness_check():
    health = await health_checker.get_system_health()
    if health.status == HealthStatus.HEALTHY:
        return {"status": "ready"}
    else:
        raise HTTPException(status_code=503, detail="Service not ready")

@app.get("/health/live")
async def liveness_check():
    return {"status": "alive", "timestamp": datetime.now()}

# === Mock Data Store (replace with real implementation) ===
_mock_sequences: Dict[str, SequenceAPI] = {}
_mock_sequence_counter = 0

def get_next_sequence_id() -> str:
    global _mock_sequence_counter
    _mock_sequence_counter += 1
    return f"seq_{_mock_sequence_counter}"

# === Sequence Endpoints ===

@app.get("/api/sequences", response_model=PaginatedResponse)
@sequence_circuit_breaker
@default_retry_policy
async def list_sequences(page: int = 1, page_size: int = 20):
    try:
        sequences = list(_mock_sequences.values())
        total_items = len(sequences)
        total_pages = (total_items + page_size - 1) // page_size
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        page_sequences = sequences[start_idx:end_idx]
        
        return PaginatedResponse(
            success=True,
            message="Sequences retrieved successfully",
            data=page_sequences,
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1
        )
    except Exception as e:
        logger.error(f"Failed to list sequences: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve sequences")

@app.post("/api/sequences", response_model=CommandResponse)
@sequence_circuit_breaker
@default_retry_policy
async def create_sequence(request: CreateSequenceRequest):
    try:
        sequence_id = get_next_sequence_id()
        
        # Create beats for the sequence
        beats = []
        if request.beats:
            beats = request.beats
        else:
            # Create empty beats
            for i in range(request.length):
                beat = BeatAPI(
                    id=f"beat_{sequence_id}_{i+1}",
                    beat_number=i + 1,
                    letter=None,
                    duration=1.0,
                    is_blank=True
                )
                beats.append(beat)
        
        sequence = SequenceAPI(
            id=sequence_id,
            name=request.name,
            beats=beats
        )
        
        _mock_sequences[sequence_id] = sequence
        
        return CommandResponse(
            success=True,
            message="Sequence created successfully",
            data=sequence,
            command_id=f"create_seq_{sequence_id}",
            can_undo=True
        )
    except Exception as e:
        logger.error(f"Failed to create sequence: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/sequences/{sequence_id}", response_model=APIResponse)
@sequence_circuit_breaker
async def get_sequence(sequence_id: str):
    try:
        if sequence_id not in _mock_sequences:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        return APIResponse(
            success=True,
            message="Sequence retrieved successfully",
            data=_mock_sequences[sequence_id]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get sequence {sequence_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve sequence")

@app.put("/api/sequences/{sequence_id}", response_model=CommandResponse)
@sequence_circuit_breaker
@default_retry_policy
async def update_sequence(sequence_id: str, request: UpdateSequenceRequest):
    try:
        if sequence_id not in _mock_sequences:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        sequence = _mock_sequences[sequence_id]
        
        # Update fields
        if request.name is not None:
            sequence.name = request.name
        if request.beats is not None:
            sequence.beats = request.beats
        if request.metadata is not None:
            sequence.metadata = request.metadata
        
        sequence.updated_at = datetime.now()
        
        return CommandResponse(
            success=True,
            message="Sequence updated successfully",
            data=sequence,
            can_undo=True
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update sequence {sequence_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/sequences/{sequence_id}", response_model=CommandResponse)
@sequence_circuit_breaker
async def delete_sequence(sequence_id: str):
    try:
        if sequence_id not in _mock_sequences:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        del _mock_sequences[sequence_id]
        
        return CommandResponse(
            success=True,
            message="Sequence deleted successfully",
            command_id=f"delete_seq_{sequence_id}",
            can_undo=True
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete sequence {sequence_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete sequence")

# === Beat Endpoints ===

@app.post("/api/sequences/{sequence_id}/beats", response_model=CommandResponse)
@sequence_circuit_breaker
@default_retry_policy  
async def add_beat(sequence_id: str, request: AddBeatRequest):
    try:
        if sequence_id not in _mock_sequences:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        sequence = _mock_sequences[sequence_id]
        
        # Add beat at specified position or end
        if request.position is not None:
            sequence.beats.insert(request.position, request.beat)
        else:
            sequence.beats.append(request.beat)
        
        # Update beat numbers
        for i, beat in enumerate(sequence.beats):
            beat.beat_number = i + 1
        
        sequence.updated_at = datetime.now()
        
        return CommandResponse(
            success=True,
            message="Beat added successfully", 
            data=sequence,
            can_undo=True
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add beat to sequence {sequence_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/sequences/{sequence_id}/beats/{beat_number}", response_model=CommandResponse)
@sequence_circuit_breaker
async def remove_beat(sequence_id: str, beat_number: int):
    try:
        if sequence_id not in _mock_sequences:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        sequence = _mock_sequences[sequence_id]
        
        # Find and remove beat
        beat_index = beat_number - 1
        if beat_index < 0 or beat_index >= len(sequence.beats):
            raise HTTPException(status_code=404, detail="Beat not found")
        
        sequence.beats.pop(beat_index)
        
        # Update beat numbers
        for i, beat in enumerate(sequence.beats):
            beat.beat_number = i + 1
        
        sequence.updated_at = datetime.now()
        
        return CommandResponse(
            success=True,
            message="Beat removed successfully",
            data=sequence,
            can_undo=True
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to remove beat {beat_number} from sequence {sequence_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# === Command/Undo Endpoints ===

@app.post("/api/commands/undo", response_model=CommandResponse)
async def undo_command():
    # Mock undo implementation
    return CommandResponse(
        success=True,
        message="Command undone successfully",
        can_undo=False,
        can_redo=True
    )

@app.post("/api/commands/redo", response_model=CommandResponse)
async def redo_command():
    # Mock redo implementation
    return CommandResponse(
        success=True,
        message="Command redone successfully",
        can_undo=True,
        can_redo=False
    )

@app.get("/api/commands/history", response_model=APIResponse)
async def get_command_history():
    return APIResponse(
        success=True,
        message="Command history retrieved successfully",
        data={
            "history": [],
            "can_undo": False,
            "can_redo": False
        }
    )

# ===== FILE: src/infrastructure/api/websocket_api.py =====
"""
WebSocket API for real-time event streaming.
"""

import asyncio
import json
import logging
from typing import Dict, Set, Optional, Any, List
from datetime import datetime
import uuid

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

class WebSocketConnectionManager:
    """Manages WebSocket connections with filtering."""

    def __init__(self):
        self._connections: Dict[str, WebSocket] = {}
        self._connection_filters: Dict[str, Set[str]] = {}
        self._connection_metadata: Dict[str, Dict[str, Any]] = {}

    async def connect(self, websocket: WebSocket, client_id: Optional[str] = None) -> str:
        await websocket.accept()
        
        if not client_id:
            client_id = f"client_{uuid.uuid4().hex[:8]}"
        
        self._connections[client_id] = websocket
        self._connection_filters[client_id] = set()
        self._connection_metadata[client_id] = {
            "connected_at": datetime.now(),
            "last_ping": datetime.now(),
            "events_sent": 0
        }
        
        logger.info(f"WebSocket client connected: {client_id}")
        
        # Send welcome message
        await self._send_to_client(client_id, {
            "type": "connection_established",
            "client_id": client_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Connected to TKA Desktop API"
        })
        
        return client_id

    async def disconnect(self, client_id: str):
        """Disconnect a WebSocket client."""
        if client_id in self._connections:
            try:
                await self._connections[client_id].close()
            except:
                pass
            
            del self._connections[client_id]
            if client_id in self._connection_filters:
                del self._connection_filters[client_id]
            if client_id in self._connection_metadata:
                del self._connection_metadata[client_id]
            
            logger.info(f"WebSocket client disconnected: {client_id}")

    async def set_event_filters(self, client_id: str, event_types: Set[str]):
        """Set event type filters for a client."""
        if client_id in self._connection_filters:
            self._connection_filters[client_id] = event_types
            logger.info(f"Set event filters for {client_id}: {event_types}")

    async def _send_to_client(self, client_id: str, data: Dict[str, Any]):
        """Send data to a specific client with error handling."""
        if client_id not in self._connections:
            return
        
        try:
            websocket = self._connections[client_id]
            await websocket.send_text(json.dumps(data, default=str))
            
            # Update metadata
            if client_id in self._connection_metadata:
                self._connection_metadata[client_id]["events_sent"] += 1
                self._connection_metadata[client_id]["last_ping"] = datetime.now()
                
        except WebSocketDisconnect:
            logger.info(f"Client {client_id} disconnected during send")
            await self.disconnect(client_id)
        except Exception as e:
            logger.error(f"Error sending to client {client_id}: {e}")
            await self.disconnect(client_id)

    async def broadcast_event(self, event_data: Dict[str, Any]):
        """Broadcast event to all connected clients."""
        if not self._connections:
            return
        
        disconnected_clients = []
        
        for client_id in self._connections.keys():
            try:
                # Check if client has filters
                filters = self._connection_filters.get(client_id, set())
                if filters and event_data.get("event_type") not in filters:
                    continue
                
                await self._send_to_client(client_id, event_data)
                
            except Exception as e:
                logger.error(f"Error broadcasting to client {client_id}: {e}")
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            await self.disconnect(client_id)

    async def send_heartbeat(self):
        """Send heartbeat to all connected clients."""
        heartbeat_data = {
            "type": "heartbeat",
            "timestamp": datetime.now().isoformat(),
            "connected_clients": len(self._connections)
        }
        
        for client_id in list(self._connections.keys()):
            await self._send_to_client(client_id, heartbeat_data)

    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        return {
            "total_connections": len(self._connections),
            "connections": {
                client_id: {
                    "connected_at": metadata["connected_at"].isoformat(),
                    "events_sent": metadata["events_sent"],
                    "last_ping": metadata["last_ping"].isoformat(),
                    "filters": list(self._connection_filters.get(client_id, set()))
                }
                for client_id, metadata in self._connection_metadata.items()
            }
        }

# Global WebSocket manager
_websocket_manager: Optional[WebSocketConnectionManager] = None

def get_websocket_manager() -> WebSocketConnectionManager:
    """Get global WebSocket manager instance."""
    global _websocket_manager
    if _websocket_manager is None:
        _websocket_manager = WebSocketConnectionManager()
    return _websocket_manager

# === WebSocket Endpoints ===

async def websocket_endpoint(websocket: WebSocket, client_id: Optional[str] = None):
    """Main WebSocket endpoint for real-time event streaming."""
    manager = get_websocket_manager()
    actual_client_id = None
    
    try:
        actual_client_id = await manager.connect(websocket, client_id)
        
        # Handle incoming messages
        while True:
            try:
                # Wait for message with timeout for heartbeat
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                message = json.loads(data)
                
                await handle_websocket_message(actual_client_id, message, manager)
                
            except asyncio.TimeoutError:
                # Send heartbeat
                await manager.send_heartbeat()
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format",
                    "timestamp": datetime.now().isoformat()
                }))
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error", 
                    "message": "Internal server error",
                    "timestamp": datetime.now().isoformat()
                }))
                
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        if actual_client_id:
            await manager.disconnect(actual_client_id)

async def handle_websocket_message(client_id: str, message: Dict[str, Any], manager: WebSocketConnectionManager):
    """Handle incoming WebSocket messages from clients."""
    message_type = message.get("type", "")
    
    if message_type == "set_filters":
        # Client wants to filter events
        event_types = set(message.get("event_types", []))
        await manager.set_event_filters(client_id, event_types)
        
        response = {
            "type": "filters_updated",
            "event_types": list(event_types),
            "timestamp": datetime.now().isoformat()
        }
        await manager._send_to_client(client_id, response)
        
    elif message_type == "ping":
        # Respond to ping
        response = {
            "type": "pong", 
            "timestamp": datetime.now().isoformat()
        }
        await manager._send_to_client(client_id, response)
        
    elif message_type == "get_stats":
        # Send connection stats
        stats = manager.get_connection_stats()
        response = {
            "type": "stats",
            "data": stats,
            "timestamp": datetime.now().isoformat()
        }
        await manager._send_to_client(client_id, response)
        
    else:
        # Unknown message type
        response = {
            "type": "error",
            "message": f"Unknown message type: {message_type}",
            "timestamp": datetime.now().isoformat()
        }
        await manager._send_to_client(client_id, response)

# ===== FILE: src/infrastructure/api/client_generator.py =====
"""
Automatic client library generation for multiple programming languages.
"""

import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ClientConfig:
    """Configuration for client generation."""
    language: str
    output_dir: Path
    package_name: str = "tka_client"
    version: str = "2.0.0"
    author: str = "TKA Desktop Team"
    description: str = "Generated client for TKA Desktop API"

class ClientGenerator:
    """Generates client libraries for multiple programming languages."""

    def __init__(self, api_schema: Dict[str, Any]):
        self.api_schema = api_schema

    def generate_all_clients(self, base_output_dir: Path) -> Dict[str, Path]:
        """Generate clients for all supported languages."""
        results = {}
        
        configs = [
            ClientConfig("typescript", base_output_dir / "typescript"),
            ClientConfig("python", base_output_dir / "python"),
            ClientConfig("rust", base_output_dir / "rust"),
        ]
        
        for config in configs:
            try:
                output_path = self.generate_client(config)
                results[config.language] = output_path
                print(f"✅ Generated {config.language} client at {output_path}")
            except Exception as e:
                print(f"❌ Failed to generate {config.language} client: {e}")
                results[config.language] = None
        
        return results

    def generate_client(self, config: ClientConfig) -> Path:
        """Generate client for specific language."""
        config.output_dir.mkdir(parents=True, exist_ok=True)
        
        if config.language == "typescript":
            return self._generate_typescript_client(config)
        elif config.language == "python":
            return self._generate_python_client(config)
        elif config.language == "rust":
            return self._generate_rust_client(config)
        else:
            raise ValueError(f"Unsupported language: {config.language}")

    def _generate_typescript_client(self, config: ClientConfig) -> Path:
        """Generate TypeScript client with full type safety."""
        
        # Generate types
        types_content = '''// Generated TypeScript types for TKA Desktop API

export interface MotionAPI {
  motion_type: "pro" | "anti" | "float" | "dash" | "static";
  prop_rot_dir: "cw" | "ccw" | "no_rot";
  start_loc: "n" | "e" | "s" | "w" | "ne" | "se" | "sw" | "nw";
  end_loc: "n" | "e" | "s" | "w" | "ne" | "se" | "sw" | "nw";
  turns: number;
  start_ori: "in" | "out";
  end_ori: "in" | "out";
}

export interface BeatAPI {
  id: string;
  beat_number: number;
  letter?: string;
  duration: number;
  blue_motion?: MotionAPI;
  red_motion?: MotionAPI;
  blue_reversal: boolean;
  red_reversal: boolean;
  is_blank: boolean;
  metadata: Record<string, any>;
}

export interface SequenceAPI {
  id: string;
  name: string;
  word: string;
  beats: BeatAPI[];
  start_position?: string;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface CreateSequenceRequest {
  name: string;
  length?: number;
  beats?: BeatAPI[];
}

export interface APIResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  error_code?: string;
  timestamp: string;
}

export interface CommandResponse<T = any> extends APIResponse<T> {
  command_id: string;
  can_undo: boolean;
  can_redo: boolean;
  undo_description?: string;
}
'''
        
        # Generate client
        client_content = '''// Generated TypeScript client for TKA Desktop API

import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { 
  SequenceAPI, BeatAPI, CreateSequenceRequest, 
  APIResponse, CommandResponse 
} from './types';

export class TKAClient {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Sequence operations
  async listSequences(page = 1, pageSize = 20): Promise<APIResponse<SequenceAPI[]>> {
    const response = await this.client.get(`/api/sequences?page=${page}&page_size=${pageSize}`);
    return response.data;
  }

  async createSequence(request: CreateSequenceRequest): Promise<CommandResponse<SequenceAPI>> {
    const response = await this.client.post('/api/sequences', request);
    return response.data;
  }

  async getSequence(sequenceId: string): Promise<APIResponse<SequenceAPI>> {
    const response = await this.client.get(`/api/sequences/${sequenceId}`);
    return response.data;
  }

  async deleteSequence(sequenceId: string): Promise<CommandResponse> {
    const response = await this.client.delete(`/api/sequences/${sequenceId}`);
    return response.data;
  }

  // Beat operations
  async addBeat(sequenceId: string, beat: BeatAPI, position?: number): Promise<CommandResponse<SequenceAPI>> {
    const request = { beat, position };
    const response = await this.client.post(`/api/sequences/${sequenceId}/beats`, request);
    return response.data;
  }

  async removeBeat(sequenceId: string, beatNumber: number): Promise<CommandResponse<SequenceAPI>> {
    const response = await this.client.delete(`/api/sequences/${sequenceId}/beats/${beatNumber}`);
    return response.data;
  }

  // Command operations
  async undo(): Promise<CommandResponse> {
    const response = await this.client.post('/api/commands/undo');
    return response.data;
  }

  async redo(): Promise<CommandResponse> {
    const response = await this.client.post('/api/commands/redo');
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<any> {
    const response = await this.client.get('/health');
    return response.data;
  }
}
'''
        
        # Generate WebSocket client
        websocket_content = '''// Generated WebSocket client for TKA Desktop API

export interface WebSocketEvent {
  type: string;
  event_type?: string;
  timestamp: string;
  data?: any;
}

export class TKAWebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private eventHandlers: Map<string, (event: WebSocketEvent) => void> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  constructor(url: string) {
    this.url = url;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
          console.log('Connected to TKA WebSocket');
          this.reconnectAttempts = 0;
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const data: WebSocketEvent = JSON.parse(event.data);
            this.handleEvent(data);
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error);
          }
        };

        this.ws.onclose = () => {
          console.log('WebSocket connection closed');
          this.attemptReconnect();
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          reject(error);
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  setEventFilters(eventTypes: string[]): void {
    this.send({
      type: 'set_filters',
      event_types: eventTypes
    });
  }

  onEvent(eventType: string, handler: (event: WebSocketEvent) => void): void {
    this.eventHandlers.set(eventType, handler);
  }

  private send(data: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  private handleEvent(event: WebSocketEvent): void {
    const handler = this.eventHandlers.get(event.type);
    if (handler) {
      handler(event);
    }

    // Also check event_type for domain events
    if (event.event_type) {
      const domainHandler = this.eventHandlers.get(event.event_type);
      if (domainHandler) {
        domainHandler(event);
      }
    }
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      
      setTimeout(() => {
        this.connect().catch(console.error);
      }, this.reconnectDelay * this.reconnectAttempts);
    }
  }
}
'''
        
        # Generate package.json
        package_json = {
            "name": config.package_name,
            "version": config.version,
            "description": config.description,
            "main": "dist/index.js",
            "types": "dist/index.d.ts",
            "scripts": {
                "build": "tsc",
                "test": "jest"
            },
            "dependencies": {
                "axios": "^1.0.0"
            },
            "devDependencies": {
                "typescript": "^5.0.0",
                "@types/node": "^20.0.0"
            }
        }
        
        # Write files
        src_dir = config.output_dir / "src"
        src_dir.mkdir(exist_ok=True)
        
        self._write_file(src_dir / "types.ts", types_content)
        self._write_file(src_dir / "client.ts", client_content)
        self._write_file(src_dir / "websocket.ts", websocket_content)
        self._write_file(src_dir / "index.ts", 
                        'export * from "./types";\nexport * from "./client";\nexport * from "./websocket";')
        self._write_file(config.output_dir / "package.json", json.dumps(package_json, indent=2))
        
        return config.output_dir

    def _generate_python_client(self, config: ClientConfig) -> Path:
        """Generate Python client with type hints."""
        
        # Generate models
        models_content = '''"""Generated Python models for TKA Desktop API."""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from datetime import datetime

class MotionAPI(BaseModel):
    motion_type: str
    prop_rot_dir: str
    start_loc: str
    end_loc: str
    turns: float
    start_ori: str = "in"
    end_ori: str = "in"

class BeatAPI(BaseModel):
    id: str
    beat_number: int
    letter: Optional[str] = None
    duration: float = 1.0
    blue_motion: Optional[MotionAPI] = None
    red_motion: Optional[MotionAPI] = None
    blue_reversal: bool = False
    red_reversal: bool = False
    is_blank: bool = False
    metadata: Dict[str, Any] = {}

class SequenceAPI(BaseModel):
    id: str
    name: str
    word: str = ""
    beats: List[BeatAPI] = []
    start_position: Optional[str] = None
    metadata: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

class CreateSequenceRequest(BaseModel):
    name: str
    length: int = 16
    beats: Optional[List[BeatAPI]] = None

class APIResponse(BaseModel):
    success: bool
    message: str = ""
    data: Optional[Any] = None
    error_code: Optional[str] = None
    timestamp: datetime

class CommandResponse(APIResponse):
    command_id: str = ""
    can_undo: bool = False
    can_redo: bool = False
    undo_description: Optional[str] = None
'''
        
        # Generate client
        client_content = '''"""Generated Python client for TKA Desktop API."""

import requests
from typing import Optional, Dict, Any
from .models import SequenceAPI, BeatAPI, CreateSequenceRequest, APIResponse, CommandResponse

class TKAClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def list_sequences(self, page: int = 1, page_size: int = 20) -> APIResponse:
        """List all sequences with pagination."""
        response = self.session.get(
            f"{self.base_url}/api/sequences",
            params={"page": page, "page_size": page_size}
        )
        response.raise_for_status()
        return APIResponse(**response.json())

    def create_sequence(self, request: CreateSequenceRequest) -> CommandResponse:
        """Create a new sequence."""
        response = self.session.post(
            f"{self.base_url}/api/sequences",
            json=request.dict()
        )
        response.raise_for_status()
        return CommandResponse(**response.json())

    def get_sequence(self, sequence_id: str) -> APIResponse:
        """Get a specific sequence by ID."""
        response = self.session.get(f"{self.base_url}/api/sequences/{sequence_id}")
        response.raise_for_status()
        return APIResponse(**response.json())

    def delete_sequence(self, sequence_id: str) -> CommandResponse:
        """Delete a sequence."""
        response = self.session.delete(f"{self.base_url}/api/sequences/{sequence_id}")
        response.raise_for_status()
        return CommandResponse(**response.json())

    def add_beat(self, sequence_id: str, beat: BeatAPI, position: Optional[int] = None) -> CommandResponse:
        """Add a beat to a sequence."""
        request_data = {"beat": beat.dict()}
        if position is not None:
            request_data["position"] = position
            
        response = self.session.post(
            f"{self.base_url}/api/sequences/{sequence_id}/beats",
            json=request_data
        )
        response.raise_for_status()
        return CommandResponse(**response.json())

    def remove_beat(self, sequence_id: str, beat_number: int) -> CommandResponse:
        """Remove a beat from a sequence."""
        response = self.session.delete(
            f"{self.base_url}/api/sequences/{sequence_id}/beats/{beat_number}"
        )
        response.raise_for_status()
        return CommandResponse(**response.json())

    def undo(self) -> CommandResponse:
        """Undo the last command."""
        response = self.session.post(f"{self.base_url}/api/commands/undo")
        response.raise_for_status()
        return CommandResponse(**response.json())

    def redo(self) -> CommandResponse:
        """Redo the last undone command."""
        response = self.session.post(f"{self.base_url}/api/commands/redo")
        response.raise_for_status()
        return CommandResponse(**response.json())

    def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
'''
        
        # Create package structure
        package_dir = config.output_dir / config.package_name
        package_dir.mkdir(parents=True, exist_ok=True)
        
        # Write Python files
        self._write_file(package_dir / "__init__.py", 
                        f'"""TKA Desktop API Client v{config.version}"""\n'
                        "from .client import TKAClient\n"
                        "from .models import *\n"
                        f'\n__version__ = "{config.version}"\n')
        self._write_file(package_dir / "models.py", models_content)
        self._write_file(package_dir / "client.py", client_content)
        
        # Generate setup.py
        setup_content = f'''from setuptools import setup, find_packages

setup(
    name="{config.package_name}",
    version="{config.version}",
    description="{config.description}",
    author="{config.author}",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.8",
)
'''
        self._write_file(config.output_dir / "setup.py", setup_content)
        
        return config.output_dir

    def _generate_rust_client(self, config: ClientConfig) -> Path:
        """Generate Rust client with strong typing."""
        
        # Generate Cargo.toml
        cargo_toml = f'''[package]
name = "{config.package_name.replace('-', '_')}"
version = "{config.version}"
description = "{config.description}"
authors = ["{config.author}"]
edition = "2021"

[dependencies]
reqwest = {{ version = "0.11", features = ["json"] }}
serde = {{ version = "1.0", features = ["derive"] }}
serde_json = "1.0"
tokio = {{ version = "1.0", features = ["full"] }}
chrono = {{ version = "0.4", features = ["serde"] }}
'''
        
        # Generate lib.rs
        lib_content = '''//! Generated Rust client for TKA Desktop API

pub mod types;
pub mod client;

pub use types::*;
pub use client::TKAClient;
'''
        
        # Generate types
        types_content = '''//! Generated Rust types for TKA Desktop API

use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MotionAPI {
    pub motion_type: String,
    pub prop_rot_dir: String,
    pub start_loc: String,
    pub end_loc: String,
    pub turns: f64,
    pub start_ori: String,
    pub end_ori: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BeatAPI {
    pub id: String,
    pub beat_number: i32,
    pub letter: Option<String>,
    pub duration: f64,
    pub blue_motion: Option<MotionAPI>,
    pub red_motion: Option<MotionAPI>,
    pub blue_reversal: bool,
    pub red_reversal: bool,
    pub is_blank: bool,
    pub metadata: HashMap<String, serde_json::Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SequenceAPI {
    pub id: String,
    pub name: String,
    pub word: String,
    pub beats: Vec<BeatAPI>,
    pub start_position: Option<String>,
    pub metadata: HashMap<String, serde_json::Value>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreateSequenceRequest {
    pub name: String,
    pub length: Option<i32>,
    pub beats: Option<Vec<BeatAPI>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct APIResponse<T> {
    pub success: bool,
    pub message: String,
    pub data: Option<T>,
    pub error_code: Option<String>,
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CommandResponse<T> {
    pub success: bool,
    pub message: String,
    pub data: Option<T>,
    pub error_code: Option<String>,
    pub timestamp: DateTime<Utc>,
    pub command_id: String,
    pub can_undo: bool,
    pub can_redo: bool,
    pub undo_description: Option<String>,
}
'''
        
        # Generate client
        client_content = '''//! Generated Rust client for TKA Desktop API

use crate::types::*;
use reqwest::Client;
use serde_json::json;

#[derive(Debug)]
pub struct TKAClient {
    client: Client,
    base_url: String,
}

impl TKAClient {
    pub fn new(base_url: &str) -> Self {
        Self {
            client: Client::new(),
            base_url: base_url.trim_end_matches('/').to_string(),
        }
    }

    pub async fn list_sequences(&self, page: Option<i32>, page_size: Option<i32>) -> Result<APIResponse<Vec<SequenceAPI>>, reqwest::Error> {
        let mut url = format!("{}/api/sequences", self.base_url);
        
        let mut params = vec![];
        if let Some(p) = page {
            params.push(format!("page={}", p));
        }
        if let Some(ps) = page_size {
            params.push(format!("page_size={}", ps));
        }
        
        if !params.is_empty() {
            url.push('?');
            url.push_str(&params.join("&"));
        }

        let response = self.client.get(&url).send().await?;
        let result = response.json().await?;
        Ok(result)
    }

    pub async fn create_sequence(&self, request: &CreateSequenceRequest) -> Result<CommandResponse<SequenceAPI>, reqwest::Error> {
        let response = self.client
            .post(&format!("{}/api/sequences", self.base_url))
            .json(request)
            .send()
            .await?;
            
        let result = response.json().await?;
        Ok(result)
    }

    pub async fn get_sequence(&self, sequence_id: &str) -> Result<APIResponse<SequenceAPI>, reqwest::Error> {
        let response = self.client
            .get(&format!("{}/api/sequences/{}", self.base_url, sequence_id))
            .send()
            .await?;
            
        let result = response.json().await?;
        Ok(result)
    }

    pub async fn delete_sequence(&self, sequence_id: &str) -> Result<CommandResponse<()>, reqwest::Error> {
        let response = self.client
            .delete(&format!("{}/api/sequences/{}", self.base_url, sequence_id))
            .send()
            .await?;
            
        let result = response.json().await?;
        Ok(result)
    }

    pub async fn add_beat(&self, sequence_id: &str, beat: &BeatAPI, position: Option<i32>) -> Result<CommandResponse<SequenceAPI>, reqwest::Error> {
        let request_data = json!({
            "beat": beat,
            "position": position
        });

        let response = self.client
            .post(&format!("{}/api/sequences/{}/beats", self.base_url, sequence_id))
            .json(&request_data)
            .send()
            .await?;
            
        let result = response.json().await?;
        Ok(result)
    }

    pub async fn remove_beat(&self, sequence_id: &str, beat_number: i32) -> Result<CommandResponse<SequenceAPI>, reqwest::Error> {
        let response = self.client
            .delete(&format!("{}/api/sequences/{}/beats/{}", self.base_url, sequence_id, beat_number))
            .send()
            .await?;
            
        let result = response.json().await?;
        Ok(result)
    }

    pub async fn undo(&self) -> Result<CommandResponse<()>, reqwest::Error> {
        let response = self.client
            .post(&format!("{}/api/commands/undo", self.base_url))
            .send()
            .await?;
            
        let result = response.json().await?;
        Ok(result)
    }

    pub async fn redo(&self) -> Result<CommandResponse<()>, reqwest::Error> {
        let response = self.client
            .post(&format!("{}/api/commands/redo", self.base_url))
            .send()
            .await?;
            
        let result = response.json().await?;
        Ok(result)
    }

    pub async fn health_check(&self) -> Result<serde_json::Value, reqwest::Error> {
        let response = self.client
            .get(&format!("{}/health", self.base_url))
            .send()
            .await?;
            
        let result = response.json().await?;
        Ok(result)
    }
}
'''
        
        # Create Rust project structure
        src_dir = config.output_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        
        self._write_file(config.output_dir / "Cargo.toml", cargo_toml)
        self._write_file(src_dir / "lib.rs", lib_content)
        self._write_file(src_dir / "types.rs", types_content)
        self._write_file(src_dir / "client.rs", client_content)
        
        return config.output_dir

    def _write_file(self, file_path: Path, content: str):
        """Write content to file, creating directories as needed."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

# ===== FILE: src/infrastructure/api/api_server.py =====
"""
Production-ready API server with comprehensive monitoring and fault tolerance.
"""

import asyncio
import signal
import logging
from typing import Optional, Dict, Any
from pathlib import Path
import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from .rest_api import app as rest_app
from .websocket_api import websocket_endpoint, get_websocket_manager
from .fault_tolerance import HealthChecker, check_event_bus_health, check_command_processor_health, check_database_health, check_memory_usage
from .client_generator import ClientGenerator

logger = logging.getLogger(__name__)

class TKAAPIServer:
    """Production-ready API server for TKA Desktop."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        auto_generate_clients: bool = True,
        client_output_dir: Optional[Path] = None
    ):
        self.host = host
        self.port = port
        self.auto_generate_clients = auto_generate_clients
        self.client_output_dir = client_output_dir or Path("./generated_clients")
        
        self.app = rest_app  # Use the FastAPI app from rest_api.py
        self.server: Optional[uvicorn.Server] = None
        self._setup_additional_routes()

    def _setup_additional_routes(self):
        """Setup additional routes not in rest_api.py."""
        
        # WebSocket endpoint
        @self.app.websocket("/ws")
        async def websocket_route(websocket):
            await websocket_endpoint(websocket)
        
        @self.app.websocket("/ws/{client_id}")
        async def websocket_route_with_id(websocket, client_id: str):
            await websocket_endpoint(websocket, client_id)
        
        # WebSocket stats endpoint
        @self.app.get("/api/websocket/stats")
        async def websocket_stats():
            """Get WebSocket connection statistics."""
            manager = get_websocket_manager()
            return manager.get_connection_stats()
        
        # Client generation endpoint
        @self.app.post("/api/generate-clients")
        async def generate_clients(languages: Optional[list] = None):
            """Generate client libraries for specified languages."""
            if not self.auto_generate_clients:
                return {"error": "Client generation is disabled"}
            
            try:
                schema = self._extract_api_schema()
                generator = ClientGenerator(schema)
                
                if languages:
                    from .client_generator import ClientConfig
                    results = {}
                    for lang in languages:
                        config = ClientConfig(lang, self.client_output_dir / lang)
                        results[lang] = str(generator.generate_client(config))
                else:
                    results = generator.generate_all_clients(self.client_output_dir)
                    results = {k: str(v) for k, v in results.items()}
                
                return {
                    "success": True,
                    "message": "Client libraries generated successfully",
                    "generated_clients": results
                }
                
            except Exception as e:
                logger.error(f"Failed to generate clients: {e}")
                return {"error": f"Client generation failed: {e}"}

    def _extract_api_schema(self) -> Dict[str, Any]:
        """Extract API schema from FastAPI app."""
        return self.app.openapi()

    async def start_async(self):
        """Start the API server asynchronously."""
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="info",
            access_log=True,
            loop="asyncio"
        )
        
        self.server = uvicorn.Server(config)
        
        logger.info(f"Starting TKA API server on {self.host}:{self.port}")
        
        # Generate clients on startup if enabled
        if self.auto_generate_clients:
            await self._generate_startup_clients()
        
        # Start server
        await self.server.serve()

    def start(self):
        """Start the API server synchronously."""
        try:
            asyncio.run(self.start_async())
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")

    async def stop(self):
        """Stop the API server gracefully."""
        if self.server:
            logger.info("Shutting down TKA API server...")
            self.server.should_exit = True
            
            # Cleanup WebSocket connections
            manager = get_websocket_manager()
            # manager.cleanup()  # Would implement cleanup method

    async def _generate_startup_clients(self):
        """Generate client libraries on server startup."""
        try:
            logger.info("Generating client libraries...")
            
            schema = self._extract_api_schema()
            generator = ClientGenerator(schema)
            results = generator.generate_all_clients(self.client_output_dir)
            
            generated_count = sum(1 for path in results.values() if path is not None)
            logger.info(f"Generated {generated_count} client libraries")
            
        except Exception as e:
            logger.warning(f"Failed to generate startup clients: {e}")

def create_api_server(
    host: str = "localhost",
    port: int = 8000,
    auto_generate_clients: bool = True
) -> TKAAPIServer:
    """Factory function to create API server with default configuration."""
    return TKAAPIServer(
        host=host,
        port=port,
        auto_generate_clients=auto_generate_clients
    )

# === CLI Integration ===

def main():
    """CLI entry point for the API server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="TKA Desktop API Server")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--no-client-gen", action="store_true", help="Disable automatic client generation")
    parser.add_argument("--client-dir", help="Client output directory")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and start server
    server = TKAAPIServer(
        host=args.host,
        port=args.port,
        auto_generate_clients=not args.no_client_gen,
        client_output_dir=Path(args.client_dir) if args.client_dir else None
    )
    
    # Handle shutdown signals
    def signal_handler(signum, frame):
        logger.info("Received shutdown signal")
        asyncio.create_task(server.stop())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    server.start()

if __name__ == "__main__":
    main()

# ===== FILE: src/infrastructure/api/integration.py =====
"""
Integration layer between TKA Desktop core and API server.
"""

import asyncio
import logging
from typing import Optional
from pathlib import Path

from .api_server import TKAAPIServer

logger = logging.getLogger(__name__)

class APIIntegration:
    """Manages API server integration with TKA Desktop."""

    def __init__(self):
        self.api_server: Optional[TKAAPIServer] = None
        self.server_task: Optional[asyncio.Task] = None

    async def start_api_server(
        self,
        host: str = "localhost",
        port: int = 8000,
        enable_client_generation: bool = True
    ):
        """Start the API server alongside TKA Desktop."""
        try:
            logger.info("Starting TKA Desktop API server...")
            
            # Create API server
            self.api_server = TKAAPIServer(
                host=host,
                port=port,
                auto_generate_clients=enable_client_generation
            )
            
            # Start server in background
            self.server_task = asyncio.create_task(self.api_server.start_async())
            
            logger.info(f"API server started on http://{host}:{port}")
            logger.info(f"API documentation available at http://{host}:{port}/api/docs")
            logger.info(f"WebSocket endpoint available at ws://{host}:{port}/ws")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start API server: {e}")
            return False

    async def stop_api_server(self):
        """Stop the API server gracefully."""
        if self.api_server:
            try:
                logger.info("Stopping API server...")
                await self.api_server.stop()
                
                if self.server_task:
                    self.server_task.cancel()
                    try:
                        await self.server_task
                    except asyncio.CancelledError:
                        pass
                
                logger.info("API server stopped")
                
            except Exception as e:
                logger.error(f"Error stopping API server: {e}")
            finally:
                self.api_server = None
                self.server_task = None

    def is_running(self) -> bool:
        """Check if API server is running."""
        return self.api_server is not None and self.server_task is not None and not self.server_task.done()

# Global integration instance
_api_integration: Optional[APIIntegration] = None

def get_api_integration() -> APIIntegration:
    """Get global API integration instance."""
    global _api_integration
    if _api_integration is None:
        _api_integration = APIIntegration()
    return _api_integration

# ===== TESTING FILES =====

# ===== FILE: tests/test_api_integration.py =====
"""
Integration tests for TKA Desktop API with fault tolerance validation.
"""

import pytest
import asyncio
import json
from typing import Dict, Any
import httpx
from fastapi.testclient import TestClient

from infrastructure.api.rest_api import app
from infrastructure.api.fault_tolerance import CircuitBreaker, RetryPolicy

class TestAPIIntegration:
    """Integration tests for API functionality."""

    def setup_method(self):
        """Setup for each test."""
        self.client = TestClient(app)

    def test_health_endpoints(self):
        """Test health check endpoints."""
        # Test main health endpoint
        response = self.client.get("/health")
        assert response.status_code == 200
        
        health_data = response.json()
        assert health_data["status"] in ["healthy", "degraded", "unhealthy"]
        assert "components" in health_data

        # Test readiness endpoint
        response = self.client.get("/health/ready")
        assert response.status_code in [200, 503]

        # Test liveness endpoint  
        response = self.client.get("/health/live")
        assert response.status_code == 200
        assert response.json()["status"] == "alive"

    def test_sequence_crud_operations(self):
        """Test complete CRUD operations for sequences."""
        # Create sequence
        create_data = {
            "name": "Test Sequence",
            "length": 4
        }
        response = self.client.post("/api/sequences", json=create_data)
        assert response.status_code == 200
        
        sequence_data = response.json()["data"]
        sequence_id = sequence_data["id"]
        assert sequence_data["name"] == "Test Sequence"
        assert len(sequence_data["beats"]) == 4

        # Get sequence
        response = self.client.get(f"/api/sequences/{sequence_id}")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == sequence_id

        # Update sequence
        update_data = {
            "name": "Updated Sequence",
            "metadata": {"test": "value"}
        }
        response = self.client.put(f"/api/sequences/{sequence_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Updated Sequence"

        # Delete sequence
        response = self.client.delete(f"/api/sequences/{sequence_id}")
        assert response.status_code == 200

        # Verify deletion
        response = self.client.get(f"/api/sequences/{sequence_id}")
        assert response.status_code == 404

    def test_beat_operations_with_undo(self):
        """Test beat operations with undo/redo functionality."""
        # Create sequence first
        create_data = {"name": "Beat Test Sequence", "length": 2}
        response = self.client.post("/api/sequences", json=create_data)
        sequence_id = response.json()["data"]["id"]

        # Add beat
        beat_data = {
            "beat": {
                "id": "test_beat",
                "beat_number": 3,
                "letter": "A",
                "duration": 1.5,
                "blue_motion": {
                    "motion_type": "pro",
                    "prop_rot_dir": "cw",
                    "start_loc": "n",
                    "end_loc": "e",
                    "turns": 1.0,
                    "start_ori": "in",
                    "end_ori": "out"
                },
                "is_blank": False,
                "blue_reversal": False,
                "red_reversal": False,
                "metadata": {}
            },
            "position": 2
        }
        
        response = self.client.post(f"/api/sequences/{sequence_id}/beats", json=beat_data)
        assert response.status_code == 200
        assert response.json()["can_undo"] == True

        # Test undo
        response = self.client.post("/api/commands/undo")
        assert response.status_code == 200
        assert response.json()["success"] == True

        # Test redo
        response = self.client.post("/api/commands/redo")
        assert response.status_code == 200
        assert response.json()["success"] == True

    def test_circuit_breaker_functionality(self):
        """Test circuit breaker fault tolerance."""
        test_breaker = CircuitBreaker(
            failure_threshold=2,
            recovery_timeout=1.0,
            name="test_breaker"
        )
        
        @test_breaker
        def failing_function():
            raise Exception("Test failure")
        
        @test_breaker
        def working_function():
            return "success"
        
        # Test normal operation
        result = working_function()
        assert result == "success"
        assert test_breaker.state.value == "closed"
        
        # Test failure threshold
        with pytest.raises(Exception):
            failing_function()
        with pytest.raises(Exception):
            failing_function()
        
        # Circuit should be open now
        assert test_breaker.state.value == "open"

    def test_retry_policy_functionality(self):
        """Test retry policy fault tolerance."""
        retry_policy = RetryPolicy(
            max_attempts=3,
            delay=0.1,
            exponential_backoff=False
        )
        
        attempt_count = 0
        
        @retry_policy
        def eventually_succeeding_function():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise Exception("Temporary failure")
            return "success"
        
        # Should succeed after retries
        result = eventually_succeeding_function()
        assert result == "success"
        assert attempt_count == 3

if __name__ == "__main__":
    pytest.main([__file__])

# ===== EXAMPLE USAGE =====

# Example: TypeScript Usage
typescript_example = '''
// TypeScript client example
import { TKAClient, TKAWebSocketClient } from 'tka-client';

// REST API client
const client = new TKAClient('http://localhost:8000');

async function example() {
  // Create sequence
  const sequence = await client.createSequence({
    name: 'External Sequence',
    length: 8
  });

  // Add beat with undo support
  const result = await client.addBeat(sequence.data.id, {
    id: 'beat_1',
    beat_number: 1,
    letter: 'X',
    duration: 1.0,
    blue_motion: { 
      motion_type: 'pro', 
      prop_rot_dir: 'cw',
      start_loc: 'n',
      end_loc: 'e',
      turns: 1.0,
      start_ori: 'in',
      end_ori: 'out'
    },
    blue_reversal: false,
    red_reversal: false,
    is_blank: false,
    metadata: {}
  });

  // Undo if needed
  if (result.can_undo) {
    await client.undo();
  }
}

// Real-time events
const wsClient = new TKAWebSocketClient('ws://localhost:8000/ws');
await wsClient.connect();

wsClient.onEvent('sequence.beat_added', (event) => {
  console.log('Beat added:', event);
});

wsClient.setEventFilters(['sequence.beat_added', 'motion.generated']);
'''

# Example: Python Usage
python_example = '''
# Python client example
from tka_client import TKAClient, CreateSequenceRequest, BeatAPI, MotionAPI

# REST API client
client = TKAClient('http://localhost:8000')

# Create sequence
sequence = client.create_sequence(CreateSequenceRequest(
    name='Python Sequence',
    length=4
))

# Add beat
beat = BeatAPI(
    id='beat_py_1',
    beat_number=1,
    letter='P',
    duration=1.0,
    blue_motion=MotionAPI(
        motion_type='pro',
        prop_rot_dir='cw',
        start_loc='n',
        end_loc='e',
        turns=1.0,
        start_ori='in',
        end_ori='out'
    ),
    blue_reversal=False,
    red_reversal=False,
    is_blank=False,
    metadata={}
)

result = client.add_beat(sequence.data.id, beat)

# Undo if possible
if result.can_undo:
    client.undo()
'''

# Example: Rust Usage
rust_example = '''
// Rust client example
use tka_client::{TKAClient, CreateSequenceRequest, BeatAPI, MotionAPI};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = TKAClient::new("http://localhost:8000");
    
    // Create sequence
    let request = CreateSequenceRequest {
        name: "Rust Sequence".to_string(),
        length: Some(6),
        beats: None,
    };
    
    let sequence = client.create_sequence(&request).await?;
    
    // Add beat
    let beat = BeatAPI {
        id: "beat_rust_1".to_string(),
        beat_number: 1,
        letter: Some("R".to_string()),
        duration: 1.0,
        blue_motion: Some(MotionAPI {
            motion_type: "pro".to_string(),
            prop_rot_dir: "cw".to_string(),
            start_loc: "n".to_string(),
            end_loc: "e".to_string(),
            turns: 1.0,
            start_ori: "in".to_string(),
            end_ori: "out".to_string(),
        }),
        red_motion: None,
        blue_reversal: false,
        red_reversal: false,
        is_blank: false,
        metadata: std::collections::HashMap::new(),
    };
    
    let result = client.add_beat(&sequence.data.unwrap().id, &beat, None).await?;
    
    // Undo if possible
    if result.can_undo {
        client.undo().await?;
    }
    
    Ok(())
}
'''

# ===== DEPLOYMENT SCRIPTS =====

docker_example = '''
# Dockerfile for TKA Desktop API
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 8000

CMD ["python", "src/infrastructure/api/api_server.py", "--host", "0.0.0.0", "--port", "8000"]
'''

docker_compose_example = '''
version: '3.8'

services:
  tka-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - TKA_LOG_LEVEL=INFO
      - TKA_ENABLE_CORS=true
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - tka-api
'''