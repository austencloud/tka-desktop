"""
Qt Compatibility Layer for TKA Desktop

A+ Enhancement: Automatic Qt version detection and compatibility management
to ensure seamless operation across different Qt versions.

ARCHITECTURE: Provides runtime Qt version detection, feature adaptation,
and compatibility fallbacks for unsupported Qt features.
"""

import sys
import logging
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum
import weakref

logger = logging.getLogger(__name__)


class QtVariant(Enum):
    """Supported Qt variants."""

    PYQT6 = "PyQt6"
    PYQT5 = "PyQt5"
    PYSIDE6 = "PySide6"
    PYSIDE2 = "PySide2"
    UNKNOWN = "Unknown"


@dataclass
class QtVersion:
    """Qt version information."""

    variant: QtVariant
    major: int
    minor: int
    patch: int
    version_string: str

    @property
    def version_tuple(self) -> Tuple[int, int, int]:
        """Get version as tuple for comparison."""
        return (self.major, self.minor, self.patch)

    def __str__(self) -> str:
        return f"{self.variant.value} {self.version_string}"


@dataclass
class QtEnvironment:
    """Complete Qt environment information."""

    version: QtVersion
    features: Dict[str, bool]
    modules: List[str]
    platform: str
    high_dpi_support: bool
    opengl_support: bool
    threading_support: bool


