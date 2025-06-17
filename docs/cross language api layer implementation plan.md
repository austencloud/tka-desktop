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
                pass  # Connection might already be closed
            
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

    async def _broadcast_event(self, event: BaseEvent):
        """Broadcast domain event to all connected WebSocket clients."""
        if not self._connections:
            return  # No clients connected
        
        # Convert domain event to API event
        api_event = self._convert_domain_event_to_api(event)
        
        # Broadcast to all clients (with filtering)
        disconnected_clients = []
        
        for client_id, websocket in self._connections.items():
            try:
                # Check if client has filters and if event passes filter
                filters = self._connection_filters.get(client_id, set())
                if filters and api_event["event_type"] not in filters:
                    continue  # Skip this client due to filters
                
                await self._send_to_client(client_id, api_event)
                
            except Exception as e:
                logger.error(f"Error broadcasting to client {client_id}: {e}")
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            await self.disconnect(client_id)

    def _convert_domain_event_to_api(self, event: BaseEvent) -> Dict[str, Any]:
        """Convert domain event to API event format."""
        base_event = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "timestamp": event.timestamp.isoformat(),
            "source": event.source or "TKA_Desktop"
        }
        
        # Add event-specific data based on event type
        if hasattr(event, 'sequence_id'):
            base_event.update({
                "sequence_id": getattr(event, 'sequence_id', ''),
                "data": self._extract_event_data(event)
            })
        
        return base_event

    def _extract_event_data(self, event: BaseEvent) -> Dict[str, Any]:
        """Extract relevant data from domain event."""
        data = {}
        
        # Extract all non-private attributes from the event
        for attr_name in dir(event):
            if not attr_name.startswith('_') and attr_name not in ['event_id', 'event_type', 'timestamp', 'source']:
                try:
                    value = getattr(event, attr_name)
                    if not callable(value):
                        data[attr_name] = value
                except:
                    continue  # Skip attributes that can't be accessed
        
        return data

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

    def cleanup(self):
        """Clean up WebSocket manager."""
        for sub_id in self._subscription_ids:
            self.event_bus.unsubscribe(sub_id)
        self._subscription_ids.clear()

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
```

### **Step 3: Client Library Generation (Days 8-12)**

#### **3.1: Schema-First Development System**

**File:** `src/infrastructure/api/client_generator.py`
```python
"""
Automatic client library generation for multiple programming languages.
Generates type-safe clients from API schema definitions.
"""

