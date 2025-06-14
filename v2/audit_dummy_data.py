#!/usr/bin/env python3
"""
Dummy Data Audit Script for TKA V2
===================================

This script audits the V2 codebase for dummy data violations and ensures
all components use real data from PictographDatasetService.

Phase 0 - Day 1: Eliminate Dummy Data
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class DummyDataAuditor:
    """Auditor for finding dummy data violations in V2 codebase."""
    
    def __init__(self, v2_root: Path):
        self.v2_root = v2_root
        self.violations = []
        
        # Patterns that indicate dummy data usage
        self.dummy_patterns = [
            # BeatData with hardcoded letters
            (r'BeatData\([^)]*letter=["\'](A|B|C|X|TEST|DUMMY)["\']', 'Hardcoded letter in BeatData'),
            
            # Motion data with obvious dummy values
            (r'MotionData\([^)]*motion_type=MotionType\.(PRO|ANTI)[^)]*start_loc=Location\.NORTH[^)]*end_loc=Location\.SOUTH', 'Dummy motion pattern'),
            
            # Hardcoded position keys that aren't real
            (r'["\'](test_position|dummy_pos|fake_alpha)["\']', 'Fake position key'),
            
            # Empty or placeholder letters
            (r'letter=["\']["\']\s*,', 'Empty letter field'),
            
            # Test-specific dummy data
            (r'letter=["\'](TEST|SAMPLE|DEMO)["\']', 'Test dummy data'),
        ]
        
        # Files to exclude from audit
        self.exclude_patterns = [
            r'__pycache__',
            r'\.pyc$',
            r'audit_dummy_data\.py$',  # This file
            r'test_.*\.py$',  # Test files (we'll audit separately)
        ]
    
    def should_exclude_file(self, file_path: Path) -> bool:
        """Check if file should be excluded from audit."""
        file_str = str(file_path)
        return any(re.search(pattern, file_str) for pattern in self.exclude_patterns)
    
    def audit_file(self, file_path: Path) -> List[Dict]:
        """Audit a single file for dummy data violations."""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            for line_num, line in enumerate(lines, 1):
                for pattern, description in self.dummy_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        violations.append({
                            'file': file_path,
                            'line': line_num,
                            'content': line.strip(),
                            'pattern': pattern,
                            'description': description,
                            'severity': 'HIGH' if 'BeatData' in line else 'MEDIUM'
                        })
                        
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            
        return violations
    
    def audit_directory(self, directory: Path) -> None:
        """Audit all Python files in directory recursively."""
        for file_path in directory.rglob("*.py"):
            if self.should_exclude_file(file_path):
                continue
                
            file_violations = self.audit_file(file_path)
            self.violations.extend(file_violations)
    
    def audit_test_files(self) -> None:
        """Separately audit test files for dummy data."""
        print("\n🧪 AUDITING TEST FILES:")
        print("=" * 50)
        
        test_violations = []
        test_files = list(self.v2_root.glob("test_*.py"))
        
        for test_file in test_files:
            violations = self.audit_file(test_file)
            if violations:
                test_violations.extend(violations)
                
        if test_violations:
            print(f"❌ Found {len(test_violations)} dummy data violations in test files:")
            for violation in test_violations:
                print(f"   📁 {violation['file'].name}:{violation['line']}")
                print(f"      {violation['description']}")
                print(f"      Code: {violation['content']}")
                print()
        else:
            print("✅ No dummy data violations found in test files!")
    
    def generate_report(self) -> None:
        """Generate comprehensive audit report."""
        print("\n📊 DUMMY DATA AUDIT REPORT")
        print("=" * 60)
        
        if not self.violations:
            print("✅ NO DUMMY DATA VIOLATIONS FOUND!")
            print("   All components are using real data from PictographDatasetService")
            return
            
        # Group violations by severity
        high_severity = [v for v in self.violations if v['severity'] == 'HIGH']
        medium_severity = [v for v in self.violations if v['severity'] == 'MEDIUM']
        
        print(f"❌ FOUND {len(self.violations)} TOTAL VIOLATIONS:")
        print(f"   🚨 High Severity: {len(high_severity)}")
        print(f"   ⚠️  Medium Severity: {len(medium_severity)}")
        print()
        
        # Report high severity violations first
        if high_severity:
            print("🚨 HIGH SEVERITY VIOLATIONS (Must Fix):")
            print("-" * 40)
            for violation in high_severity:
                print(f"📁 {violation['file'].relative_to(self.v2_root)}:{violation['line']}")
                print(f"   {violation['description']}")
                print(f"   Code: {violation['content']}")
                print()
                
        # Report medium severity violations
        if medium_severity:
            print("⚠️  MEDIUM SEVERITY VIOLATIONS (Should Fix):")
            print("-" * 40)
            for violation in medium_severity:
                print(f"📁 {violation['file'].relative_to(self.v2_root)}:{violation['line']}")
                print(f"   {violation['description']}")
                print(f"   Code: {violation['content']}")
                print()
    
    def generate_fix_recommendations(self) -> None:
        """Generate specific fix recommendations."""
        if not self.violations:
            return
            
        print("🔧 FIX RECOMMENDATIONS:")
        print("=" * 40)
        print("Replace dummy data with real dataset calls:")
        print()
        print("❌ WRONG:")
        print("   BeatData(letter='A', blue_motion=...)")
        print()
        print("✅ CORRECT:")
        print("   dataset_service = PictographDatasetService()")
        print("   real_beat = dataset_service.get_start_position_pictograph('alpha1_alpha1', 'diamond')")
        print()
        print("Available real positions:")
        print("   - alpha1_alpha1 (diamond)")
        print("   - beta5_beta5 (diamond)")  
        print("   - gamma11_gamma11 (diamond)")
        print("   - alpha2_alpha2 (box)")
        print("   - beta4_beta4 (box)")
        print("   - gamma12_gamma12 (box)")


def main():
    """Main audit function."""
    print("🔍 TKA V2 DUMMY DATA AUDIT")
    print("=" * 60)
    print("Phase 0 - Day 1: Eliminate Dummy Data")
    print("Scanning for dummy data violations...")
    print()
    
    # Get V2 root directory
    v2_root = Path(__file__).parent
    
    # Create auditor
    auditor = DummyDataAuditor(v2_root)
    
    # Audit main source directories
    print("📂 Auditing main source directories...")
    src_dir = v2_root / "src"
    if src_dir.exists():
        auditor.audit_directory(src_dir)
    
    # Audit test files separately
    auditor.audit_test_files()
    
    # Generate reports
    auditor.generate_report()
    auditor.generate_fix_recommendations()
    
    # Return exit code based on violations
    if auditor.violations:
        print(f"\n❌ AUDIT FAILED: {len(auditor.violations)} violations found")
        return 1
    else:
        print("\n✅ AUDIT PASSED: No dummy data violations found")
        return 0


if __name__ == "__main__":
    sys.exit(main())
