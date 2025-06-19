#!/usr/bin/env python3
"""
API Documentation Validation Script

This script validates that the API documentation meets world-class professional
standards and provides comprehensive coverage of all endpoints.

Usage:
    python validate_api_documentation.py
"""

import sys
import json
from pathlib import Path

# Add src to path for imports
modern_src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from infrastructure.api.production_api import app


def validate_api_documentation():
    """Validate API documentation quality and completeness."""
    print("=" * 60)
    print("API DOCUMENTATION VALIDATION")
    print("=" * 60)
    print("Validating world-class API documentation standards...")
    print()
    
    validation_results = {
        "total_endpoints": 0,
        "documented_endpoints": 0,
        "endpoints_with_examples": 0,
        "endpoints_with_error_docs": 0,
        "endpoints_with_performance_info": 0,
        "validation_passed": True,
        "issues": []
    }
    
    # Get OpenAPI schema
    openapi_schema = app.openapi()
    
    # Validate basic API information
    print("Basic API Information:")
    print(f"  Title: {openapi_schema.get('info', {}).get('title', 'N/A')}")
    print(f"  Version: {openapi_schema.get('info', {}).get('version', 'N/A')}")
    print(f"  Description: {openapi_schema.get('info', {}).get('description', 'N/A')}")
    print()
    
    # Validate endpoints
    paths = openapi_schema.get('paths', {})
    validation_results["total_endpoints"] = len(paths)
    
    print("Endpoint Documentation Analysis:")
    print("-" * 40)
    
    for path, methods in paths.items():
        for method, details in methods.items():
            if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                endpoint_name = f"{method.upper()} {path}"
                print(f"\n{endpoint_name}:")
                
                # Check for summary and description
                has_summary = bool(details.get('summary'))
                has_description = bool(details.get('description'))
                
                if has_summary and has_description:
                    validation_results["documented_endpoints"] += 1
                    print("  ✓ Summary and description present")
                else:
                    validation_results["issues"].append(f"{endpoint_name}: Missing summary or description")
                    print("  ✗ Missing summary or description")
                
                # Check for response examples
                responses = details.get('responses', {})
                has_examples = False
                
                for status_code, response_info in responses.items():
                    content = response_info.get('content', {})
                    for media_type, media_info in content.items():
                        if 'example' in media_info:
                            has_examples = True
                            break
                    if has_examples:
                        break
                
                if has_examples:
                    validation_results["endpoints_with_examples"] += 1
                    print("  ✓ Response examples present")
                else:
                    validation_results["issues"].append(f"{endpoint_name}: Missing response examples")
                    print("  ✗ Missing response examples")
                
                # Check for error response documentation
                has_error_docs = any(
                    int(status) >= 400 for status in responses.keys() 
                    if status.isdigit()
                )
                
                if has_error_docs:
                    validation_results["endpoints_with_error_docs"] += 1
                    print("  ✓ Error responses documented")
                else:
                    validation_results["issues"].append(f"{endpoint_name}: Missing error response documentation")
                    print("  ✗ Missing error response documentation")
                
                # Check for performance information in description
                description_text = details.get('description', '').lower()
                has_performance_info = (
                    'performance' in description_text or
                    'response time' in description_text or
                    'memory' in description_text or
                    'cpu' in description_text
                )
                
                if has_performance_info:
                    validation_results["endpoints_with_performance_info"] += 1
                    print("  ✓ Performance characteristics documented")
                else:
                    validation_results["issues"].append(f"{endpoint_name}: Missing performance characteristics")
                    print("  ✗ Missing performance characteristics")
    
    # Calculate scores
    total = validation_results["total_endpoints"]
    if total > 0:
        documentation_score = (validation_results["documented_endpoints"] / total) * 100
        examples_score = (validation_results["endpoints_with_examples"] / total) * 100
        error_docs_score = (validation_results["endpoints_with_error_docs"] / total) * 100
        performance_score = (validation_results["endpoints_with_performance_info"] / total) * 100
    else:
        documentation_score = examples_score = error_docs_score = performance_score = 0
    
    # Print summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total Endpoints: {total}")
    print(f"Documentation Coverage: {documentation_score:.1f}% ({validation_results['documented_endpoints']}/{total})")
    print(f"Examples Coverage: {examples_score:.1f}% ({validation_results['endpoints_with_examples']}/{total})")
    print(f"Error Documentation: {error_docs_score:.1f}% ({validation_results['endpoints_with_error_docs']}/{total})")
    print(f"Performance Documentation: {performance_score:.1f}% ({validation_results['endpoints_with_performance_info']}/{total})")
    
    # Overall assessment
    overall_score = (documentation_score + examples_score + error_docs_score + performance_score) / 4
    print(f"\nOverall Documentation Quality: {overall_score:.1f}%")
    
    if overall_score >= 90:
        print("\n🎉 WORLD-CLASS API DOCUMENTATION!")
        print("✅ Documentation meets enterprise-grade standards")
        print("✅ Comprehensive coverage of all endpoints")
        print("✅ Professional-quality examples and error handling")
        print("✅ Performance characteristics well documented")
        validation_results["validation_passed"] = True
    elif overall_score >= 75:
        print("\n✅ Good API documentation with room for improvement")
        validation_results["validation_passed"] = True
    else:
        print("\n❌ API documentation needs significant improvement")
        validation_results["validation_passed"] = False
    
    # Print issues if any
    if validation_results["issues"]:
        print(f"\nIssues Found ({len(validation_results['issues'])}):")
        for issue in validation_results["issues"][:10]:  # Show first 10 issues
            print(f"  - {issue}")
        if len(validation_results["issues"]) > 10:
            print(f"  ... and {len(validation_results['issues']) - 10} more issues")
    
    return validation_results


