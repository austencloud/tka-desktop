# Schema-First Development

## Task 3.2: Schema-First API Development

**Generate Type-Safe Bindings:**

```python
# FILE: src/infrastructure/codegen/schema_generator.py

"""
Schema-first development tooling for TKA modern.
Generates type-safe bindings for TypeScript, Python, and other languages.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import ast

class LanguageTarget(Enum):
    """Supported code generation targets."""
    TYPESCRIPT = "typescript"
    PYTHON = "python"
    CSHARP = "csharp"
    JAVA = "java"

@dataclass
class SchemaField:
    """Represents a field in a schema."""
    name: str
    type: str
    optional: bool = False
    description: Optional[str] = None

@dataclass
class SchemaModel:
    """Represents a data model."""
    name: str
    fields: List[SchemaField]
    description: Optional[str] = None

@dataclass
class APIEndpoint:
    """Represents an API endpoint."""
    method: str
    path: str
    request_model: Optional[str] = None
    response_model: Optional[str] = None
    description: Optional[str] = None

class SchemaGenerator:
    """Generates schema and type bindings from Python models."""

    def __init__(self, src_dir: Path):
        self.src_dir = src_dir
        self.models: List[SchemaModel] = []
        self.endpoints: List[APIEndpoint] = []

    def analyze_models(self) -> None:
        """Analyze Python models and extract schema information."""
        domain_dir = self.src_dir / "domain" / "models"

        for py_file in domain_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue

            self._analyze_file(py_file)

    def _analyze_file(self, file_path: Path) -> None:
        """Analyze a single Python file for models."""
        with open(file_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it's a dataclass
                for decorator in node.decorator_list:
                    if (isinstance(decorator, ast.Name) and decorator.id == "dataclass") or \
                       (isinstance(decorator, ast.Attribute) and decorator.attr == "dataclass"):
                        model = self._extract_dataclass_schema(node)
                        if model:
                            self.models.append(model)
                        break

    def _extract_dataclass_schema(self, class_node: ast.ClassDef) -> Optional[SchemaModel]:
        """Extract schema from a dataclass."""
        fields = []
        description = ast.get_docstring(class_node)

        for node in class_node.body:
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                field_name = node.target.id
                field_type = self._get_type_annotation(node.annotation)
                optional = self._is_optional_type(node.annotation)

                # Look for field description in comments
                field_desc = None
                # This is simplified - would need more sophisticated comment parsing

                fields.append(SchemaField(
                    name=field_name,
                    type=field_type,
                    optional=optional,
                    description=field_desc
                ))

        if fields:
            return SchemaModel(
                name=class_node.name,
                fields=fields,
                description=description
            )
        return None

    def _get_type_annotation(self, annotation: ast.AST) -> str:
        """Extract type annotation as string."""
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Attribute):
            return f"{self._get_type_annotation(annotation.value)}.{annotation.attr}"
        elif isinstance(annotation, ast.Subscript):
            value = self._get_type_annotation(annotation.value)
            slice_val = annotation.slice
            if isinstance(slice_val, ast.Name):
                return f"{value}[{slice_val.id}]"
            elif isinstance(slice_val, ast.Tuple):
                elts = [self._get_type_annotation(elt) for elt in slice_val.elts]
                return f"{value}[{', '.join(elts)}]"
        return "Any"

    def _is_optional_type(self, annotation: ast.AST) -> bool:
        """Check if type annotation represents an optional type."""
        if isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name):
                if annotation.value.id in ["Optional", "Union"]:
                    return True
        return False

    def generate_typescript(self, output_dir: Path) -> None:
        """Generate TypeScript type definitions."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate models
        models_content = [
            "// Generated TypeScript types for TKA Desktop modern",
            "// DO NOT EDIT - Generated automatically",
            "",
        ]

        for model in self.models:
            if model.description:
                models_content.append(f"/**")
                models_content.append(f" * {model.description}")
                models_content.append(f" */")

            models_content.append(f"export interface {model.name} {{")

            for field in model.fields:
                optional_marker = "?" if field.optional else ""
                ts_type = self._python_type_to_typescript(field.type)

                if field.description:
                    models_content.append(f"  /** {field.description} */")
                models_content.append(f"  {field.name}{optional_marker}: {ts_type};")

            models_content.extend(["}", ""])

        with open(output_dir / "models.ts", 'w') as f:
            f.write('\n'.join(models_content))

        # Generate API client
        self._generate_typescript_api_client(output_dir)

    def _generate_typescript_api_client(self, output_dir: Path) -> None:
        """Generate TypeScript API client."""
        client_content = [
            "// Generated TypeScript API client for TKA Desktop modern",
            "// DO NOT EDIT - Generated automatically",
            "",
            "import { " + ", ".join([model.name for model in self.models]) + " } from './models';",
            "",
            "export class TKAApiClient {",
            "  private baseUrl: string;",
            "",
            "  constructor(baseUrl: string = 'http://localhost:8000/api') {",
            "    this.baseUrl = baseUrl;",
            "  }",
            "",
            "  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {",
            "    const response = await fetch(`${this.baseUrl}${path}`, {",
            "      headers: {",
            "        'Content-Type': 'application/json',",
            "        ...options.headers,",
            "      },",
            "      ...options,",
            "    });",
            "",
            "    if (!response.ok) {",
            "      throw new Error(`API request failed: ${response.statusText}`);",
            "    }",
            "",
            "    return response.json();",
            "  }",
            "",
        ]

        # Add API methods based on endpoints
        for endpoint in self.endpoints:
            method_name = self._generate_method_name(endpoint)
            client_content.extend(self._generate_typescript_method(endpoint, method_name))

        client_content.append("}")

        with open(output_dir / "api-client.ts", 'w') as f:
            f.write('\n'.join(client_content))

    def generate_python_client(self, output_dir: Path) -> None:
        """Generate Python API client."""
        output_dir.mkdir(parents=True, exist_ok=True)

        client_content = [
            '"""',
            'Generated Python API client for TKA Desktop modern.',
            'DO NOT EDIT - Generated automatically.',
            '"""',
            "",
            "import requests",
            "from typing import Dict, List, Any, Optional",
            "from dataclasses import dataclass",
            "",
            "# Re-export models",
        ]

        # Import models
        for model in self.models:
            client_content.append(f"from src.domain.models.{model.name.lower()} import {model.name}")

        client_content.extend([
            "",
            "class TKAApiClient:",
            '    """Type-safe Python client for TKA Desktop API."""',
            "",
            '    def __init__(self, base_url: str = "http://localhost:8000/api"):',
            "        self.base_url = base_url",
            "        self.session = requests.Session()",
            "",
            "    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:",
            '        """Make a request to the API."""',
            "        url = f'{self.base_url}{path}'",
            "        response = self.session.request(method, url, **kwargs)",
            "        response.raise_for_status()",
            "        return response.json()",
            "",
        ])

        # Add API methods
        for endpoint in self.endpoints:
            method_name = self._generate_method_name(endpoint)
            client_content.extend(self._generate_python_method(endpoint, method_name))

        with open(output_dir / "api_client.py", 'w') as f:
            f.write('\n'.join(client_content))

    def generate_openapi_spec(self, output_path: Path) -> None:
        """Generate OpenAPI 3.0 specification."""
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "TKA Desktop API",
                "version": "2.0.0",
                "description": "REST API for TKA Desktop application"
            },
            "servers": [
                {
                    "url": "http://localhost:8000/api",
                    "description": "Development server"
                }
            ],
            "paths": {},
            "components": {
                "schemas": {}
            }
        }

        # Add model schemas
        for model in self.models:
            spec["components"]["schemas"][model.name] = self._model_to_openapi_schema(model)

        # Add endpoints
        for endpoint in self.endpoints:
            path = endpoint.path
            if path not in spec["paths"]:
                spec["paths"][path] = {}

            spec["paths"][path][endpoint.method.lower()] = self._endpoint_to_openapi(endpoint)

        with open(output_path, 'w') as f:
            json.dump(spec, f, indent=2)

    def _python_type_to_typescript(self, python_type: str) -> str:
        """Convert Python type to TypeScript type."""
        type_mapping = {
            "str": "string",
            "int": "number",
            "float": "number",
            "bool": "boolean",
            "dict": "object",
            "Dict": "object",
            "list": "any[]",
            "List": "any[]",
            "Any": "any",
        }

        # Handle generic types
        if "[" in python_type:
            base_type = python_type.split("[")[0]
            inner_types = python_type.split("[")[1].rstrip("]")

            if base_type in ["List", "list"]:
                inner_ts = self._python_type_to_typescript(inner_types)
                return f"{inner_ts}[]"
            elif base_type in ["Dict", "dict"]:
                # Simplified - assume string keys
                value_type = inner_types.split(",")[-1].strip()
                value_ts = self._python_type_to_typescript(value_type)
                return f"Record<string, {value_ts}>"

        return type_mapping.get(python_type, python_type)

    def _generate_method_name(self, endpoint: APIEndpoint) -> str:
        """Generate method name from endpoint."""
        path_parts = [part for part in endpoint.path.split("/") if part and not part.startswith("{")]
        method_base = "_".join(path_parts).replace("-", "_")
        return f"{endpoint.method.lower()}_{method_base}"

    def _generate_typescript_method(self, endpoint: APIEndpoint, method_name: str) -> List[str]:
        """Generate TypeScript method for endpoint."""
        method_lines = []

        if endpoint.description:
            method_lines.extend([
                f"  /**",
                f"   * {endpoint.description}",
                f"   */"
            ])

        # Determine parameters and return type
        params = []
        if endpoint.request_model:
            params.append(f"data: {endpoint.request_model}")

        return_type = endpoint.response_model or "any"

        method_lines.append(f"  async {method_name}({', '.join(params)}): Promise<{return_type}> {{")

        # Generate method body
        if endpoint.method.upper() == "GET":
            method_lines.append(f"    return this.request<{return_type}>('{endpoint.path}');")
        else:
            method_lines.append(f"    return this.request<{return_type}>('{endpoint.path}', {{")
            method_lines.append(f"      method: '{endpoint.method.upper()}',")
            if endpoint.request_model:
                method_lines.append(f"      body: JSON.stringify(data),")
            method_lines.append(f"    }});")

        method_lines.extend(["  }", ""])

        return method_lines

    def _generate_python_method(self, endpoint: APIEndpoint, method_name: str) -> List[str]:
        """Generate Python method for endpoint."""
        method_lines = []

        if endpoint.description:
            method_lines.extend([
                f'    """{endpoint.description}"""'
            ])

        # Determine parameters and return type
        params = ["self"]
        if endpoint.request_model:
            params.append(f"data: {endpoint.request_model}")

        return_type = endpoint.response_model or "Dict[str, Any]"

        method_lines.append(f"    def {method_name}({', '.join(params)}) -> {return_type}:")

        # Generate method body
        if endpoint.method.upper() == "GET":
            method_lines.append(f"        return self._request('GET', '{endpoint.path}')")
        else:
            method_lines.append(f"        return self._request('{endpoint.method.upper()}', '{endpoint.path}',")
            if endpoint.request_model:
                method_lines.append(f"                             json=data.__dict__ if hasattr(data, '__dict__') else data)")
            else:
                method_lines.append(f"                             )")

        method_lines.append("")

        return method_lines

    def _model_to_openapi_schema(self, model: SchemaModel) -> Dict[str, Any]:
        """Convert model to OpenAPI schema."""
        properties = {}
        required = []

        for field in model.fields:
            properties[field.name] = {
                "type": self._python_type_to_openapi_type(field.type)
            }

            if field.description:
                properties[field.name]["description"] = field.description

            if not field.optional:
                required.append(field.name)

        schema = {
            "type": "object",
            "properties": properties
        }

        if required:
            schema["required"] = required

        if model.description:
            schema["description"] = model.description

        return schema

    def _endpoint_to_openapi(self, endpoint: APIEndpoint) -> Dict[str, Any]:
        """Convert endpoint to OpenAPI specification."""
        spec = {}

        if endpoint.description:
            spec["summary"] = endpoint.description

        if endpoint.request_model:
            spec["requestBody"] = {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": f"#/components/schemas/{endpoint.request_model}"}
                    }
                }
            }

        spec["responses"] = {
            "200": {
                "description": "Successful response"
            }
        }

        if endpoint.response_model:
            spec["responses"]["200"]["content"] = {
                "application/json": {
                    "schema": {"$ref": f"#/components/schemas/{endpoint.response_model}"}
                }
            }

        return spec

    def _python_type_to_openapi_type(self, python_type: str) -> str:
        """Convert Python type to OpenAPI type."""
        type_mapping = {
            "str": "string",
            "int": "integer",
            "float": "number",
            "bool": "boolean",
        }

        return type_mapping.get(python_type, "string")

def main():
    """CLI entry point for schema generation."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate API schemas and clients")
    parser.add_argument("--src-dir", default="src", help="Source directory")
    parser.add_argument("--output-dir", default="generated", help="Output directory")
    parser.add_argument("--language",
                       choices=[lang.value for lang in LanguageTarget],
                       help="Target language")
    parser.add_argument("--openapi", action="store_true", help="Generate OpenAPI spec")

    args = parser.parse_args()

    src_dir = Path(args.src_dir)
    output_dir = Path(args.output_dir)

    generator = SchemaGenerator(src_dir)
    generator.analyze_models()

    if args.language == LanguageTarget.TYPESCRIPT.value:
        generator.generate_typescript(output_dir / "typescript")
        print(f"✅ TypeScript bindings generated in {output_dir}/typescript")
    elif args.language == LanguageTarget.PYTHON.value:
        generator.generate_python_client(output_dir / "python")
        print(f"✅ Python client generated in {output_dir}/python")

    if args.openapi:
        generator.generate_openapi_spec(output_dir / "openapi.json")
        print(f"✅ OpenAPI spec generated in {output_dir}/openapi.json")

if __name__ == "__main__":
    main()
```

**Usage Example:**

```bash
# Generate TypeScript bindings
python src/infrastructure/codegen/schema_generator.py --language typescript --output-dir clients/

# Generate OpenAPI specification
python src/infrastructure/codegen/schema_generator.py --openapi --output-dir api-docs/

# Use in TypeScript project
npm install
# Import generated types
import { BeatData, SequenceData } from './clients/typescript/models';
import { TKAApiClient } from './clients/typescript/api-client';

const client = new TKAApiClient();
const sequences = await client.get_sequences();
```

This generates **type-safe API clients** in multiple languages, ensuring consistency across all integrations.
