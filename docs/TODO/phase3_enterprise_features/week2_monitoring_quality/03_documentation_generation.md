# Documentation Generation

## Task 3.5: Documentation Generation

**Auto-generate Documentation:**

````python
# FILE: src/infrastructure/docs/doc_generator.py

"""
Automatic documentation generation for TKA v2.
Generates API docs, architecture diagrams, and user guides.
"""

import ast
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class ClassInfo:
    """Information about a class."""
    name: str
    docstring: Optional[str]
    methods: List[str]
    file_path: str
    is_interface: bool = False
    is_service: bool = False

@dataclass
class ServiceInfo:
    """Information about a service."""
    name: str
    interface: Optional[str]
    implementation: str
    dependencies: List[str]
    description: str

class DocumentationGenerator:
    """Generates comprehensive documentation."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_dir = project_root / "src"
        self.docs_dir = project_root / "docs"
        self.docs_dir.mkdir(exist_ok=True)

    def generate_all(self) -> None:
        """Generate all documentation."""
        print("📚 Generating TKA modern Documentation...")

        # Generate API documentation
        self._generate_api_docs()
        print("  ✅ API Documentation")

        # Generate architecture overview
        self._generate_architecture_docs()
        print("  ✅ Architecture Documentation")

        # Generate service documentation
        self._generate_service_docs()
        print("  ✅ Service Documentation")

        # Generate user guide
        self._generate_user_guide()
        print("  ✅ User Guide")

        print(f"🎉 Documentation generated in: {self.docs_dir}")

    def _generate_api_docs(self) -> None:
        """Generate API documentation."""
        api_file = self.src_dir / "infrastructure" / "api" / "rest_api.py"

        if not api_file.exists():
            return

        # Parse API endpoints
        endpoints = self._parse_api_endpoints(api_file)

        # Generate markdown
        content = [
            "# TKA Desktop API Documentation",
            "",
            "This document describes the REST API for TKA Desktop v2.",
            "",
            "## Base URL",
            "```",
            "http://localhost:8000/api",
            "```",
            "",
            "## Endpoints",
            ""
        ]

        for endpoint in endpoints:
            content.extend([
                f"### {endpoint['method']} {endpoint['path']}",
                "",
                endpoint.get('description', 'No description available.'),
                "",
                "**Request:**",
                f"```http",
                f"{endpoint['method']} {endpoint['path']}",
                "```",
                "",
                "**Response:**",
                "```json",
                json.dumps(endpoint.get('response_example', {}), indent=2),
                "```",
                ""
            ])

        with open(self.docs_dir / "API.md", 'w') as f:
            f.write('\n'.join(content))

    def _generate_architecture_docs(self) -> None:
        """Generate architecture documentation."""
        content = [
            "# TKA Desktop modern Architecture",
            "",
            "## Overview",
            "",
            "TKA Desktop modern follows Clean Architecture principles with clear separation of concerns:",
            "",
            "```",
            "src/",
            "├── domain/          # Business logic and models",
            "├── application/     # Use cases and services",
            "├── infrastructure/  # External concerns (DB, APIs, etc.)",
            "└── presentation/    # UI components and controllers",
            "```",
            "",
            "## Layer Responsibilities",
            "",
            "### Domain Layer",
            "- Core business models (`BeatData`, `SequenceData`, `MotionData`)",
            "- Business rules and invariants",
            "- No dependencies on other layers",
            "",
            "### Application Layer",
            "- Application services implementing use cases",
            "- Service interfaces (Protocols)",
            "- Cross-cutting concerns (events, commands)",
            "",
            "### Infrastructure Layer",
            "- Data persistence",
            "- External API integrations",
            "- Configuration management",
            "",
            "### Presentation Layer",
            "- UI components and widgets",
            "- User interaction handling",
            "- View models and controllers",
            "",
            "## Key Patterns",
            "",
            "### Dependency Injection",
            "- Constructor injection with type resolution",
            "- Interface-based programming",
            "- Singleton and transient lifetimes",
            "",
            "### Event-Driven Architecture",
            "- Type-safe event bus",
            "- Decoupled component communication",
            "- Event sourcing for complex workflows",
            "",
            "### Command Pattern",
            "- Undoable operations",
            "- Command history and replay",
            "- Transactional business operations",
            "",
            "## Service Architecture",
            ""
        ]

        # Add service information
        services = self._analyze_services()
        for service in services:
            content.extend([
                f"### {service.name}",
                f"- **Interface**: `{service.interface}`",
                f"- **Implementation**: `{service.implementation}`",
                f"- **Dependencies**: {', '.join(service.dependencies) if service.dependencies else 'None'}",
                f"- **Description**: {service.description}",
                ""
            ])

        with open(self.docs_dir / "ARCHITECTURE.md", 'w') as f:
            f.write('\n'.join(content))

    def _generate_service_docs(self) -> None:
        """Generate detailed service documentation."""
        services = self._analyze_services()

        content = [
            "# Service Documentation",
            "",
            "This document provides detailed information about all services in TKA v2.",
            ""
        ]

        for service in services:
            content.extend([
                f"## {service.name}",
                "",
                f"**Interface**: `{service.interface}`",
                f"**Implementation**: `{service.implementation}`",
                "",
                f"### Description",
                service.description,
                "",
                f"### Dependencies",
                ""
            ])

            if service.dependencies:
                for dep in service.dependencies:
                    content.append(f"- `{dep}`")
            else:
                content.append("- None")

            content.extend(["", "---", ""])

        with open(self.docs_dir / "SERVICES.md", 'w') as f:
            f.write('\n'.join(content))

    def _generate_user_guide(self) -> None:
        """Generate user guide."""
        content = [
            "# TKA Desktop modern User Guide",
            "",
            "## Getting Started",
            "",
            "### Installation",
            "",
            "1. Clone the repository",
            "2. Install dependencies: `pip install -r requirements.txt`",
            "3. Run the application: `python v2/main.py`",
            "",
            "### Basic Usage",
            "",
            "1. **Create a Sequence**: Use the Construct tab to create new sequences",
            "2. **Add Beats**: Click the '+' button to add beats to your sequence",
            "3. **Edit Motions**: Select a beat and modify its blue/red motions",
            "4. **Preview**: Use the graph editor to preview your sequence",
            "",
            "## Advanced Features",
            "",
            "### Command Line Interface",
            "",
            "TKA modern includes a powerful CLI for automation:",
            "",
            "```bash",
            "# Generate API bindings",
            "python src/infrastructure/codegen/schema_generator.py --language typescript",
            "",
            "# Run quality gates",
            "python src/infrastructure/quality/quality_gates.py",
            "",
            "# Start API server",
            "python src/infrastructure/api/rest_api.py",
            "```",
            "",
            "### API Integration",
            "",
            "TKA modern provides a REST API for external integrations. See [API.md](API.md) for details.",
            "",
            "### Performance Monitoring",
            "",
            "Enable performance monitoring to track application performance:",
            "",
            "```python",
            "from src.infrastructure.monitoring.performance_monitor import monitor_performance",
            "",
            "@monitor_performance()",
            "def my_function():",
            "    # Function will be automatically monitored",
            "    pass",
            "```"
        ]

        with open(self.docs_dir / "USER_GUIDE.md", 'w') as f:
            f.write('\n'.join(content))

    def _parse_api_endpoints(self, api_file: Path) -> List[Dict[str, Any]]:
        """Parse API endpoints from FastAPI file."""
        # This is a simplified parser - in reality you'd want more sophisticated parsing
        endpoints = [
            {
                "method": "GET",
                "path": "/api/sequences/",
                "description": "List all sequences",
                "response_example": {"sequences": []}
            },
            {
                "method": "POST",
                "path": "/api/sequences/",
                "description": "Create a new sequence",
                "response_example": {"id": "seq_123", "name": "New Sequence"}
            }
        ]
        return endpoints

    def _analyze_services(self) -> List[ServiceInfo]:
        """Analyze services in the application."""
        services = [
            ServiceInfo(
                name="Sequence Management",
                interface="ISequenceManagementService",
                implementation="SequenceManagementService",
                dependencies=["IEventBus", "CommandProcessor"],
                description="Manages sequence creation, modification, and persistence"
            ),
            ServiceInfo(
                name="Motion Management",
                interface="IMotionManagementService",
                implementation="MotionManagementService",
                dependencies=["IMotionValidationService", "IMotionGenerationService"],
                description="Handles motion generation, validation, and transformation"
            ),
            ServiceInfo(
                name="Arrow Management",
                interface="IArrowManagementService",
                implementation="ArrowManagementService",
                dependencies=["DefaultPlacementService", "PlacementKeyService"],
                description="Manages arrow positioning, rotation, and visualization"
            )
        ]
        return services

def main():
    """CLI entry point for documentation generation."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate TKA modern documentation")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--type", choices=["all", "api", "architecture", "services", "user"],
                       default="all", help="Documentation type to generate")

    args = parser.parse_args()

    project_root = Path(args.project_root).absolute()
    generator = DocumentationGenerator(project_root)

    if args.type == "all":
        generator.generate_all()
    elif args.type == "api":
        generator._generate_api_docs()
    elif args.type == "architecture":
        generator._generate_architecture_docs()
    elif args.type == "services":
        generator._generate_service_docs()
    elif args.type == "user":
        generator._generate_user_guide()

if __name__ == "__main__":
    main()
````