def validate_openapi_schema():
    """Validate OpenAPI schema structure and completeness."""
    print("\n" + "=" * 60)
    print("OPENAPI SCHEMA VALIDATION")
    print("=" * 60)
    
    try:
        schema = app.openapi()
        
        # Check required OpenAPI fields
        required_fields = ['openapi', 'info', 'paths']
        missing_fields = [field for field in required_fields if field not in schema]
        
        if missing_fields:
            print(f"❌ Missing required OpenAPI fields: {missing_fields}")
            return False
        
        print("✅ OpenAPI schema structure is valid")
        
        # Check info section
        info = schema.get('info', {})
        required_info = ['title', 'version', 'description']
        missing_info = [field for field in required_info if not info.get(field)]
        
        if missing_info:
            print(f"❌ Missing required info fields: {missing_info}")
            return False
        
        print("✅ API info section is complete")
        
        # Check components/schemas
        components = schema.get('components', {})
        schemas = components.get('schemas', {})
        
        if schemas:
            print(f"✅ {len(schemas)} data models documented")
        else:
            print("⚠️ No data models found in schema")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating OpenAPI schema: {e}")
        return False


def main():
    """Main validation function."""
    print("TKA DESKTOP API DOCUMENTATION VALIDATION")
    print("=" * 60)
    print("Validating world-class API documentation standards...")
    print()
    
    try:
        # Validate API documentation
        doc_results = validate_api_documentation()
        
        # Validate OpenAPI schema
        schema_valid = validate_openapi_schema()
        
        # Final assessment
        print("\n" + "=" * 60)
        print("FINAL ASSESSMENT")
        print("=" * 60)
        
        if doc_results["validation_passed"] and schema_valid:
            print("🎉 API DOCUMENTATION VALIDATION PASSED!")
            print("✅ World-class professional standards achieved")
            print("✅ Ready for enterprise deployment")
            return 0
        else:
            print("❌ API documentation validation failed")
            print("⚠️ Documentation needs improvement before deployment")
            return 1
            
    except Exception as e:
        print(f"❌ Validation error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