class QtCompatibilityManager:
    """
    Qt compatibility manager for automatic version detection and adaptation.

    A+ Enhancement: Provides automatic Qt version detection, feature adaptation,
    and compatibility fallbacks for robust Qt integration across versions.
    """

    def __init__(self):
        """Initialize Qt compatibility manager."""
        self._environment: Optional[QtEnvironment] = None
        self._feature_cache: Dict[str, bool] = {}
        self._compatibility_warnings: List[str] = []

        # Detect Qt environment on initialization
        self._detect_qt_environment()

        logger.info(
            f"Qt compatibility manager initialized: {self._environment.version}"
        )

    def _detect_qt_environment(self) -> None:
        """Detect current Qt environment and capabilities."""
        try:
            # Detect Qt variant and version
            version = self._detect_qt_version()

            # Detect available features
            features = self._detect_qt_features(version)

            # Detect available modules
            modules = self._detect_qt_modules(version)

            # Detect platform capabilities
            platform = sys.platform
            high_dpi_support = self._detect_high_dpi_support(version)
            opengl_support = self._detect_opengl_support(version)
            threading_support = self._detect_threading_support(version)

            self._environment = QtEnvironment(
                version=version,
                features=features,
                modules=modules,
                platform=platform,
                high_dpi_support=high_dpi_support,
                opengl_support=opengl_support,
                threading_support=threading_support,
            )

        except Exception as e:
            logger.error(f"Failed to detect Qt environment: {e}")
            # Create fallback environment
            self._environment = self._create_fallback_environment()

    def _detect_qt_version(self) -> QtVersion:
        """Detect Qt variant and version."""
        # Try PyQt6 first (preferred)
        try:
            import PyQt6.QtCore as QtCore

            version_str = QtCore.qVersion() or "6.0.0"
            major, minor, patch = map(int, version_str.split("."))
            return QtVersion(
                variant=QtVariant.PYQT6,
                major=major,
                minor=minor,
                patch=patch,
                version_string=version_str,
            )
        except ImportError:
            pass

        # Try PySide6
        try:
            import PySide6.QtCore as QtCore

            version_str = QtCore.qVersion()
            major, minor, patch = map(int, version_str.split("."))
            return QtVersion(
                variant=QtVariant.PYSIDE6,
                major=major,
                minor=minor,
                patch=patch,
                version_string=version_str,
            )
        except ImportError:
            pass

        # Try PyQt5
        try:
            import PyQt5.QtCore as QtCore

            version_str = QtCore.qVersion()
            major, minor, patch = map(int, version_str.split("."))
            return QtVersion(
                variant=QtVariant.PYQT5,
                major=major,
                minor=minor,
                patch=patch,
                version_string=version_str,
            )
        except ImportError:
            pass

        # Try PySide2
        try:
            import PySide2.QtCore as QtCore

            version_str = QtCore.qVersion()
            major, minor, patch = map(int, version_str.split("."))
            return QtVersion(
                variant=QtVariant.PYSIDE2,
                major=major,
                minor=minor,
                patch=patch,
                version_string=version_str,
            )
        except ImportError:
            pass

        # No Qt found
        logger.warning("No Qt installation detected")
        return QtVersion(
            variant=QtVariant.UNKNOWN, major=0, minor=0, patch=0, version_string="0.0.0"
        )

    def _detect_qt_features(self, version: QtVersion) -> Dict[str, bool]:
        """Detect available Qt features based on version."""
        features = {}

        if version.variant == QtVariant.UNKNOWN:
            return features

        try:
            # High DPI scaling (Qt 5.6+)
            features["high_dpi_scaling"] = version.major >= 6 or (
                version.major == 5 and version.minor >= 6
            )

            # OpenGL support
            features["opengl"] = self._test_opengl_support(version)

            # Threading support
            features["threading"] = True  # All Qt versions support threading

            # Async/await support (Qt 6.0+)
            features["async_support"] = version.major >= 6

            # Modern widgets (Qt 6.0+)
            features["modern_widgets"] = version.major >= 6

            # Enhanced graphics (Qt 5.12+)
            features["enhanced_graphics"] = version.major >= 6 or (
                version.major == 5 and version.minor >= 12
            )

            # Memory management improvements (Qt 6.0+)
            features["improved_memory_management"] = version.major >= 6

        except Exception as e:
            logger.warning(f"Error detecting Qt features: {e}")

        return features

    def _detect_qt_modules(self, version: QtVersion) -> List[str]:
        """Detect available Qt modules."""
        modules = []

        if version.variant == QtVariant.UNKNOWN:
            return modules

        # Standard modules to check
        module_names = [
            "QtCore",
            "QtGui",
            "QtWidgets",
            "QtOpenGL",
            "QtNetwork",
            "QtMultimedia",
            "QtSvg",
            "QtPrintSupport",
            "QtTest",
        ]

        variant_prefix = version.variant.value

        for module_name in module_names:
            try:
                __import__(f"{variant_prefix}.{module_name}")
                modules.append(module_name)
            except ImportError:
                pass

        return modules

    def _test_opengl_support(self, version: QtVersion) -> bool:
        """Test if OpenGL support is available."""
        try:
            variant_prefix = version.variant.value
            opengl_module = __import__(
                f"{variant_prefix}.QtOpenGL", fromlist=["QOpenGLWidget"]
            )
            return hasattr(opengl_module, "QOpenGLWidget")
        except ImportError:
            return False

    def _detect_high_dpi_support(self, version: QtVersion) -> bool:
        """Detect high DPI support."""
        return version.major >= 6 or (version.major == 5 and version.minor >= 6)

    def _detect_opengl_support(self, version: QtVersion) -> bool:
        """Detect OpenGL support."""
        return "QtOpenGL" in self._detect_qt_modules(version)

    def _detect_threading_support(self, version: QtVersion) -> bool:
        """Detect threading support."""
        return version.variant != QtVariant.UNKNOWN

    def _create_fallback_environment(self) -> QtEnvironment:
        """Create fallback environment when detection fails."""
        fallback_version = QtVersion(
            variant=QtVariant.UNKNOWN, major=0, minor=0, patch=0, version_string="0.0.0"
        )

        return QtEnvironment(
            version=fallback_version,
            features={},
            modules=[],
            platform=sys.platform,
            high_dpi_support=False,
            opengl_support=False,
            threading_support=False,
        )

    def get_environment(self) -> QtEnvironment:
        """Get current Qt environment information."""
        if self._environment is None:
            self._detect_qt_environment()
        assert self._environment is not None, "Qt environment detection failed"
        return self._environment

    def has_feature(self, feature_name: str) -> bool:
        """Check if a specific Qt feature is available."""
        if feature_name in self._feature_cache:
            return self._feature_cache[feature_name]

        available = self._environment.features.get(feature_name, False)
        self._feature_cache[feature_name] = available

        return available

    def require_feature(
        self, feature_name: str, fallback_message: Optional[str] = None
    ) -> bool:
        """Require a specific Qt feature, log warning if not available."""
        if self.has_feature(feature_name):
            return True

        warning_msg = (
            fallback_message or f"Required Qt feature '{feature_name}' is not available"
        )
        self._compatibility_warnings.append(warning_msg)
        logger.warning(warning_msg)

        return False

    def get_compatibility_warnings(self) -> List[str]:
        """Get list of compatibility warnings."""
        return self._compatibility_warnings.copy()

    def is_compatible_version(self, min_version: Tuple[int, int, int]) -> bool:
        """Check if current Qt version meets minimum requirements."""
        current_version = self._environment.version.version_tuple
        return current_version >= min_version

    def get_recommended_settings(self) -> Dict[str, Any]:
        """Get recommended Qt settings for current environment."""
        settings = {}

        # High DPI settings
        if self.has_feature("high_dpi_scaling"):
            settings["high_dpi_scaling"] = True
            settings["high_dpi_scale_factor_rounding_policy"] = "PassThrough"

        # OpenGL settings
        if self.has_feature("opengl"):
            settings["opengl_enabled"] = True
            settings["opengl_format"] = "OpenGL"

        # Threading settings
        if self.has_feature("threading"):
            settings["threading_enabled"] = True
            settings["max_thread_count"] = 4

        return settings


# Global compatibility manager instance
_qt_compat_manager: Optional[QtCompatibilityManager] = None


def qt_compat() -> QtCompatibilityManager:
    """Get global Qt compatibility manager instance."""
    global _qt_compat_manager
    if _qt_compat_manager is None:
        _qt_compat_manager = QtCompatibilityManager()
    return _qt_compat_manager