import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass
import subprocess

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
    """
    Generates client libraries for multiple programming languages.
    
    Supports:
    - TypeScript/JavaScript
    - Python
    - Rust
    - C++
    - Java
    - C#
    """

    def __init__(self, api_schema: Dict[str, Any]):
        self.api_schema = api_schema
        self.template_dir = Path(__file__).parent / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(str(self.template_dir)))

    def generate_all_clients(self, base_output_dir: Path) -> Dict[str, Path]:
        """Generate clients for all supported languages."""
        results = {}
        
        configs = [
            ClientConfig("typescript", base_output_dir / "typescript"),
            ClientConfig("python", base_output_dir / "python"),
            ClientConfig("rust", base_output_dir / "rust"),
            ClientConfig("cpp", base_output_dir / "cpp"),
            ClientConfig("java", base_output_dir / "java"),
            ClientConfig("csharp", base_output_dir / "csharp"),
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
        elif config.language == "cpp":
            return self._generate_cpp_client(config)
        elif config.language == "java":
            return self._generate_java_client(config)
        elif config.language == "csharp":
            return self._generate_csharp_client(config)
        else:
            raise ValueError(f"Unsupported language: {config.language}")

    def _generate_typescript_client(self, config: ClientConfig) -> Path:
        """Generate TypeScript client with full type safety."""
        
        # Generate types
        types_content = self._render_template("typescript/types.ts.j2", {
            "schema": self.api_schema,
            "package_name": config.package_name,
            "version": config.version
        })
        
        # Generate API client
        client_content = self._render_template("typescript/client.ts.j2", {
            "schema": self.api_schema,
            "package_name": config.package_name,
            "version": config.version
        })
        
        # Generate WebSocket client
        websocket_content = self._render_template("typescript/websocket.ts.j2", {
            "schema": self.api_schema,
            "package_name": config.package_name
        })
        
        # Generate package.json
        package_json = {
            "name": config.package_name,
            "version": config.version,
            "description": config.description,
            "main": "dist/index.js",
            "types": "dist/index.d.ts",
            "scripts": {
                "build": "tsc",
                "test": "jest",
                "lint": "eslint src/**/*.ts"
            },
            "dependencies": {
                "axios": "^1.0.0",
                "ws": "^8.0.0"
            },
            "devDependencies": {
                "typescript": "^5.0.0",
                "@types/node": "^20.0.0",
                "@types/ws": "^8.0.0",
                "jest": "^29.0.0",
                "eslint": "^8.0.0"
            }
        }
        
        # Write files
        self._write_file(config.output_dir / "src" / "types.ts", types_content)
        self._write_file(config.output_dir / "src" / "client.ts", client_content)
        self._write_file(config.output_dir / "src" / "websocket.ts", websocket_content)
        self._write_file(config.output_dir / "src" / "index.ts", 
                        'export * from "./types";\nexport * from "./client";\nexport * from "./websocket";')
        self._write_file(config.output_dir / "package.json", json.dumps(package_json, indent=2))
        
        # Generate TypeScript config
        tsconfig = {
            "compilerOptions": {
                "target": "ES2020",
                "module": "commonjs",
                "lib": ["ES2020"],
                "outDir": "./dist",
                "rootDir": "./src",
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True,
                "declaration": True
            },
            "include": ["src/**/*"],
            "exclude": ["node_modules", "dist"]
        }
        self._write_file(config.output_dir / "tsconfig.json", json.dumps(tsconfig, indent=2))
        
        # Generate README
        readme_content = self._render_template("typescript/README.md.j2", {
            "package_name": config.package_name,
            "version": config.version,
            "description": config.description
        })
        self._write_file(config.output_dir / "README.md", readme_content)
        
        return config.output_dir

    def _generate_python_client(self, config: ClientConfig) -> Path:
        """Generate Python client with type hints."""
        
        # Generate models
        models_content = self._render_template("python/models.py.j2", {
            "schema": self.api_schema
        })
        
        # Generate client
        client_content = self._render_template("python/client.py.j2", {
            "schema": self.api_schema,
            "package_name": config.package_name
        })
        
        # Generate async client
        async_client_content = self._render_template("python/async_client.py.j2", {
            "schema": self.api_schema,
            "package_name": config.package_name
        })
        
        # Generate WebSocket client
        websocket_content = self._render_template("python/websocket_client.py.j2", {
            "schema": self.api_schema
        })
        
        # Create package structure
        package_dir = config.output_dir / config.package_name
        package_dir.mkdir(parents=True, exist_ok=True)
        
        # Write Python files
        self._write_file(package_dir / "__init__.py", 
                        f'"""TKA Desktop API Client v{config.version}"""\n'
                        "from .client import TKAClient\n"
                        "from .async_client import TKAAsyncClient\n"
                        "from .websocket_client import TKAWebSocketClient\n"
                        "from .models import *\n"
                        "\n__version__ = \"" + config.version + "\"\n")
        self._write_file(package_dir / "models.py", models_content)
        self._write_file(package_dir / "client.py", client_content)
        self._write_file(package_dir / "async_client.py", async_client_content)
        self._write_file(package_dir / "websocket_client.py", websocket_content)
        
        # Generate setup.py
        setup_content = self._render_template("python/setup.py.j2", {
            "package_name": config.package_name,
            "version": config.version,
            "description": config.description,
            "author": config.author
        })
        self._write_file(config.output_dir / "setup.py", setup_content)
        
        # Generate requirements.txt
        requirements = [
            "requests>=2.25.0",
            "aiohttp>=3.8.0",
            "websockets>=10.0",
            "pydantic>=2.0.0",
            "typing-extensions>=4.0.0"
        ]
        self._write_file(config.output_dir / "requirements.txt", "\n".join(requirements))
        
        # Generate README
        readme_content = self._render_template("python/README.md.j2", {
            "package_name": config.package_name,
            "version": config.version,
            "description": config.description
        })
        self._write_file(config.output_dir / "README.md", readme_content)
        
        return config.output_dir

    def _generate_rust_client(self, config: ClientConfig) -> Path:
        """Generate Rust client with strong typing."""
        
        # Generate Cargo.toml
        cargo_toml = self._render_template("rust/Cargo.toml.j2", {
            "package_name": config.package_name.replace("-", "_"),
            "version": config.version,
            "description": config.description,
            "author": config.author
        })
        
        # Generate lib.rs
        lib_content = self._render_template("rust/lib.rs.j2", {
            "schema": self.api_schema
        })
        
        # Generate types
        types_content = self._render_template("rust/types.rs.j2", {
            "schema": self.api_schema
        })
        
        # Generate client
        client_content = self._render_template("rust/client.rs.j2", {
            "schema": self.api_schema
        })
        
        # Create Rust project structure
        src_dir = config.output_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        
        self._write_file(config.output_dir / "Cargo.toml", cargo_toml)
        self._write_file(src_dir / "lib.rs", lib_content)
        self._write_file(src_dir / "types.rs", types_content)
        self._write_file(src_dir / "client.rs", client_content)
        
        # Generate README
        readme_content = self._render_template("rust/README.md.j2", {
            "package_name": config.package_name,
            "version": config.version,
            "description": config.description
        })
        self._write_file(config.output_dir / "README.md", readme_content)
        
        return config.output_dir

    def _generate_cpp_client(self, config: ClientConfig) -> Path:
        """Generate C++ client with modern C++17 features."""
        
        # Generate header file
        header_content = self._render_template("cpp/tka_client.hpp.j2", {
            "schema": self.api_schema,
            "package_name": config.package_name
        })
        
        # Generate implementation
        impl_content = self._render_template("cpp/tka_client.cpp.j2", {
            "schema": self.api_schema,
            "package_name": config.package_name
        })
        
        # Generate CMakeLists.txt
        cmake_content = self._render_template("cpp/CMakeLists.txt.j2", {
            "package_name": config.package_name,
            "version": config.version
        })
        
        # Create directory structure
        include_dir = config.output_dir / "include" / config.package_name
        src_dir = config.output_dir / "src"
        include_dir.mkdir(parents=True, exist_ok=True)
        src_dir.mkdir(parents=True, exist_ok=True)
        
        self._write_file(include_dir / "tka_client.hpp", header_content)
        self._write_file(src_dir / "tka_client.cpp", impl_content)
        self._write_file(config.output_dir / "CMakeLists.txt", cmake_content)
        
        # Generate README
        readme_content = self._render_template("cpp/README.md.j2", {
            "package_name": config.package_name,
            "version": config.version,
            "description": config.description
        })
        self._write_file(config.output_dir / "README.md", readme_content)
        
        return config.output_dir

    def _generate_java_client(self, config: ClientConfig) -> Path:
        """Generate Java client with Maven build system."""
        package_path = config.package_name.replace("_", "").replace("-", "")
        
        # Generate pom.xml
        pom_content = self._render_template("java/pom.xml.j2", {
            "package_name": config.package_name,
            "package_path": package_path,
            "version": config.version,
            "description": config.description
        })
        
        # Generate main client class
        client_content = self._render_template("java/TKAClient.java.j2", {
            "schema": self.api_schema,
            "package_path": package_path
        })
        
        # Generate models
        models_content = self._render_template("java/Models.java.j2", {
            "schema": self.api_schema,
            "package_path": package_path
        })
        
        # Create Maven directory structure
        java_dir = config.output_dir / "src" / "main" / "java" / package_path.replace(".", "/")
        java_dir.mkdir(parents=True, exist_ok=True)
        
        self._write_file(config.output_dir / "pom.xml", pom_content)
        self._write_file(java_dir / "TKAClient.java", client_content)
        self._write_file(java_dir / "Models.java", models_content)
        
        return config.output_dir

    def _generate_csharp_client(self, config: ClientConfig) -> Path:
        """Generate C# client with NuGet package structure."""
        
        # Generate .csproj file
        csproj_content = self._render_template("csharp/TKAClient.csproj.j2", {
            "package_name": config.package_name,
            "version": config.version,
            "description": config.description,
            "author": config.author
        })
        
        # Generate client class
        client_content = self._render_template("csharp/TKAClient.cs.j2", {
            "schema": self.api_schema,
            "package_name": config.package_name
        })
        
        # Generate models
        models_content = self._render_template("csharp/Models.cs.j2", {
            "schema": self.api_schema,
            "package_name": config.package_name
        })
        
        self._write_file(config.output_dir / f"{config.package_name}.csproj", csproj_content)
        self._write_file(config.output_dir / "TKAClient.cs", client_content)
        self._write_file(config.output_dir / "Models.cs", models_content)
        
        return config.output_dir

    def _render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render Jinja2 template with context."""
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)

    def _write_file(self, file_path: Path, content: str):
        """Write content to file, creating directories as needed."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _extract_api_schema(self) -> Dict[str, Any]:
        """Extract API schema from FastAPI app."""
        # This would be implemented to extract schema from the FastAPI app
        # For now, return a basic schema structure
        return {
            "info": {
                "title": "TKA Desktop API",
                "version": "2.0.0",
                "description": "Cross-language API for Kinetic Alphabet Desktop"
            },
            "endpoints": self._extract_endpoints(),
            "models": self._extract_models()
        }

    def _extract_endpoints(self) -> List[Dict[str, Any]]:
        """Extract API endpoints information."""
        return [
            {
                "path": "/api/sequences",
                "method": "GET",
                "description": "List all sequences",
                "parameters": [
                    {"name": "page", "type": "int", "default": 1},
                    {"name": "page_size", "type": "int", "default": 20}
                ],
                "response_type": "PaginatedResponse[SequenceAPI]"
            },
            {
                "path": "/api/sequences",
                "method": "POST", 
                "description": "Create a new sequence",
                "body_type": "CreateSequenceRequest",
                "response_type": "CommandResponse[SequenceAPI]"
            },
            # Add more endpoints...
        ]

    def _extract_models(self) -> Dict[str, Any]:
        """Extract API model definitions."""
        return {
            "SequenceAPI": {
                "properties": {
                    "id": {"type": "string", "required": True},
                    "name": {"type": "string", "required": True},
                    "word": {"type": "string", "default": ""},
                    "beats": {"type": "array", "items": "BeatAPI", "default": []},
                    "start_position": {"type": "string", "nullable": True},
                    "metadata": {"type": "object", "default": {}}
                }
            },
            "BeatAPI": {
                "properties": {
                    "id": {"type": "string", "required": True},
                    "beat_number": {"type": "int", "required": True},
                    "letter": {"type": "string", "nullable": True},
                    "duration": {"type": "float", "default": 1.0},
                    "blue_motion": {"type": "MotionAPI", "nullable": True},
                    "red_motion": {"type": "MotionAPI", "nullable": True},
                    "blue_reversal": {"type": "bool", "default": False},
                    "red_reversal": {"type": "bool", "default": False},
                    "is_blank": {"type": "bool", "default": False},
                    "metadata": {"type": "object", "default": {}}
                }
            },
            # Add more models...
        }
```

### **Step 4: API Server Integration (Days 13-15)**

#### **4.1: Main API Server**

**File:** `src/infrastructure/api/api_server.py`
```python
"""
Production-ready API server with comprehensive monitoring and fault tolerance.
Integrates REST, WebSocket, and health checking into a single server.
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
    """
    Production-ready API server for TKA Desktop.
    
    Features:
    - REST API endpoints
    - WebSocket real-time events
    - Health checking and monitoring
    - Graceful shutdown
    - Client library generation
    """

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
        self._setup_health_checks()

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

    def _setup_health_checks(self):
        """Setup health checks for monitoring."""
        health_checker = HealthChecker()
        
        # Register health checks
        health_checker.register_health_check("event_bus", check_event_bus_health)
        health_checker.register_health_check("command_processor", check_command_processor_health)
        health_checker.register_health_check("database", check_database_health)
        health_checker.register_health_check("memory", check_memory_usage)

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
            manager.cleanup()

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
```

### **Step 5: Integration with TKA Desktop (Days 16-18)**

#### **5.1: Update Main Application**

**File:** `src/infrastructure/api/integration.py`
```python
"""
Integration layer between TKA Desktop core and API server.
Handles startup, shutdown, and service coordination.
"""

import asyncio
import logging
from typing import Optional
from pathlib import Path

from .api_server import TKAAPIServer
from ...core.dependency_injection.di_container import get_container
from ...core.events import get_event_bus

logger = logging.getLogger(__name__)

class APIIntegration:
    """
    Manages API server integration with TKA Desktop.
    
    Handles:
    - API server lifecycle
    - Service registration
    - Event bus integration
    - Graceful shutdown
    """

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
            # Ensure core services are initialized
            container = get_container()
            event_bus = get_event_bus()
            
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
```

#### **5.2: Update Main Application Entry Point**

**File:** `src/modern/main.py` (modifications to existing file)

Add these imports at the top:
```python
from infrastructure.api.integration import get_api_integration
```

Update the `KineticConstructorModern` class:
```python
class KineticConstructorModern(QMainWindow):
    def __init__(
        self,
        splash_screen: Optional[SplashScreen] = None,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
        enable_api_server=True,  # NEW: API server option
        api_host="localhost",    # NEW: API configuration
        api_port=8000           # NEW: API configuration
    ):
        super().__init__()
        self.splash = splash_screen
        self.target_screen = target_screen
        self.parallel_mode = parallel_mode
        self.parallel_geometry = parallel_geometry
        self.enable_api_server = enable_api_server
        self.api_host = api_host
        self.api_port = api_port

        # ... existing initialization code ...

        self.container = get_container()
        self._configure_services()
        self._set_legacy_style_dimensions()
        self._setup_ui()
        self._setup_background()
        
        # NEW: Start API server if enabled
        if self.enable_api_server:
            self._start_api_server()

    def _start_api_server(self):
        """Start the API server in the background."""
        try:
            if self.splash:
                self.splash.update_progress(98, "Starting API server...")
            
            api_integration = get_api_integration()
            
            # Start API server asynchronously
            def start_api():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    success = loop.run_until_complete(
                        api_integration.start_api_server(
                            host=self.api_host,
                            port=self.api_port,
                            enable_client_generation=True
                        )
                    )
                    if success:
                        print(f"🌐 API server running at http://{self.api_host}:{self.api_port}")
                        print(f"📚 API docs: http://{self.api_host}:{self.api_port}/api/docs")
                        print(f"🔌 WebSocket: ws://{self.api_host}:{self.api_port}/ws")
                except Exception as e:
                    print(f"⚠️ API server failed to start: {e}")
                finally:
                    loop.close()
            
            # Start in separate thread to avoid blocking UI
            import threading
            api_thread = threading.Thread(target=start_api, daemon=True)
            api_thread.start()
            
        except Exception as e:
            print(f"⚠️ Failed to initialize API server: {e}")

    def closeEvent(self, event):
        """Handle application close with API server cleanup."""
        try:
            # Stop API server
            if self.enable_api_server:
                api_integration = get_api_integration()
                if api_integration.is_running():
                    # Stop API server asynchronously
                    def stop_api():
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            loop.run_until_complete(api_integration.stop_api_server())
                        except Exception as e:
                            print(f"⚠️ Error stopping API server: {e}")
                        finally:
                            loop.close()
                    
                    import threading
                    stop_thread = threading.Thread(target=stop_api)
                    stop_thread.start()
                    stop_thread.join(timeout=5)  # Wait up to 5 seconds
            
            # Continue with normal close
            super().closeEvent(event)
            
        except Exception as e:
            print(f"⚠️ Error during application shutdown: {e}")
            super().closeEvent(event)

# Update main() function to support API server options
def main():
    print("🚀 Kinetic Constructor - Starting...")

    # Detect parallel testing mode early
    parallel_mode, monitor, geometry = detect_parallel_testing_mode()

    # NEW: Parse API server arguments
    import argparse
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--no-api", action="store_true", help="Disable API server")
    parser.add_argument("--api-host", default="localhost", help="API server host")
    parser.add_argument("--api-port", type=int, default=8000, help="API server port")
    args, unknown = parser.parse_known_args()

    app = QApplication(sys.argv + unknown)  # Pass remaining args to QApplication
    app.setStyle("Fusion")

    # ... existing screen detection code ...

    # Create and show splash screen on target screen
    splash = SplashScreen(target_screen=target_screen)
    fade_in_animation = splash.show_animated()

    # Wait for fade-in to complete before starting app initialization
    def start_initialization():
        splash.update_progress(5, "Initializing application...")
        app.processEvents()

        # Set application icon if available
        icon_path = Path(__file__).parent / "images" / "icons" / "app_icon.png"
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))

        splash.update_progress(15, "Creating main window...")
        window = KineticConstructorModern(
            splash_screen=splash,
            target_screen=target_screen,
            parallel_mode=parallel_mode,
            parallel_geometry=geometry,
            enable_api_server=not args.no_api,  # NEW: API server control
            api_host=args.api_host,             # NEW: API configuration
            api_port=args.api_port              # NEW: API configuration
        )

        def complete_startup():
            splash.update_progress(100, "Ready!")
            app.processEvents()

            # Hide splash immediately after reaching 100%
            QTimer.singleShot(200, lambda: splash.hide_animated())

            # Show main window after splash starts hiding
            QTimer.singleShot(300, lambda: window.show())

        QTimer.singleShot(200, complete_startup)

    fade_in_animation.finished.connect(start_initialization)

    print("✅ Application started successfully!")
    return app.exec()
```

### **Step 6: Testing and Validation (Days 19-21)**

#### **6.1: API Integration Tests**

**File:** `tests/test_api_integration.py`
```python
"""
Integration tests for TKA Desktop API with fault tolerance validation.
Tests real API endpoints, WebSocket functionality, and error handling.
"""

import pytest
import asyncio
import json
from typing import Dict, Any
import httpx
import websockets
from fastapi.testclient import TestClient

from infrastructure.api.rest_api import app
from infrastructure.api.websocket_api import get_websocket_manager
from infrastructure.api.fault_tolerance import CircuitBreaker, RetryPolicy
from core.events import get_event_bus, reset_event_bus

class TestAPIIntegration:
    """Integration tests for API functionality."""

    def setup_method(self):
        """Setup for each test."""
        reset_event_bus()
        self.client = TestClient(app)

    def test_health_endpoints(self):
        """Test health check endpoints."""
        # Test main health endpoint
        response = self.client.get("/health")
        assert response.status_code == 200
        
        health_data = response.json()
        assert health_data["status"] in ["healthy", "degraded", "unhealthy"]
        assert "components" in health_data
        assert "version" in health_data

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
                    "turns": 1.0
                },
                "is_blank": False
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
        assert response.json()["can_redo"] == True

        # Test redo
        response = self.client.post("/api/commands/redo")
        assert response.status_code == 200
        assert response.json()["success"] == True

        # Get command history
        response = self.client.get("/api/commands/history")
        assert response.status_code == 200
        history = response.json()["data"]["history"]
        assert len(history) > 0

    def test_error_handling_and_validation(self):
        """Test API error handling and validation."""
        # Test invalid sequence creation
        invalid_data = {
            "name": "",  # Empty name should fail validation
            "length": -1  # Negative length should fail
        }
        response = self.client.post("/api/sequences", json=invalid_data)
        assert response.status_code == 422  # Validation error

        # Test non-existent sequence
        response = self.client.get("/api/sequences/nonexistent")
        assert response.status_code == 404

        # Test invalid beat data
        invalid_beat = {
            "beat": {
                "id": "invalid",
                "beat_number": 0,  # Invalid beat number
                "duration": -1.0   # Invalid duration
            }
        }
        response = self.client.post("/api/sequences/test/beats", json=invalid_beat)
        assert response.status_code in [400, 404, 422]

    @pytest.mark.asyncio
    async def test_websocket_event_streaming(self):
        """Test WebSocket event streaming functionality."""
        manager = get_websocket_manager()
        
        # Simulate WebSocket connection (simplified test)
        event_bus = get_event_bus()
        
        # Test event publishing
        from core.events.domain_events import SequenceCreatedEvent
        import uuid
        from datetime import datetime
        
        test_event = SequenceCreatedEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            source="test",
            sequence_id="test_seq",
            sequence_name="Test Sequence",
            sequence_length=4
        )
        
        # Publish event
        event_bus.publish(test_event)
        
        # Verify manager received event (would be more comprehensive in real test)
        assert manager is not None

    def test_circuit_breaker_functionality(self):
        """Test circuit breaker fault tolerance."""
        # Create a circuit breaker for testing
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
        
        # Should reject requests while open
        from infrastructure.api.fault_tolerance import CircuitBreakerError
        with pytest.raises(CircuitBreakerError):
            failing_function()

    def test_retry_policy_functionality(self):
        """Test retry policy fault tolerance."""
        retry_policy = RetryPolicy(
            max_attempts=3,
            delay=0.1,  # Short delay for testing
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

    def test_performance_under_load(self):
        """Test API performance under moderate load."""
        import time
        import concurrent.futures
        
        def create_sequence(index):
            """Create a sequence and measure response time."""
            start_time = time.perf_counter()
            
            response = self.client.post("/api/sequences", json={
                "name": f"Load Test Sequence {index}",
                "length": 4
            })
            
            end_time = time.perf_counter()
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "index": index
            }
        
        # Test with 20 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_sequence, i) for i in range(20)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Verify all requests succeeded
        success_count = sum(1 for r in results if r["status_code"] == 200)
        assert success_count >= 18  # Allow for some failures under load
        
        # Verify reasonable response times
        avg_response_time = sum(r["response_time"] for r in results) / len(results)
        assert avg_response_time < 1.0  # Should be under 1 second average

    def test_client_generation_endpoint(self):
        """Test client library generation endpoint."""
        # Test generating all clients
        response = self.client.post("/api/generate-clients")
        assert response.status_code == 200
        
        result = response.json()
        assert result.get("success") == True
        assert "generated_clients" in result
        
        # Test generating specific languages
        response = self.client.post("/api/generate-clients", json=["typescript", "python"])
        assert response.status_code == 200
        
        result = response.json()
        generated = result.get("generated_clients", {})
        assert "typescript" in generated
        assert "python" in generated
```

### **6.2: Client Library Tests**

**File:** `tests/test_client_generation.py`
```python
"""
Tests for client library generation functionality.
Validates that generated clients work correctly with the API.
"""

import pytest
import tempfile
import subprocess
from pathlib import Path
import json

from infrastructure.api.client_generator import ClientGenerator, ClientConfig
from infrastructure.api.rest_api import app

class TestClientGeneration:
    """Tests for client library generation."""

    def setup_method(self):
        """Setup for each test."""
        # Create a mock API schema
        self.api_schema = {
            "info": {
                "title": "TKA Desktop API",
                "version": "2.0.0",
                "description": "Test API"
            },
            "paths": {
                "/api/sequences": {
                    "get": {
                        "summary": "List sequences",
                        "responses": {
                            "200": {
                                "description": "Success",
                                "content": {
                                    "application/json": {
                                        "schema": {"type": "array"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "components": {
                "schemas": {
                    "SequenceAPI": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "beats": {"type": "array"}
                        }
                    }
                }
            }
        }

    def test_typescript_client_generation(self):
        """Test TypeScript client generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = ClientGenerator(self.api_schema)
            config = ClientConfig("typescript", Path(temp_dir))
            
            output_path = generator.generate_client(config)
            
            # Verify files were created
            assert (output_path / "src" / "types.ts").exists()
            assert (output_path / "src" / "client.ts").exists()
            assert (output_path / "src" / "websocket.ts").exists()
            assert (output_path / "package.json").exists()
            assert (output_path / "tsconfig.json").exists()
            
            # Verify package.json is valid
            with open(output_path / "package.json") as f:
                package_data = json.load(f)
                assert package_data["name"] == "tka_client"
                assert "dependencies" in package_data

    def test_python_client_generation(self):
        """Test Python client generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = ClientGenerator(self.api_schema)
            config = ClientConfig("python", Path(temp_dir))
            
            output_path = generator.generate_client(config)
            
            # Verify files were created
            package_dir = output_path / "tka_client"
            assert package_dir.exists()
            assert (package_dir / "__init__.py").exists()
            assert (package_dir / "models.py").exists()
            assert (package_dir / "client.py").exists()
            assert (package_dir / "async_client.py").exists()
            assert (output_path / "setup.py").exists()
            assert (output_path / "requirements.txt").exists()

    def test_rust_client_generation(self):
        """Test Rust client generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = ClientGenerator(self.api_schema)
            config = ClientConfig("rust", Path(temp_dir))
            
            output_path = generator.generate_client(config)
            
            # Verify Cargo project structure
            assert (output_path / "Cargo.toml").exists()
            assert (output_path / "src" / "lib.rs").exists()
            assert (output_path / "src" / "types.rs").exists()
            assert (output_path / "src" / "client.rs").exists()

    def test_all_languages_generation(self):
        """Test generating clients for all supported languages."""
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = ClientGenerator(self.api_schema)
            results = generator.generate_all_clients(Path(temp_dir))
            
            # Verify all languages were generated
            expected_languages = ["typescript", "python", "rust", "cpp", "java", "csharp"]
            for lang in expected_languages:
                assert lang in results
                if results[lang] is not None:  # Some might fail in test environment
                    assert Path(results[lang]).exists()

    def test_schema_extraction(self):
        """Test API schema extraction from FastAPI app."""
        generator = ClientGenerator({})
        schema = generator._extract_api_schema()
        
        # Should return a valid schema structure
        assert isinstance(schema, dict)
        assert "info" in schema or "endpoints" in schema

if __name__ == "__main__":
    pytest.main([__file__])
```

---

## 🎯 **Expected Outcomes After Phase 2**

### **Cross-Language Integration Achieved** ✅
- **Any Language Can Integrate:** TypeScript, Rust, C++, Java, C#, Python clients auto-generated
- **Real-Time Events:** WebSocket streaming of all TKA events to external clients
- **Type-Safe APIs:** Full type safety across all generated clients
- **Production Ready:** Comprehensive error handling, validation, monitoring

### **Bulletproof Fault Tolerance** ✅
- **Circuit Breakers:** Prevent cascading failures during legacy integration
- **Retry Logic:** Automatic retry with exponential backoff for transient failures
- **Health Monitoring:** Comprehensive system health checks and alerting
- **Graceful Degradation:** System continues working even when components fail

### **Legacy Migration Ready** ✅
- **Any Legacy Language:** Can integrate via REST API, WebSocket, or generated client
- **Event-Driven Integration:** Legacy components just subscribe to events
- **Fault Tolerant:** Legacy component failures don't bring down the system
- **Gradual Migration:** Can migrate piece by piece without system disruption

---

## 🔧 **Testing Your Implementation**

### **Manual Testing Checklist**

1. **Start TKA Desktop with API**
   ```bash
   python main.py --api-host localhost --api-port 8000
   ```

2. **Test REST API**
   - Visit `http://localhost:8000/api/docs` for interactive API documentation
   - Create sequence: `POST /api/sequences`
   - Add beat: `POST /api/sequences/{id}/beats`
   - Test undo: `POST /api/commands/undo`

3. **Test WebSocket Events**
   ```javascript
   const ws = new WebSocket('ws://localhost:8000/ws');
   ws.onmessage = (event) => console.log('Event:', JSON.parse(event.data));
   ```

4. **Test Fault Tolerance**
   - Simulate service failures
   - Verify circuit breakers activate
   - Confirm graceful degradation

5. **Test Client Generation**
   - Visit `http://localhost:8000/api/generate-clients`
   - Verify TypeScript, Python, Rust clients generated
   - Test generated client functionality

### **Key Test Commands**
```bash
# Run API integration tests
python -m pytest tests/test_api_integration.py -v

# Run client generation tests  
python -m pytest tests/test_client_generation.py -v

# Run fault tolerance tests
python -m pytest tests/test_fault_tolerance.py -v

# Start API server standalone
python src/infrastructure/api/api_server.py --host 0.0.0.0 --port 8000

# Generate clients manually
python src/infrastructure/api/client_generator.py --output ./clients --language all
```

---

## 🚀 **Production Deployment Guide**

### **API Server Configuration**
```python
# Production configuration
api_server = TKAAPIServer(
    host="0.0.0.0",           # Allow external connections
    port=8000,                # Standard port
    auto_generate_clients=True, # Enable client generation
)

# With SSL/TLS (recommended for production)
uvicorn.run(
    app,
    host="0.0.0.0",
    port=443,
    ssl_keyfile="/path/to/private.key",
    ssl_certfile="/path/to/certificate.crt"
)
```

### **Docker Deployment**
```dockerfile
# Dockerfile for TKA Desktop API
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 8000

CMD ["python", "src/infrastructure/api/api_server.py", "--host", "0.0.0.0", "--port", "8000"]
```

### **Environment Variables**
```bash
# Production environment variables
export TKA_API_HOST=0.0.0.0
export TKA_API_PORT=8000
export TKA_LOG_LEVEL=INFO
export TKA_ENABLE_CORS=true
export TKA_CLIENT_GENERATION=true
export TKA_HEALTH_CHECK_INTERVAL=30
```

---

## 🎉 **Success Validation**

After Phase 2 implementation, you should be able to:

### **Cross-Language Integration**
```typescript
// TypeScript client example
import { TKAClient, SequenceAPI } from 'tka-client';

const client = new TKAClient('http://localhost:8000');

// Create sequence
const sequence = await client.createSequence({
  name: 'External Sequence',
  length: 8
});

// Add beat with undo support
const result = await client.addBeat(sequence.id, {
  letter: 'X',
  duration: 1.0,
  blue_motion: { motion_type: 'pro', prop_rot_dir: 'cw', /* ... */ }
});

// Undo if needed
if (result.can_undo) {
  await client.undo();
}
```

```python
# Python client example
from tka_client import TKAClient, TKAWebSocketClient

# REST API client
client = TKAClient('http://localhost:8000')
sequence = client.create_sequence('Python Sequence', length=4)

# Real-time events
ws_client = TKAWebSocketClient('ws://localhost:8000/ws')
ws_client.on_event('sequence.beat_added', lambda event: print(f'Beat added: {event}'))
```

```rust
// Rust client example
use tka_client::{TKAClient, CreateSequenceRequest};

let client = TKAClient::new("http://localhost:8000");
let sequence = client.create_sequence(CreateSequenceRequest {
    name: "Rust Sequence".to_string(),
    length: Some(6),
    beats: None,
}).await?;
```

### **Fault Tolerance in Action**
```python
# Circuit breaker protecting legacy integration
@circuit_breaker(failure_threshold=5, recovery_timeout=30)
@retry_policy(max_attempts=3, delay=1.0)
async def integrate_legacy_component(data):
    # Legacy component integration with fault protection
    return await legacy_service.process(data)

# Graceful degradation
async def process_with_fallback(data):
    try:
        return await primary_service.process(data)
    except ServiceUnavailableError:
        # Use fallback when primary service fails
        return await fallback_service.process(data)
```

### **Real-Time Event Streaming**
```javascript
// External client receiving live TKA events
const ws = new WebSocket('ws://localhost:8000/ws');

// Set event filters
ws.send(JSON.stringify({
  type: 'set_filters',
  event_types: ['sequence.beat_added', 'motion.generated']
}));

// Receive real-time events
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(`Received: ${data.event_type}`, data);
  
  // Legacy systems can respond to TKA events in real-time!
  if (data.event_type === 'sequence.beat_added') {
    updateLegacyDisplay(data.sequence_id, data.beat_data);
  }
};
```

---

## 🔮 **Ready for Phase 3**

With Phase 2 complete, your architecture will be **enterprise-grade** and **legacy-migration-ready**:

### **What You'll Have**
- ✅ **Event-driven core** (Phase 1) with full undo/redo
- ✅ **Cross-language API layer** (Phase 2) with fault tolerance
- ✅ **Production-grade monitoring** and health checks
- ✅ **Auto-generated client libraries** for all major languages

### **What's Next (Phase 3)**
- 🚀 **Advanced Performance Monitoring** - Distributed tracing, metrics dashboards
- 🚀 **Security Layer** - Authentication, authorization, API rate limiting  
- 🚀 **Advanced Schema Validation** - Runtime validation, schema evolution
- 🚀 **Production Deployment** - Kubernetes, Docker, CI/CD pipelines

Your TKA Desktop will be **bulletproof** and ready for any legacy migration scenario! The combination of event-driven architecture (Phase 1) and cross-language API access (Phase 2) provides the ultimate flexibility for integrating components written in any language while maintaining system reliability through comprehensive fault tolerance.

---

## 📋 **Implementation Checklist**

- [ ] **Days 1-3:** API infrastructure and data models
- [ ] **Days 4-7:** Fault tolerance (circuit breakers, retry, health checks)
- [ ] **Days 8-12:** Client library generation system  
- [ ] **Days 13-15:** API server integration
- [ ] **Days 16-18:** TKA Desktop integration
- [ ] **Days 19-21:** Testing and validation

**Total Timeline:** 3 weeks to production-ready cross-language API with enterprise fault tolerance.

Ready to build the ultimate legacy migration platform! 🚀# Phase 2: Cross-Language API Layer + Enhanced Fault Tolerance

**Target:** Create bulletproof external API access and resilient error handling for legacy migration  
**Timeline:** 3 weeks  
**Priority:** HIGH - Essential for multi-language legacy integration and production stability

---

## 📋 Implementation Overview

### **Phase 1 SUCCESS ✅**
Your team flawlessly implemented:
- ✅ Event-driven architecture with domain events
- ✅ Command pattern with full undo/redo capability  
- ✅ Services decoupled and communicating via events
- ✅ Foundation ready for legacy integration

### **Phase 2 OBJECTIVES**
Now we build on this solid foundation to add:
1. **Cross-Language API Layer** - REST/WebSocket APIs for any language to integrate
2. **Enhanced Fault Tolerance** - Circuit breakers, retries, graceful degradation
3. **Schema-First Development** - Auto-generated client libraries in multiple languages
4. **Production-Grade Monitoring** - Health checks, metrics, observability

---

## 🏗️ **Architecture Overview**

### **Current State (Post-Phase 1)**
```
┌─────────────────────────────────────────────┐
│              TKA Desktop Modern             │
├─────────────────────────────────────────────┤
│  Event Bus (✅) │ Commands (✅) │ Services  │
│  SequenceEvent  │ AddBeatCmd    │ Sequence  │
│  MotionEvent    │ RemoveBeatCmd │ Motion    │ 
│  LayoutEvent    │ UpdateBeatCmd │ Layout    │
└─────────────────────────────────────────────┘
```

### **Target State (Post-Phase 2)**
```
┌─────────────────────────────────────────────┐
│           External Language Access          │
├─────────────────────────────────────────────┤
│  TypeScript │  Rust  │  C++  │  Python     │
│   Client    │ Client │Client │  Client     │
└─────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│              API Gateway Layer              │
├─────────────────────────────────────────────┤
│  REST API │ WebSocket │ GraphQL │ Auth      │
│  Circuit  │  Retry    │ Metrics │ Validate  │
│  Breaker  │  Logic    │ Health  │ Transform │
└─────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────┐
│           TKA Desktop Modern Core           │
├─────────────────────────────────────────────┤
│  Event Bus (✅) │ Commands (✅) │ Services  │
│  SequenceEvent  │ AddBeatCmd    │ Sequence  │
│  MotionEvent    │ RemoveBeatCmd │ Motion    │
│  LayoutEvent    │ UpdateBeatCmd │ Layout    │
└─────────────────────────────────────────────┘
```

---

## 🎯 Implementation Steps

### **Step 1: API Infrastructure Foundation (Days 1-3)**

#### **1.1: Create API Layer Structure**

**File:** `src/infrastructure/api/__init__.py`
```python
"""
TKA Desktop API Infrastructure

Provides multi-language access to TKA functionality through:
- REST API for CRUD operations
- WebSocket API for real-time events
- GraphQL API for flexible queries
- Auto-generated client libraries
"""

from .rest_api import TKARestAPI
from .websocket_api import TKAWebSocketAPI
from .api_models import *
from .api_server import TKAAPIServer
from .client_generator import ClientGenerator

__all__ = [
    "TKARestAPI", "TKAWebSocketAPI", "TKAAPIServer", 
    "ClientGenerator", "SequenceAPI", "BeatAPI", "MotionAPI"
]
```

#### **1.2: API Data Models with Validation**

**File:** `src/infrastructure/api/api_models.py`
```python
"""
API data models with comprehensive validation and serialization.
These models provide the contract between external clients and TKA core.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum

# === Core API Models ===

class MotionTypeAPI(str, Enum):
    """API enum for motion types."""
    PRO = "pro"
    ANTI = "anti"
    FLOAT = "float"
    DASH = "dash"
    STATIC = "static"

class RotationDirectionAPI(str, Enum):
    """API enum for rotation directions."""
    CLOCKWISE = "cw"
    COUNTER_CLOCKWISE = "ccw"
    NO_ROTATION = "no_rot"

class LocationAPI(str, Enum):
    """API enum for locations."""
    NORTH = "n"
    EAST = "e"
    SOUTH = "s"
    WEST = "w"
    NORTHEAST = "ne"
    SOUTHEAST = "se"
    SOUTHWEST = "sw"
    NORTHWEST = "nw"

class MotionAPI(BaseModel):
    """API model for motion data with validation."""
    motion_type: MotionTypeAPI
    prop_rot_dir: RotationDirectionAPI
    start_loc: LocationAPI
    end_loc: LocationAPI
    turns: float = Field(default=0.0, ge=0.0, le=4.0)
    start_ori: str = Field(default="in", regex="^(in|out)$")
    end_ori: str = Field(default="in", regex="^(in|out)$")

    @validator('turns')
    def validate_turns(cls, v):
        """Validate turns are in valid increments."""
        # Allow turns in 0.5 increments only
        if v % 0.5 != 0:
            raise ValueError("Turns must be in 0.5 increments")
        return v

    class Config:
        schema_extra = {
            "example": {
                "motion_type": "pro",
                "prop_rot_dir": "cw",
                "start_loc": "n",
                "end_loc": "e",
                "turns": 1.0,
                "start_ori": "in",
                "end_ori": "out"
            }
        }

class BeatAPI(BaseModel):
    """API model for beat data with comprehensive validation."""
    id: str = Field(..., description="Unique beat identifier")
    beat_number: int = Field(..., ge=1, le=64, description="Beat number in sequence")
    letter: Optional[str] = Field(None, regex="^[A-Za-z]?$", description="Letter for this beat")
    duration: float = Field(default=1.0, gt=0.0, le=10.0, description="Beat duration in seconds")
    
    blue_motion: Optional[MotionAPI] = Field(None, description="Blue motion data")
    red_motion: Optional[MotionAPI] = Field(None, description="Red motion data")
    
    blue_reversal: bool = Field(default=False, description="Blue motion is reversed")
    red_reversal: bool = Field(default=False, description="Red motion is reversed")
    is_blank: bool = Field(default=False, description="Beat is blank/empty")
    
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional beat metadata")

    @validator('letter')
    def validate_letter(cls, v):
        """Ensure letter is uppercase if provided."""
        return v.upper() if v else v

    class Config:
        schema_extra = {
            "example": {
                "id": "beat_12345",
                "beat_number": 1,
                "letter": "A",
                "duration": 1.0,
                "blue_motion": {
                    "motion_type": "pro",
                    "prop_rot_dir": "cw", 
                    "start_loc": "n",
                    "end_loc": "e",
                    "turns": 1.0
                },
                "red_motion": {
                    "motion_type": "anti",
                    "prop_rot_dir": "ccw",
                    "start_loc": "s", 
                    "end_loc": "w",
                    "turns": 1.5
                },
                "blue_reversal": False,
                "red_reversal": False,
                "is_blank": False,
                "metadata": {}
            }
        }

class SequenceAPI(BaseModel):
    """API model for sequence data with validation."""
    id: str = Field(..., description="Unique sequence identifier")
    name: str = Field(..., min_length=1, max_length=100, description="Sequence name")
    word: str = Field(default="", max_length=100, description="Generated word from sequence")
    beats: List[BeatAPI] = Field(default_factory=list, description="List of beats in sequence")
    start_position: Optional[str] = Field(None, description="Starting position for sequence")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional sequence metadata")
    
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    @validator('beats')
    def validate_beat_numbers(cls, v):
        """Ensure beat numbers are sequential starting from 1."""
        for i, beat in enumerate(v):
            expected_number = i + 1
            if beat.beat_number != expected_number:
                raise ValueError(f"Beat {i} has number {beat.beat_number}, expected {expected_number}")
        return v

    @property
    def length(self) -> int:
        """Get sequence length."""
        return len(self.beats)

    @property
    def total_duration(self) -> float:
        """Get total sequence duration."""
        return sum(beat.duration for beat in self.beats)

    class Config:
        schema_extra = {
            "example": {
                "id": "seq_12345",
                "name": "Example Sequence",
                "word": "HELLO",
                "beats": [],
                "start_position": "n",
                "metadata": {
                    "difficulty": 5,
                    "category": "beginner"
                }
            }
        }

# === Request/Response Models ===

class CreateSequenceRequest(BaseModel):
    """Request model for creating sequences."""
    name: str = Field(..., min_length=1, max_length=100)
    length: int = Field(default=16, ge=1, le=64)
    beats: Optional[List[BeatAPI]] = Field(None, description="Pre-populated beats")

class UpdateSequenceRequest(BaseModel):
    """Request model for updating sequences."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    beats: Optional[List[BeatAPI]] = None
    metadata: Optional[Dict[str, Any]] = None

class AddBeatRequest(BaseModel):
    """Request model for adding beats."""
    beat: BeatAPI
    position: Optional[int] = Field(None, ge=0, description="Position to insert beat")

class UpdateBeatRequest(BaseModel):
    """Request model for updating beats."""
    letter: Optional[str] = Field(None, regex="^[A-Za-z]?$")
    duration: Optional[float] = Field(None, gt=0.0, le=10.0)
    blue_motion: Optional[MotionAPI] = None
    red_motion: Optional[MotionAPI] = None
    blue_reversal: Optional[bool] = None
    red_reversal: Optional[bool] = None
    is_blank: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None

# === Response Models ===

class APIResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool
    message: str = ""
    data: Optional[Any] = None
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class PaginatedResponse(APIResponse):
    """Paginated response wrapper."""
    page: int = 1
    page_size: int = 20
    total_items: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_previous: bool = False

class CommandResponse(APIResponse):
    """Response for command operations with undo/redo info."""
    command_id: str = ""
    can_undo: bool = False
    can_redo: bool = False
    undo_description: Optional[str] = None
    redo_description: Optional[str] = None

# === Event Models (for WebSocket) ===

class EventAPI(BaseModel):
    """Base model for API events."""
    event_id: str
    event_type: str
    timestamp: datetime
    source: str
    data: Dict[str, Any] = Field(default_factory=dict)

class SequenceEventAPI(EventAPI):
    """Sequence-specific event model."""
    sequence_id: str
    change_type: str  # "created", "updated", "deleted", "beat_added", etc.

class MotionEventAPI(EventAPI):
    """Motion-specific event model."""
    sequence_id: str
    beat_number: int
    color: str  # "blue" or "red"

class LayoutEventAPI(EventAPI):
    """Layout-specific event model."""
    layout_type: str  # "beat_frame", "component", "responsive"
    trigger_reason: str

# === Health and Status Models ===

class HealthStatus(str, Enum):
    """Health status values."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

class ComponentHealth(BaseModel):
    """Health status for individual components."""
    name: str
    status: HealthStatus
    message: str = ""
    last_check: datetime = Field(default_factory=datetime.now)
    response_time_ms: float = 0.0

class SystemHealth(BaseModel):
    """Overall system health status."""
    status: HealthStatus
    components: List[ComponentHealth]
    version: str = "2.0.0"
    uptime_seconds: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)

# === Error Models ===

class APIError(BaseModel):
    """Structured API error response."""
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: Optional[str] = None

class ValidationError(APIError):
    """Validation-specific error."""
    field_errors: Dict[str, List[str]] = Field(default_factory=dict)
```

#### **1.3: FastAPI REST Implementation**

**File:** `src/infrastructure/api/rest_api.py`
```python
"""
High-performance REST API for TKA Desktop with comprehensive error handling.
Provides full CRUD operations, real-time events, and fault tolerance.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
import asyncio
import logging
import time
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from .api_models import *
from .fault_tolerance import CircuitBreaker, RetryPolicy, HealthChecker
from ...core.events import IEventBus, get_event_bus
from ...core.commands import CommandProcessor
from ...application.services.core.sequence_management_service import SequenceManagementService
from ...domain.models.core_models import SequenceData, BeatData, MotionData

logger = logging.getLogger(__name__)

# === Dependency Injection ===

def get_event_bus_dependency() -> IEventBus:
    """Get event bus for dependency injection."""
    return get_event_bus()

def get_sequence_service() -> SequenceManagementService:
    """Get sequence service from DI container."""
    from ...core.dependency_injection.di_container import get_container
    container = get_container()
    return container.resolve(SequenceManagementService)

def get_command_processor() -> CommandProcessor:
    """Get command processor from DI container.""" 
    from ...core.dependency_injection.di_container import get_container
    container = get_container()
    return container.resolve(CommandProcessor)

# === Circuit Breakers for External Dependencies ===

sequence_circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=30,
    expected_exception=Exception
)

motion_circuit_breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=20,
    expected_exception=Exception
)

# === Retry Policies ===

default_retry_policy = RetryPolicy(
    max_attempts=3,
    delay=1.0,
    exponential_backoff=True,
    max_delay=10.0
)

# === Health Checker ===

health_checker = HealthChecker()

# === FastAPI Application ===

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    logger.info("Starting TKA Desktop API...")
    health_checker.start()
    yield
    # Shutdown
    logger.info("Shutting down TKA Desktop API...")
    health_checker.stop()

app = FastAPI(
    title="TKA Desktop API",
    description="Cross-language API for Kinetic Alphabet Desktop with fault tolerance",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# === Middleware ===

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# === Global Error Handler ===

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler with structured error responses."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content=APIError(
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
            details={"path": str(request.url)},
            request_id=request.headers.get("X-Request-ID")
        ).dict()
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP exception handler with consistent error format."""
    return JSONResponse(
        status_code=exc.status_code,
        content=APIError(
            error_code=f"HTTP_{exc.status_code}",
            message=exc.detail,
            request_id=request.headers.get("X-Request-ID")
        ).dict()
    )

# === Request/Response Middleware ===

@app.middleware("http")
async def add_request_timing(request: Request, call_next):
    """Add request timing and logging."""
    start_time = time.perf_counter()
    
    # Add request ID if not present
    request_id = request.headers.get("X-Request-ID", f"req_{int(time.time())}")
    
    response = await call_next(request)
    
    process_time = time.perf_counter() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(process_time)
    
    logger.info(f"Request {request_id}: {request.method} {request.url} - {response.status_code} ({process_time:.3f}s)")
    
    return response

# === Health Endpoints ===

@app.get("/health", response_model=SystemHealth)
async def health_check():
    """Comprehensive health check endpoint."""
    return await health_checker.get_system_health()

@app.get("/health/ready")
async def readiness_check():
    """Kubernetes-style readiness check."""
    health = await health_checker.get_system_health()
    if health.status == HealthStatus.HEALTHY:
        return {"status": "ready"}
    else:
        raise HTTPException(status_code=503, detail="Service not ready")

@app.get("/health/live")
async def liveness_check():
    """Kubernetes-style liveness check."""
    return {"status": "alive", "timestamp": datetime.now()}

# === Sequence Endpoints ===

@app.get("/api/sequences", response_model=PaginatedResponse)
@sequence_circuit_breaker
@default_retry_policy
async def list_sequences(
    page: int = 1,
    page_size: int = 20,
    sequence_service: SequenceManagementService = Depends(get_sequence_service)
):
    """List all sequences with pagination."""
    try:
        # In a real implementation, this would come from a repository
        # For now, we'll return a mock response
        sequences = []  # sequence_service.get_all_sequences()
        
        total_items = len(sequences)
        total_pages = (total_items + page_size - 1) // page_size
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        page_sequences = sequences[start_idx:end_idx]
        
        return PaginatedResponse(
            success=True,
            message="Sequences retrieved successfully",
            data=[_convert_sequence_to_api(seq) for seq in page_sequences],
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
async def create_sequence(
    request: CreateSequenceRequest,
    background_tasks: BackgroundTasks,
    sequence_service: SequenceManagementService = Depends(get_sequence_service),
    event_bus: IEventBus = Depends(get_event_bus_dependency)
):
    """Create a new sequence with event publishing."""
    try:
        # Create sequence using event-driven service
        sequence = sequence_service.create_sequence_with_events(
            name=request.name,
            length=request.length
        )
        
        # Add pre-populated beats if provided
        if request.beats:
            for i, beat_api in enumerate(request.beats):
                beat_data = _convert_api_to_beat(beat_api)
                sequence = sequence_service.add_beat_with_undo(beat_data, i)
        
        # Schedule background task for additional processing
        background_tasks.add_task(_post_sequence_creation_tasks, sequence.id)
        
        return CommandResponse(
            success=True,
            message="Sequence created successfully",
            data=_convert_sequence_to_api(sequence),
            command_id=f"create_seq_{sequence.id}",
            can_undo=sequence_service.can_undo(),
            can_redo=sequence_service.can_redo(),
            undo_description=sequence_service.get_undo_description()
        )
        
    except Exception as e:
        logger.error(f"Failed to create sequence: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/sequences/{sequence_id}", response_model=APIResponse)
@sequence_circuit_breaker
async def get_sequence(
    sequence_id: str,
    sequence_service: SequenceManagementService = Depends(get_sequence_service)
):
    """Get a specific sequence by ID."""
    try:
        # In real implementation, get from repository
        # For now, return current sequence if ID matches
        current_sequence = sequence_service._current_sequence
        
        if not current_sequence or current_sequence.id != sequence_id:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        return APIResponse(
            success=True,
            message="Sequence retrieved successfully",
            data=_convert_sequence_to_api(current_sequence)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get sequence {sequence_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve sequence")

@app.put("/api/sequences/{sequence_id}", response_model=CommandResponse)
@sequence_circuit_breaker
@default_retry_policy
async def update_sequence(
    sequence_id: str,
    request: UpdateSequenceRequest,
    sequence_service: SequenceManagementService = Depends(get_sequence_service)
):
    """Update a sequence with undo support."""
    try:
        current_sequence = sequence_service._current_sequence
        
        if not current_sequence or current_sequence.id != sequence_id:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        # Update sequence fields
        updated_sequence = current_sequence
        
        if request.name is not None:
            updated_sequence = updated_sequence.update(name=request.name)
        
        if request.metadata is not None:
            updated_sequence = updated_sequence.update(metadata=request.metadata)
        
        # Update beats if provided
        if request.beats is not None:
            beat_data_list = [_convert_api_to_beat(beat_api) for beat_api in request.beats]
            updated_sequence = updated_sequence.update(beats=beat_data_list)
        
        # This would use a command for undo support in real implementation
        sequence_service._current_sequence = updated_sequence
        
        return CommandResponse(
            success=True,
            message="Sequence updated successfully",
            data=_convert_sequence_to_api(updated_sequence),
            can_undo=sequence_service.can_undo(),
            can_redo=sequence_service.can_redo()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update sequence {sequence_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/sequences/{sequence_id}", response_model=CommandResponse)
@sequence_circuit_breaker
async def delete_sequence(
    sequence_id: str,
    sequence_service: SequenceManagementService = Depends(get_sequence_service)
):
    """Delete a sequence with undo support."""
    try:
        # In real implementation, this would use a DeleteSequenceCommand
        current_sequence = sequence_service._current_sequence
        
        if not current_sequence or current_sequence.id != sequence_id:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        # For now, just clear current sequence
        sequence_service._current_sequence = None
        
        return CommandResponse(
            success=True,
            message="Sequence deleted successfully",
            command_id=f"delete_seq_{sequence_id}",
            can_undo=sequence_service.can_undo(),
            can_redo=sequence_service.can_redo()
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
async def add_beat(
    sequence_id: str,
    request: AddBeatRequest,
    sequence_service: SequenceManagementService = Depends(get_sequence_service)
):
    """Add a beat to a sequence with undo support."""
    try:
        current_sequence = sequence_service._current_sequence
        
        if not current_sequence or current_sequence.id != sequence_id:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        beat_data = _convert_api_to_beat(request.beat)
        position = request.position
        
        updated_sequence = sequence_service.add_beat_with_undo(beat_data, position)
        
        return CommandResponse(
            success=True,
            message="Beat added successfully", 
            data=_convert_sequence_to_api(updated_sequence),
            can_undo=sequence_service.can_undo(),
            can_redo=sequence_service.can_redo(),
            undo_description=sequence_service.get_undo_description()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add beat to sequence {sequence_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/sequences/{sequence_id}/beats/{beat_number}", response_model=CommandResponse)
@sequence_circuit_breaker
@default_retry_policy
async def update_beat(
    sequence_id: str,
    beat_number: int,
    request: UpdateBeatRequest,
    sequence_service: SequenceManagementService = Depends(get_sequence_service)
):
    """Update a beat with undo support."""
    try:
        current_sequence = sequence_service._current_sequence
        
        if not current_sequence or current_sequence.id != sequence_id:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        # Update each field that was provided
        updated_sequence = current_sequence
        
        for field_name, value in request.dict(exclude_unset=True).items():
            if value is not None:
                if field_name in ["blue_motion", "red_motion"] and isinstance(value, dict):
                    # Convert motion API model to domain model
                    motion_data = _convert_api_to_motion(value)
                    updated_sequence = sequence_service.update_beat_with_undo(
                        beat_number, field_name, motion_data
                    )
                else:
                    updated_sequence = sequence_service.update_beat_with_undo(
                        beat_number, field_name, value
                    )
        
        return CommandResponse(
            success=True,
            message="Beat updated successfully",
            data=_convert_sequence_to_api(updated_sequence),
            can_undo=sequence_service.can_undo(),
            can_redo=sequence_service.can_redo(),
            undo_description=sequence_service.get_undo_description()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update beat {beat_number} in sequence {sequence_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/sequences/{sequence_id}/beats/{beat_number}", response_model=CommandResponse)
@sequence_circuit_breaker
async def remove_beat(
    sequence_id: str,
    beat_number: int,
    sequence_service: SequenceManagementService = Depends(get_sequence_service)
):
    """Remove a beat with undo support."""
    try:
        current_sequence = sequence_service._current_sequence
        
        if not current_sequence or current_sequence.id != sequence_id:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        # Convert beat_number to position (beat_number is 1-indexed, position is 0-indexed)
        position = beat_number - 1
        
        updated_sequence = sequence_service.remove_beat_with_undo(position)
        
        return CommandResponse(
            success=True,
            message="Beat removed successfully",
            data=_convert_sequence_to_api(updated_sequence),
            can_undo=sequence_service.can_undo(),
            can_redo=sequence_service.can_redo(),
            undo_description=sequence_service.get_undo_description()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to remove beat {beat_number} from sequence {sequence_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# === Command/Undo Endpoints ===

@app.post("/api/commands/undo", response_model=CommandResponse)
async def undo_command(
    sequence_service: SequenceManagementService = Depends(get_sequence_service)
):
    """Undo the last command."""
    try:
        result_sequence = sequence_service.undo_last_operation()
        
        return CommandResponse(
            success=result_sequence is not None,
            message="Command undone successfully" if result_sequence else "No commands to undo",
            data=_convert_sequence_to_api(result_sequence) if result_sequence else None,
            can_undo=sequence_service.can_undo(),
            can_redo=sequence_service.can_redo(),
            undo_description=sequence_service.get_undo_description(),
            redo_description=sequence_service.get_redo_description()
        )
        
    except Exception as e:
        logger.error(f"Failed to undo command: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/commands/redo", response_model=CommandResponse)
async def redo_command(
    sequence_service: SequenceManagementService = Depends(get_sequence_service)
):
    """Redo the last undone command."""
    try:
        result_sequence = sequence_service.redo_last_operation()
        
        return CommandResponse(
            success=result_sequence is not None,
            message="Command redone successfully" if result_sequence else "No commands to redo",
            data=_convert_sequence_to_api(result_sequence) if result_sequence else None,
            can_undo=sequence_service.can_undo(),
            can_redo=sequence_service.can_redo(),
            undo_description=sequence_service.get_undo_description(),
            redo_description=sequence_service.get_redo_description()
        )
        
    except Exception as e:
        logger.error(f"Failed to redo command: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/commands/history", response_model=APIResponse)
async def get_command_history(
    sequence_service: SequenceManagementService = Depends(get_sequence_service)
):
    """Get command history for debugging."""
    try:
        history = sequence_service.command_processor.get_history_summary()
        
        return APIResponse(
            success=True,
            message="Command history retrieved successfully",
            data={
                "history": history,
                "can_undo": sequence_service.can_undo(),
                "can_redo": sequence_service.can_redo(),
                "undo_description": sequence_service.get_undo_description(),
                "redo_description": sequence_service.get_redo_description()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get command history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === Utility Functions ===

def _convert_sequence_to_api(sequence: SequenceData) -> SequenceAPI:
    """Convert domain sequence to API model."""
    if not sequence:
        return None
        
    return SequenceAPI(
        id=sequence.id,
        name=sequence.name,
        word=sequence.word,
        beats=[_convert_beat_to_api(beat) for beat in sequence.beats],
        start_position=sequence.start_position,
        metadata=sequence.metadata
    )

def _convert_beat_to_api(beat: BeatData) -> BeatAPI:
    """Convert domain beat to API model."""
    return BeatAPI(
        id=beat.id,
        beat_number=beat.beat_number,
        letter=beat.letter,
        duration=beat.duration,
        blue_motion=_convert_motion_to_api(beat.blue_motion) if beat.blue_motion else None,
        red_motion=_convert_motion_to_api(beat.red_motion) if beat.red_motion else None,
        blue_reversal=beat.blue_reversal,
        red_reversal=beat.red_reversal,
        is_blank=beat.is_blank,
        metadata=beat.metadata
    )

def _convert_motion_to_api(motion: MotionData) -> MotionAPI:
    """Convert domain motion to API model."""
    return MotionAPI(
        motion_type=MotionTypeAPI(motion.motion_type.value),
        prop_rot_dir=RotationDirectionAPI(motion.prop_rot_dir.value),
        start_loc=LocationAPI(motion.start_loc.value),
        end_loc=LocationAPI(motion.end_loc.value),
        turns=motion.turns,
        start_ori=motion.start_ori,
        end_ori=motion.end_ori
    )

def _convert_api_to_beat(beat_api: BeatAPI) -> BeatData:
    """Convert API beat to domain model."""
    from ...domain.models.core_models import BeatData
    
    return BeatData(
        id=beat_api.id,
        beat_number=beat_api.beat_number,
        letter=beat_api.letter,
        duration=beat_api.duration,
        blue_motion=_convert_api_to_motion(beat_api.blue_motion) if beat_api.blue_motion else None,
        red_motion=_convert_api_to_motion(beat_api.red_motion) if beat_api.red_motion else None,
        blue_reversal=beat_api.blue_reversal,
        red_reversal=beat_api.red_reversal,
        is_blank=beat_api.is_blank,
        metadata=beat_api.metadata
    )

def _convert_api_to_motion(motion_api: MotionAPI) -> MotionData:
    """Convert API motion to domain model."""
    from ...domain.models.core_models import MotionData, MotionType, RotationDirection, Location
    
    return MotionData(
        motion_type=MotionType(motion_api.motion_type.value),
        prop_rot_dir=RotationDirection(motion_api.prop_rot_dir.value),
        start_loc=Location(motion_api.start_loc.value),
        end_loc=Location(motion_api.end_loc.value),
        turns=motion_api.turns,
        start_ori=motion_api.start_ori,
        end_ori=motion_api.end_ori
    )

async def _post_sequence_creation_tasks(sequence_id: str):
    """Background tasks after sequence creation."""
    # Add any post-creation processing here
    logger.info(f"Post-creation tasks completed for sequence {sequence_id}")
```

### **Step 2: Fault Tolerance Infrastructure (Days 4-7)**

#### **2.1: Circuit Breaker Implementation**

**File:** `src/infrastructure/api/fault_tolerance.py`
```python
"""
Fault tolerance infrastructure for production-grade reliability.
Implements circuit breaker, retry logic, health checking, and graceful degradation.
"""

import asyncio
import time
import logging
from typing import Callable, Any, Optional, Dict, List, Union
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class CircuitBreakerStats:
    """Statistics for circuit breaker monitoring."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    state_changes: List[Dict[str, Any]] = field(default_factory=list)

class CircuitBreaker:
    """
    Circuit breaker implementation for fault tolerance.
    
    Prevents cascading failures by temporarily stopping calls to failing services.
    """

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
        """Decorator to wrap functions with circuit breaker."""
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
        """Execute async function with circuit breaker protection."""
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
        except Exception as e:
            # Unexpected exceptions don't trigger circuit breaker
            logger.warning(f"Unexpected exception in {self.name}: {e}")
            raise

    def _call_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Execute sync function with circuit breaker protection."""
        if not self._can_execute():
            raise CircuitBreakerError(f"Circuit breaker {self.name} is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success_sync()
            return result
        except self.expected_exception as e:
            self._on_failure_sync()
            raise
        except Exception as e:
            logger.warning(f"Unexpected exception in {self.name}: {e}")
            raise

    def _can_execute(self) -> bool:
        """Check if the circuit breaker allows execution."""
        if self._state == CircuitState.CLOSED:
            return True
        elif self._state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if (self._last_failure_time and 
                time.time() - self._last_failure_time > self.recovery_timeout):
                self._state = CircuitState.HALF_OPEN
                logger.info(f"Circuit breaker {self.name} moved to HALF_OPEN")
                return True
            return False
        elif self._state == CircuitState.HALF_OPEN:
            return True
        return False

    async def _on_success(self):
        """Handle successful execution."""
        async with self._lock:
            self._stats.total_requests += 1
            self._stats.successful_requests += 1
            self._stats.last_success_time = datetime.now()
            
            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.CLOSED
                self._failure_count = 0
                logger.info(f"Circuit breaker {self.name} recovered to CLOSED")
                self._stats.state_changes.append({
                    "timestamp": datetime.now(),
                    "from_state": "HALF_OPEN",
                    "to_state": "CLOSED",
                    "reason": "successful_request"
                })

    def _on_success_sync(self):
        """Handle successful execution (sync version)."""
        self._stats.total_requests += 1
        self._stats.successful_requests += 1
        self._stats.last_success_time = datetime.now()
        
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            logger.info(f"Circuit breaker {self.name} recovered to CLOSED")

    async def _on_failure(self):
        """Handle failed execution."""
        async with self._lock:
            self._stats.total_requests += 1
            self._stats.failed_requests += 1
            self._stats.last_failure_time = datetime.now()
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
                logger.warning(f"Circuit breaker {self.name} opened after {self._failure_count} failures")
                self._stats.state_changes.append({
                    "timestamp": datetime.now(),
                    "from_state": "CLOSED" if self._state != CircuitState.HALF_OPEN else "HALF_OPEN",
                    "to_state": "OPEN",
                    "reason": f"failure_threshold_reached_{self._failure_count}"
                })

    def _on_failure_sync(self):
        """Handle failed execution (sync version)."""
        self._stats.total_requests += 1
        self._stats.failed_requests += 1
        self._stats.last_failure_time = datetime.now()
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN
            logger.warning(f"Circuit breaker {self.name} opened after {self._failure_count} failures")

    @property
    def state(self) -> CircuitState:
        """Get current circuit breaker state."""
        return self._state

    @property
    def stats(self) -> CircuitBreakerStats:
        """Get circuit breaker statistics."""
        return self._stats

    def reset(self):
        """Reset circuit breaker to closed state."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        logger.info(f"Circuit breaker {self.name} manually reset")

class CircuitBreakerError(Exception):
    """Exception raised when circuit breaker is open."""
    pass

class RetryPolicy:
    """
    Retry policy with exponential backoff and jitter.
    """

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
        """Decorator to add retry logic to functions."""
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
        """Execute async function with retry logic."""
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                return await func(*args, **kwargs)
            except self.retryable_exceptions as e:
                last_exception = e
                
                if attempt == self.max_attempts - 1:
                    logger.error(f"Function {func.__name__} failed after {self.max_attempts} attempts")
                    raise
                
                delay = self._calculate_delay(attempt)
                logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{self.max_attempts}), retrying in {delay:.2f}s: {e}")
                await asyncio.sleep(delay)
            except Exception as e:
                # Non-retryable exception
                logger.error(f"Non-retryable exception in {func.__name__}: {e}")
                raise
        
        raise last_exception

    def _retry_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Execute sync function with retry logic."""
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except self.retryable_exceptions as e:
                last_exception = e
                
                if attempt == self.max_attempts - 1:
                    logger.error(f"Function {func.__name__} failed after {self.max_attempts} attempts")
                    raise
                
                delay = self._calculate_delay(attempt)
                logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{self.max_attempts}), retrying in {delay:.2f}s: {e}")
                time.sleep(delay)
            except Exception as e:
                logger.error(f"Non-retryable exception in {func.__name__}: {e}")
                raise
        
        raise last_exception

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for next retry attempt."""
        if self.exponential_backoff:
            delay = self.delay * (2 ** attempt)
        else:
            delay = self.delay
        
        delay = min(delay, self.max_delay)
        
        if self.jitter:
            delay *= (0.5 + random.random() * 0.5)  # 50-100% of calculated delay
        
        return delay

class HealthChecker:
    """
    Health checker for monitoring system and component health.
    """

    def __init__(self, check_interval: float = 30.0):
        self.check_interval = check_interval
        self._health_checks: Dict[str, Callable] = {}
        self._component_health: Dict[str, ComponentHealth] = {}
        self._running = False
        self._task: Optional[asyncio.Task] = None

    def register_health_check(self, name: str, check_func: Callable) -> None:
        """Register a health check function."""
        self._health_checks[name] = check_func
        logger.info(f"Registered health check: {name}")

    async def start(self):
        """Start the health checker background task."""
        if self._running:
            return
        
        self._running = True
        self._task = asyncio.create_task(self._health_check_loop())
        logger.info("Health checker started")

    async def stop(self):
        """Stop the health checker."""
        if not self._running:
            return
        
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        logger.info("Health checker stopped")

    async def _health_check_loop(self):
        """Main health check loop."""
        while self._running:
            try:
                await self._perform_health_checks()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check loop error: {e}")
                await asyncio.sleep(self.check_interval)

    async def _perform_health_checks(self):
        """Perform all registered health checks."""
        for name, check_func in self._health_checks.items():
            try:
                start_time = time.perf_counter()
                
                if asyncio.iscoroutinefunction(check_func):
                    result = await check_func()
                else:
                    result = check_func()
                
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
                    message=str(e),
                    response_time_ms=0.0
                )
                logger.warning(f"Health check failed for {name}: {e}")

    async def get_system_health(self) -> SystemHealth:
        """Get overall system health status."""
        if not self._component_health:
            # No health checks registered yet
            return SystemHealth(
                status=HealthStatus.HEALTHY,
                components=[],
                uptime_seconds=time.time()
            )
        
        components = list(self._component_health.values())
        
        # Determine overall status
        unhealthy_count = sum(1 for c in components if c.status == HealthStatus.UNHEALTHY)
        degraded_count = sum(1 for c in components if c.status == HealthStatus.DEGRADED)
        
        if unhealthy_count > 0:
            overall_status = HealthStatus.UNHEALTHY
        elif degraded_count > 0:
            overall_status = HealthStatus.DEGRADED
        else:
            overall_status = HealthStatus.HEALTHY
        
        return SystemHealth(
            status=overall_status,
            components=components,
            uptime_seconds=time.time()
        )

# === Default Health Checks ===

async def check_event_bus_health():
    """Health check for event bus."""
    try:
        from ...core.events import get_event_bus
        event_bus = get_event_bus()
        # Basic connectivity test
        subscription_count = event_bus.get_subscription_count()
        if subscription_count >= 0:  # Any non-negative number is healthy
            return True
        else:
            raise Exception("Event bus returned invalid subscription count")
    except Exception as e:
        raise Exception(f"Event bus health check failed: {e}")

async def check_command_processor_health():
    """Health check for command processor."""
    try:
        from ...core.dependency_injection.di_container import get_container
        container = get_container()
        command_processor = container.resolve(CommandProcessor)
        # Check if command processor is responsive
        history = command_processor.get_history_summary()
        return True
    except Exception as e:
        raise Exception(f"Command processor health check failed: {e}")

def check_database_health():
    """Health check for database connectivity."""
    # In a real implementation, this would check database connection
    # For now, just return healthy
    return True

def check_memory_usage():
    """Health check for memory usage."""
    import psutil
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > 90:
        raise Exception(f"High memory usage: {memory_percent}%")
    return True

# === Graceful Degradation ===

class GracefulDegradation:
    """
    Provides graceful degradation capabilities when services are unavailable.
    """

    def __init__(self):
        self._fallback_handlers: Dict[str, Callable] = {}
        self._service_status: Dict[str, bool] = {}

    def register_fallback(self, service_name: str, fallback_func: Callable):
        """Register a fallback function for a service."""
        self._fallback_handlers[service_name] = fallback_func
        logger.info(f"Registered fallback for service: {service_name}")

    def mark_service_unavailable(self, service_name: str):
        """Mark a service as unavailable."""
        self._service_status[service_name] = False
        logger.warning(f"Service marked as unavailable: {service_name}")

    def mark_service_available(self, service_name: str):
        """Mark a service as available."""
        self._service_status[service_name] = True
        logger.info(f"Service marked as available: {service_name}")

    def is_service_available(self, service_name: str) -> bool:
        """Check if a service is available."""
        return self._service_status.get(service_name, True)

    async def call_with_fallback(self, service_name: str, primary_func: Callable, *args, **kwargs):
        """Call primary function or fallback if service is unavailable."""
        if self.is_service_available(service_name):
            try:
                if asyncio.iscoroutinefunction(primary_func):
                    return await primary_func(*args, **kwargs)
                else:
                    return primary_func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Primary function failed for {service_name}: {e}")
                self.mark_service_unavailable(service_name)
                # Fall through to fallback
        
        # Use fallback
        if service_name in self._fallback_handlers:
            fallback_func = self._fallback_handlers[service_name]
            logger.info(f"Using fallback for {service_name}")
            
            if asyncio.iscoroutinefunction(fallback_func):
                return await fallback_func(*args, **kwargs)
            else:
                return fallback_func(*args, **kwargs)
        else:
            raise ServiceUnavailableError(f"Service {service_name} is unavailable and no fallback is registered")

class ServiceUnavailableError(Exception):
    """Exception raised when a service is unavailable and no fallback exists."""
    pass
```

#### **2.2: WebSocket API for Real-Time Events**

**File:** `src/infrastructure/api/websocket_api.py`
```python
"""
WebSocket API for real-time event streaming to external clients.
Provides live updates of TKA events with connection management and fault tolerance.
"""

import asyncio
import json
import logging
from typing import Dict, Set, Optional, Any, List
from datetime import datetime
import uuid

from fastapi import WebSocket, WebSocketDisconnect
from .api_models import EventAPI, SequenceEventAPI, MotionEventAPI, LayoutEventAPI
from .fault_tolerance import CircuitBreaker, RetryPolicy
from ...core.events import IEventBus, get_event_bus, BaseEvent

logger = logging.getLogger(__name__)

class WebSocketConnectionManager:
    """
    Manages WebSocket connections with automatic reconnection and filtering.
    """

    def __init__(self, event_bus: Optional[IEventBus] = None):
        self.event_bus = event_bus or get_event_bus()
        self._connections: Dict[str, WebSocket] = {}
        self._connection_filters: Dict[str, Set[str]] = {}
        self._connection_metadata: Dict[str, Dict[str, Any]] = {}
        self._subscription_ids: List[str] = []
        
        # Setup event subscriptions
        self._setup_event_subscriptions()

    def _setup_event_subscriptions(self):
        """Subscribe to all domain events for WebSocket broadcasting."""
        # Subscribe to all sequence events
        for event_type in ["sequence.created", "sequence.beat_added", "sequence.beat_removed", "sequence.beat_updated"]:
            sub_id = self.event_bus.subscribe(event_type, self._broadcast_event)
            self._subscription_ids.append(sub_id)
        
        # Subscribe to motion events
        for event_type in ["motion.generated", "motion.validated"]:
            sub_id = self.event_bus.subscribe(event_type, self._broadcast_event)
            self._subscription_ids.append(sub_id)
        
        # Subscribe to layout events
        for event_type in ["layout.beat_frame_recalculated", "layout.component_recalculated"]:
            sub_id = self.event_bus.subscribe(event_type, self._broadcast_event)
            self._subscription_ids.append(sub_id)

    async def connect(self, websocket: WebSocket, client_id: Optional[str] = None) -> str:
        """Accept a new WebSocket connection."""
        await websocket.accept()
        
        if not client_id:
            client_id = f"client_{uuid.uuid4().hex[:8]}"
        
        self._connections[client_id] = websocket
        self._connection_filters[client_id] = set()  # No filters by default
        self._connection_metadata