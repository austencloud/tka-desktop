# Version-Aware Path Management System
"""
Centralized path management for V1 and V2 versions of the Kinetic Constructor.

This module provides version-aware path resolution to eliminate hardcoded paths
and ensure correct file loading across different versions.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Union
from enum import Enum


class Version(Enum):
    V1 = "v1"
    V2 = "v2"


class VersionPathManager:
    """
    Centralized path management for version-specific file access.
    
    Automatically detects version context and provides correct paths
    for data files, assets, and configuration files.
    """
    
    def __init__(self):
        self.project_root = self._find_project_root()
        self.v1_root = self.project_root / "v1"
        self.v2_root = self.project_root / "v2"
        
    def _find_project_root(self) -> Path:
        """Find the project root directory containing v1/ and v2/ folders."""
        current = Path(__file__).parent
        
        # Walk up the directory tree to find project root
        while current.parent != current:
            if (current / "v1").exists() and (current / "v2").exists():
                return current
            current = current.parent
            
        # Fallback to launcher parent directory
        return Path(__file__).parent.parent.parent
    
    def detect_version_from_context(self) -> Version:
        """
        Detect version based on current execution context.
        
        Returns:
            Version.V1 or Version.V2 based on calling context
        """
        # Get the calling frame to determine version context
        frame = sys._getframe(1)
        calling_file = frame.f_code.co_filename
        
        if "v1" in calling_file or "\\v1\\" in calling_file or "/v1/" in calling_file:
            return Version.V1
        elif "v2" in calling_file or "\\v2\\" in calling_file or "/v2/" in calling_file:
            return Version.V2
        else:
            # Default to V2 for launcher and other contexts
            return Version.V2
    
    def get_data_path(self, relative_path: str, version: Optional[Version] = None) -> str:
        """
        Get version-specific data file path.
        
        Args:
            relative_path: Path relative to data directory (e.g., "arrow_placement/diamond/default/file.json")
            version: Specific version to use, or None for auto-detection
            
        Returns:
            Absolute path to the data file
        """
        if version is None:
            version = self.detect_version_from_context()
            
        if version == Version.V1:
            base_path = self.v1_root / "data"
        else:  # V2
            base_path = self.v2_root / "src" / "data"
            
        full_path = base_path / relative_path
        return str(full_path)
    
    def get_image_path(self, relative_path: str, version: Optional[Version] = None) -> str:
        """
        Get version-specific image/asset file path.
        
        Args:
            relative_path: Path relative to images directory (e.g., "grid/diamond_grid.svg")
            version: Specific version to use, or None for auto-detection
            
        Returns:
            Absolute path to the image file
        """
        if version is None:
            version = self.detect_version_from_context()
            
        if version == Version.V1:
            base_path = self.v1_root / "images"
        else:  # V2
            # V2 uses assets directory (copied from V1)
            base_path = self.v2_root / "src" / "assets" / "images"
            
        full_path = base_path / relative_path
        return str(full_path)
    
    def get_src_path(self, relative_path: str, version: Optional[Version] = None) -> str:
        """
        Get version-specific source file path.
        
        Args:
            relative_path: Path relative to src directory
            version: Specific version to use, or None for auto-detection
            
        Returns:
            Absolute path to the source file
        """
        if version is None:
            version = self.detect_version_from_context()
            
        if version == Version.V1:
            base_path = self.v1_root / "src"
        else:  # V2
            base_path = self.v2_root / "src"
            
        full_path = base_path / relative_path
        return str(full_path)
    
    def ensure_v2_assets_exist(self):
        """
        Ensure V2 assets directory exists and copy V1 assets if needed.
        
        This implements the requirement to copy V1 assets to v2/src/assets/
        for V2 compatibility.
        """
        v2_assets_dir = self.v2_root / "src" / "assets"
        v2_images_dir = v2_assets_dir / "images"
        v1_images_dir = self.v1_root / "images"
        
        # Create V2 assets directory structure
        v2_assets_dir.mkdir(exist_ok=True)
        v2_images_dir.mkdir(exist_ok=True)
        
        # Copy V1 images to V2 assets if V1 images exist and V2 is missing files
        if v1_images_dir.exists():
            self._copy_assets_if_needed(v1_images_dir, v2_images_dir)
    
    def _copy_assets_if_needed(self, source_dir: Path, target_dir: Path):
        """Copy assets from source to target if target is missing files."""
        import shutil
        
        # Key asset files that should exist in V2
        key_assets = [
            "grid/diamond_grid.svg",
            "grid/box_grid.svg", 
            "grid/diamond_nonradial_points.svg",
            "same_opp_dot.svg"
        ]
        
        for asset in key_assets:
            source_file = source_dir / asset
            target_file = target_dir / asset
            
            if source_file.exists() and not target_file.exists():
                # Create target directory if needed
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    shutil.copy2(source_file, target_file)
                    print(f"✅ Copied asset: {asset} to V2")
                except Exception as e:
                    print(f"⚠️ Failed to copy {asset}: {e}")
    
    def file_exists(self, relative_path: str, path_type: str = "data", 
                   version: Optional[Version] = None) -> bool:
        """
        Check if a version-specific file exists.
        
        Args:
            relative_path: Path relative to the specified directory type
            path_type: Type of path ("data", "image", "src")
            version: Specific version to use, or None for auto-detection
            
        Returns:
            True if file exists, False otherwise
        """
        if path_type == "data":
            full_path = self.get_data_path(relative_path, version)
        elif path_type == "image":
            full_path = self.get_image_path(relative_path, version)
        elif path_type == "src":
            full_path = self.get_src_path(relative_path, version)
        else:
            raise ValueError(f"Unknown path_type: {path_type}")
            
        return os.path.exists(full_path)
    
    def get_arrow_placement_path(self, grid_mode: str, placement_type: str, 
                                filename: str, version: Optional[Version] = None) -> str:
        """
        Get path to arrow placement JSON files.
        
        Args:
            grid_mode: "diamond" or "box"
            placement_type: "default" or "special"
            filename: Name of the JSON file
            version: Specific version to use, or None for auto-detection
            
        Returns:
            Absolute path to the arrow placement file
        """
        relative_path = f"arrow_placement/{grid_mode}/{placement_type}/{filename}"
        return self.get_data_path(relative_path, version)
    
    def get_all_arrow_placement_files(self, version: Optional[Version] = None) -> dict:
        """
        Get all arrow placement file paths for a version.
        
        Returns:
            Dictionary mapping file types to their paths
        """
        if version is None:
            version = self.detect_version_from_context()
            
        files = {}
        
        for grid_mode in ["diamond", "box"]:
            files[grid_mode] = {}
            for motion_type in ["pro", "anti", "float", "dash", "static"]:
                filename = f"default_{grid_mode}_{motion_type}_placements.json"
                path = self.get_arrow_placement_path(grid_mode, "default", filename, version)
                files[grid_mode][motion_type] = path
                
        return files


# Global instance for easy access
_path_manager = None

def get_path_manager() -> VersionPathManager:
    """Get the global VersionPathManager instance."""
    global _path_manager
    if _path_manager is None:
        _path_manager = VersionPathManager()
        # Ensure V2 assets exist on first access
        _path_manager.ensure_v2_assets_exist()
    return _path_manager


# Convenience functions for common use cases
def get_version_aware_data_path(relative_path: str, version: Optional[Version] = None) -> str:
    """Get version-aware data path."""
    return get_path_manager().get_data_path(relative_path, version)

def get_version_aware_image_path(relative_path: str, version: Optional[Version] = None) -> str:
    """Get version-aware image path."""
    return get_path_manager().get_image_path(relative_path, version)

def get_arrow_placement_file_path(grid_mode: str, motion_type: str, version: Optional[Version] = None) -> str:
    """Get path to specific arrow placement file."""
    filename = f"default_{grid_mode}_{motion_type}_placements.json"
    return get_path_manager().get_arrow_placement_path(grid_mode, "default", filename, version)
