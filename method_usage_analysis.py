#!/usr/bin/env python3
"""
TKA Desktop Modern - Method Usage Analysis Script
Phase 3: Deep Architecture Audit

This script analyzes method usage across the Modern codebase to identify:
- Unused methods that can be removed
- Over-engineered interfaces
- Bridge services that can be eliminated
- Complex DI features that aren't used

Generated: 2025-06-17
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple


class MethodUsageAnalyzer:
    """Analyzes method usage patterns in the TKA Modern codebase."""
    
    def __init__(self, modern_path: str):
        self.modern_path = Path(modern_path)
        self.src_path = self.modern_path / "src"
        self.report_lines = []
        
    def analyze_all(self) -> str:
        """Run complete method usage analysis."""
        self._add_header()
        self._analyze_layout_management_service()
        self._analyze_motion_management_service()
        self._analyze_di_container_features()
        self._analyze_bridge_services()
        self._analyze_interface_hierarchy()
        self._add_summary()
        
        return "\n".join(self.report_lines)
    
    def _add_header(self):
        """Add report header."""
        self.report_lines.extend([
            "🔍 TKA DESKTOP MODERN - METHOD USAGE ANALYSIS REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
            ""
        ])
    
    def _analyze_layout_management_service(self):
        """Analyze LayoutManagementService method usage."""
        self.report_lines.extend([
            "📊 LAYOUT MANAGEMENT SERVICE ANALYSIS:",
            "-" * 40
        ])
        
        # Methods to analyze from the audit
        layout_methods = [
            "calculate_context_aware_scaling",
            "get_layout_for_screen_size", 
            "calculate_component_positions",
            "_calculate_horizontal_beat_layout",
            "_calculate_grid_beat_layout",
            "_calculate_flow_layout",
            "_calculate_grid_layout",
            "calculate_beat_frame_layout",
            "calculate_responsive_scaling",
            "get_optimal_grid_layout",
            "get_main_window_size",
            "get_workbench_size",
            "get_picker_size",
            "get_layout_ratio",
            "set_layout_ratio",
            "calculate_component_size"
        ]
        
        for method in layout_methods:
            usage_count = self._count_method_usage(method)
            self._add_method_analysis(method, usage_count)
    
    def _analyze_motion_management_service(self):
        """Analyze MotionManagementService method usage."""
        self.report_lines.extend([
            "",
            "📊 MOTION MANAGEMENT SERVICE ANALYSIS:",
            "-" * 40
        ])
        
        motion_methods = [
            "generate_motion_combinations_for_letter",
            "calculate_prop_rotation_angle", 
            "_load_letter_specific_rules",
            "_validate_dependency_chain",
            "validate_motion_combination",
            "get_valid_motion_combinations",
            "calculate_motion_orientation",
            "get_motion_validation_errors"
        ]
        
        for method in motion_methods:
            usage_count = self._count_method_usage(method)
            self._add_method_analysis(method, usage_count)
    
    def _analyze_di_container_features(self):
        """Analyze DI Container complex features usage."""
        self.report_lines.extend([
            "",
            "📊 DI CONTAINER FEATURES ANALYSIS:",
            "-" * 40
        ])
        
        di_methods = [
            "auto_register_with_validation",
            "validate_all_registrations",
            "_detect_circular_dependencies", 
            "_create_with_lifecycle",
            "cleanup_all",
            "_validate_protocol_implementation",
            "_validate_dependency_chain",
            "register_transient",
            "register_singleton",
            "register_instance"
        ]
        
        for method in di_methods:
            usage_count = self._count_method_usage(method)
            self._add_method_analysis(method, usage_count)
    
    def _analyze_bridge_services(self):
        """Analyze bridge service usage patterns."""
        self.report_lines.extend([
            "",
            "📊 BRIDGE SERVICES ANALYSIS:",
            "-" * 40
        ])
        
        bridge_services = [
            "MotionManagementBridgeService",
            "LayoutManagementBridgeService"
        ]
        
        for service in bridge_services:
            usage_count = self._count_method_usage(service)
            self._add_method_analysis(service, usage_count, is_class=True)
            
            # Check if bridge service is registered in DI
            di_usage = self._count_method_usage(f"register_instance.*{service}")
            if di_usage > 0:
                self.report_lines.append(f"   🔗 Registered in DI container: {di_usage} times")
    
    def _analyze_interface_hierarchy(self):
        """Analyze interface implementation patterns."""
        self.report_lines.extend([
            "",
            "📊 INTERFACE HIERARCHY ANALYSIS:",
            "-" * 40
        ])
        
        # Check for classes implementing multiple interfaces
        interface_patterns = [
            ("ILayoutManagementService", "ILayoutService"),
            ("IMotionManagementService", "IMotionValidationService"),
            ("IBeatLayoutService", "IResponsiveLayoutService")
        ]
        
        for interface1, interface2 in interface_patterns:
            # Look for classes implementing both interfaces
            combined_usage = self._search_for_pattern(f"class.*{interface1}.*{interface2}")
            if combined_usage:
                self.report_lines.append(f"⚠️  Multiple interface implementation found:")
                self.report_lines.append(f"   {interface1} + {interface2}")
                self.report_lines.append(f"   Instances: {len(combined_usage)}")
    
    def _count_method_usage(self, method_name: str) -> int:
        """Count how many times a method is used in the codebase."""
        try:
            # Use grep to search for method usage
            result = subprocess.run(
                ["grep", "-r", method_name, str(self.src_path)],
                capture_output=True,
                text=True,
                cwd=self.modern_path
            )
            
            if result.returncode == 0:
                # Count non-empty lines (actual matches)
                lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                return len(lines)
            else:
                return 0
                
        except Exception as e:
            self.report_lines.append(f"   ❌ Error analyzing {method_name}: {e}")
            return -1
    
    def _search_for_pattern(self, pattern: str) -> List[str]:
        """Search for a specific pattern in the codebase."""
        try:
            result = subprocess.run(
                ["grep", "-r", "-E", pattern, str(self.src_path)],
                capture_output=True,
                text=True,
                cwd=self.modern_path
            )
            
            if result.returncode == 0:
                return [line.strip() for line in result.stdout.split('\n') if line.strip()]
            else:
                return []
                
        except Exception:
            return []
    
    def _add_method_analysis(self, method_name: str, usage_count: int, is_class: bool = False):
        """Add method analysis to report."""
        if usage_count == -1:
            self.report_lines.append(f"🔍 {method_name}: ERROR in analysis")
        elif usage_count == 0:
            self.report_lines.append(f"🔍 {method_name}:")
            self.report_lines.append("   ❌ UNUSED - Consider removing")
        elif usage_count == 1:
            self.report_lines.append(f"🔍 {method_name}:")
            self.report_lines.append("   ⚠️  Used only once - Verify necessity")
        elif usage_count <= 3:
            self.report_lines.append(f"🔍 {method_name}:")
            self.report_lines.append(f"   ⚠️  Low usage ({usage_count} times) - Review necessity")
        else:
            self.report_lines.append(f"🔍 {method_name}:")
            self.report_lines.append(f"   ✅ Well used ({usage_count} times)")
    
    def _add_summary(self):
        """Add analysis summary and recommendations."""
        self.report_lines.extend([
            "",
            "🎯 ANALYSIS SUMMARY & RECOMMENDATIONS:",
            "=" * 50,
            "",
            "IMMEDIATE ACTIONS:",
            "1. Remove methods marked as UNUSED",
            "2. Review single-use methods for necessity", 
            "3. Consider consolidating low-usage methods",
            "4. Plan bridge service elimination",
            "",
            "INTERFACE CONSOLIDATION:",
            "1. Merge redundant interface hierarchies",
            "2. Simplify over-engineered abstractions",
            "3. Reduce method signature complexity",
            "",
            "DI CONTAINER SIMPLIFICATION:",
            "1. Remove unused validation features",
            "2. Simplify lifecycle management",
            "3. Consider lighter DI approach",
            "",
            "ESTIMATED CODE REDUCTION: 500-800 lines",
            "RISK LEVEL: MEDIUM (requires careful testing)",
            ""
        ])


def main():
    """Main entry point for method usage analysis."""
    # Determine the modern path
    if len(sys.argv) > 1:
        modern_path = sys.argv[1]
    else:
        # Default to current directory if run from modern/
        modern_path = "."
        
    # Validate path
    modern_path = Path(modern_path).resolve()
    if not (modern_path / "src").exists():
        print(f"❌ Error: {modern_path}/src not found")
        print("Usage: python method_usage_analysis.py [path_to_modern]")
        return 1
    
    print(f"🔍 Analyzing method usage in: {modern_path}")
    
    # Run analysis
    analyzer = MethodUsageAnalyzer(str(modern_path))
    report = analyzer.analyze_all()
    
    # Write report to file
    report_file = modern_path / "method_usage_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Also print to console
    print(report)
    print(f"\n✅ Method usage analysis complete!")
    print(f"📄 Report saved to: {report_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
