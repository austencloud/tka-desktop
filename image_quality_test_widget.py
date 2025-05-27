#!/usr/bin/env python3
"""
Image Quality Test Widget

This standalone test widget allows visual comparison of different image scaling methods
to identify the best approach for thumbnail quality in the browse tab.
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox,
    QScrollArea,
    QFrame,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QCheckBox,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QPainter, QColor
from typing import Optional

# Try to import PIL for advanced processing
try:
    from PIL import Image as PILImage, ImageFilter, ImageEnhance

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL/Pillow not available - some methods will be disabled")

# Add src to path to import project utilities
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

# Import dictionary path helper
try:
    from utils.path_helpers import get_dictionary_path

    DICTIONARY_PATH_AVAILABLE = True
except ImportError:
    print("⚠️ Dictionary path helper not available - using fallback paths")
    DICTIONARY_PATH_AVAILABLE = False


class ImageScalingMethod:
    """Represents a single image scaling method for testing."""

    def __init__(self, name: str, description: str, method_func):
        self.name = name
        self.description = description
        self.method_func = method_func


class ImageQualityTestWidget(QMainWindow):
    """Main test widget for comparing image scaling methods."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Quality Test - Browse Tab Thumbnail Scaling")
        self.setGeometry(100, 100, 1400, 900)

        # Test parameters
        self.current_image_path: Optional[str] = None
        self.original_pixmap: Optional[QPixmap] = None
        self.target_size = QSize(200, 150)  # Default thumbnail size

        # Dictionary images
        self.dictionary_images: list[str] = []
        self.dictionary_combo: Optional[QComboBox] = None

        # Scaling methods to test
        self.scaling_methods = self._create_scaling_methods()

        self._setup_ui()
        self._load_dictionary_images()
        self._load_sample_image()

    def _setup_ui(self):
        """Set up the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Controls section
        controls_frame = self._create_controls_section()
        main_layout.addWidget(controls_frame)

        # Results section
        results_scroll = self._create_results_section()
        main_layout.addWidget(results_scroll)

        # Status bar
        self.statusBar().showMessage("Ready - Load an image to start testing")

    def _create_controls_section(self) -> QFrame:
        """Create the controls section."""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setMaximumHeight(120)

        layout = QHBoxLayout(frame)

        # Image selection
        image_group = QGroupBox("Image Selection")
        image_layout = QVBoxLayout(image_group)

        # Dictionary images dropdown
        dict_layout = QHBoxLayout()
        dict_layout.addWidget(QLabel("Dictionary Images:"))
        self.dictionary_combo = QComboBox()
        self.dictionary_combo.setMinimumWidth(200)
        self.dictionary_combo.currentTextChanged.connect(
            self._on_dictionary_selection_changed
        )
        dict_layout.addWidget(self.dictionary_combo)
        dict_layout.addStretch()
        image_layout.addLayout(dict_layout)

        # Manual file selection (fallback)
        self.load_button = QPushButton("Load Other Image...")
        self.load_button.clicked.connect(self._load_image)
        image_layout.addWidget(self.load_button)

        # Current image info
        self.image_path_label = QLabel("No image loaded")
        self.image_path_label.setStyleSheet("color: gray; font-style: italic;")
        self.image_path_label.setWordWrap(True)
        image_layout.addWidget(self.image_path_label)

        layout.addWidget(image_group)

        # Size controls
        size_group = QGroupBox("Target Size")
        size_layout = QVBoxLayout(size_group)

        size_controls = QHBoxLayout()
        size_controls.addWidget(QLabel("Width:"))
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(50, 800)
        self.width_spinbox.setValue(200)
        self.width_spinbox.valueChanged.connect(self._update_target_size)
        size_controls.addWidget(self.width_spinbox)

        size_controls.addWidget(QLabel("Height:"))
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(50, 600)
        self.height_spinbox.setValue(150)
        self.height_spinbox.valueChanged.connect(self._update_target_size)
        size_controls.addWidget(self.height_spinbox)

        size_layout.addLayout(size_controls)

        # Preset sizes
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Presets:"))

        small_btn = QPushButton("Small (150x112)")
        small_btn.clicked.connect(lambda: self._set_preset_size(150, 112))
        preset_layout.addWidget(small_btn)

        medium_btn = QPushButton("Medium (200x150)")
        medium_btn.clicked.connect(lambda: self._set_preset_size(200, 150))
        preset_layout.addWidget(medium_btn)

        large_btn = QPushButton("Large (300x225)")
        large_btn.clicked.connect(lambda: self._set_preset_size(300, 225))
        preset_layout.addWidget(large_btn)

        size_layout.addLayout(preset_layout)
        layout.addWidget(size_group)

        # Test controls
        test_group = QGroupBox("Test Controls")
        test_layout = QVBoxLayout(test_group)

        self.run_test_button = QPushButton("🔄 Run All Tests")
        self.run_test_button.clicked.connect(self._run_all_tests)
        self.run_test_button.setStyleSheet(
            "QPushButton { font-weight: bold; padding: 8px; }"
        )
        test_layout.addWidget(self.run_test_button)

        self.auto_update_checkbox = QCheckBox("Auto-update on changes")
        self.auto_update_checkbox.setChecked(True)
        test_layout.addWidget(self.auto_update_checkbox)

        layout.addWidget(test_group)

        return frame

    def _create_results_section(self) -> QScrollArea:
        """Create the results display section."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.results_widget = QWidget()
        self.results_layout = QGridLayout(self.results_widget)
        self.results_layout.setSpacing(10)

        scroll_area.setWidget(self.results_widget)
        return scroll_area

    def _create_scaling_methods(self) -> list[ImageScalingMethod]:
        """Create list of scaling methods to test."""
        methods = []

        # Qt-based methods
        methods.append(
            ImageScalingMethod(
                "Qt Fast Transform",
                "Qt's FastTransformation - fastest but lowest quality",
                self._qt_fast_transform,
            )
        )

        methods.append(
            ImageScalingMethod(
                "Qt Smooth Transform",
                "Qt's SmoothTransformation - good balance",
                self._qt_smooth_transform,
            )
        )

        methods.append(
            ImageScalingMethod(
                "Qt Multi-Step (2 stages)",
                "Two-stage Qt scaling for better quality",
                self._qt_multistep_2_transform,
            )
        )

        methods.append(
            ImageScalingMethod(
                "Qt Multi-Step (3 stages)",
                "Three-stage Qt scaling for maximum quality",
                self._qt_multistep_3_transform,
            )
        )

        # PIL-based methods (if available)
        if PIL_AVAILABLE:
            methods.append(
                ImageScalingMethod(
                    "PIL Lanczos",
                    "PIL Lanczos resampling - high quality",
                    self._pil_lanczos,
                )
            )

            methods.append(
                ImageScalingMethod(
                    "PIL Lanczos + Sharpen",
                    "PIL Lanczos with unsharp mask filter",
                    self._pil_lanczos_sharpen,
                )
            )

            methods.append(
                ImageScalingMethod(
                    "PIL Lanczos + Enhance",
                    "PIL Lanczos with contrast/brightness enhancement",
                    self._pil_lanczos_enhance,
                )
            )

            methods.append(
                ImageScalingMethod(
                    "PIL Multi-Step Lanczos",
                    "Multi-stage PIL Lanczos for extreme quality",
                    self._pil_multistep_lanczos,
                )
            )

        return methods

    # Qt-based scaling methods
    def _qt_fast_transform(self, pixmap: QPixmap, target_size: QSize) -> QPixmap:
        """Qt FastTransformation scaling."""
        return pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation,
        )

    def _qt_smooth_transform(self, pixmap: QPixmap, target_size: QSize) -> QPixmap:
        """Qt SmoothTransformation scaling."""
        return pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def _qt_multistep_2_transform(self, pixmap: QPixmap, target_size: QSize) -> QPixmap:
        """Two-stage Qt scaling."""
        original_size = pixmap.size()
        scale_factor = min(
            target_size.width() / original_size.width(),
            target_size.height() / original_size.height(),
        )

        if scale_factor >= 0.75:
            # Single step for small scale changes
            return self._qt_smooth_transform(pixmap, target_size)

        # Two-stage scaling
        intermediate_factor = 0.75
        intermediate_size = QSize(
            int(original_size.width() * intermediate_factor),
            int(original_size.height() * intermediate_factor),
        )

        # Stage 1
        intermediate_pixmap = pixmap.scaled(
            intermediate_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Stage 2
        return intermediate_pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def _qt_multistep_3_transform(self, pixmap: QPixmap, target_size: QSize) -> QPixmap:
        """Three-stage Qt scaling."""
        original_size = pixmap.size()
        scale_factor = min(
            target_size.width() / original_size.width(),
            target_size.height() / original_size.height(),
        )

        if scale_factor >= 0.75:
            return self._qt_smooth_transform(pixmap, target_size)
        elif scale_factor >= 0.4:
            return self._qt_multistep_2_transform(pixmap, target_size)

        # Three-stage scaling for very small targets
        stage1_factor = 0.7
        stage2_factor = 0.5

        # Stage 1
        stage1_size = QSize(
            int(original_size.width() * stage1_factor),
            int(original_size.height() * stage1_factor),
        )
        stage1_pixmap = pixmap.scaled(
            stage1_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Stage 2
        stage2_size = QSize(
            int(original_size.width() * stage2_factor),
            int(original_size.height() * stage2_factor),
        )
        stage2_pixmap = stage1_pixmap.scaled(
            stage2_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Stage 3
        return stage2_pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    # PIL-based scaling methods
    def _pil_lanczos(self, pixmap: QPixmap, target_size: QSize) -> QPixmap:
        """PIL Lanczos resampling."""
        if not PIL_AVAILABLE:
            return self._qt_smooth_transform(pixmap, target_size)

        # Convert QPixmap to PIL Image
        pil_image = self._qpixmap_to_pil(pixmap)
        if not pil_image:
            return self._qt_smooth_transform(pixmap, target_size)

        # Calculate target size maintaining aspect ratio
        original_size = pil_image.size
        scale_factor = min(
            target_size.width() / original_size[0],
            target_size.height() / original_size[1],
        )

        new_size = (
            int(original_size[0] * scale_factor),
            int(original_size[1] * scale_factor),
        )

        # Resize with Lanczos
        resized_image = pil_image.resize(new_size, PILImage.Resampling.LANCZOS)

        # Convert back to QPixmap
        return self._pil_to_qpixmap(resized_image)

    def _pil_lanczos_sharpen(self, pixmap: QPixmap, target_size: QSize) -> QPixmap:
        """PIL Lanczos with sharpening."""
        if not PIL_AVAILABLE:
            return self._qt_smooth_transform(pixmap, target_size)

        # Start with Lanczos resize
        result_pixmap = self._pil_lanczos(pixmap, target_size)

        # Apply sharpening
        pil_image = self._qpixmap_to_pil(result_pixmap)
        if pil_image:
            # Apply unsharp mask
            sharpened = pil_image.filter(
                ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3)
            )
            return self._pil_to_qpixmap(sharpened)

        return result_pixmap

    def _pil_lanczos_enhance(self, pixmap: QPixmap, target_size: QSize) -> QPixmap:
        """PIL Lanczos with enhancement."""
        if not PIL_AVAILABLE:
            return self._qt_smooth_transform(pixmap, target_size)

        # Start with Lanczos resize
        result_pixmap = self._pil_lanczos(pixmap, target_size)

        # Apply enhancement
        pil_image = self._qpixmap_to_pil(result_pixmap)
        if pil_image:
            # Enhance contrast and sharpness
            enhancer = ImageEnhance.Contrast(pil_image)
            enhanced = enhancer.enhance(1.1)  # Slight contrast boost

            enhancer = ImageEnhance.Sharpness(enhanced)
            enhanced = enhancer.enhance(1.2)  # Slight sharpness boost

            return self._pil_to_qpixmap(enhanced)

        return result_pixmap

    def _pil_multistep_lanczos(self, pixmap: QPixmap, target_size: QSize) -> QPixmap:
        """Multi-step PIL Lanczos for extreme quality."""
        if not PIL_AVAILABLE:
            return self._qt_multistep_3_transform(pixmap, target_size)

        pil_image = self._qpixmap_to_pil(pixmap)
        if not pil_image:
            return self._qt_multistep_3_transform(pixmap, target_size)

        original_size = pil_image.size
        scale_factor = min(
            target_size.width() / original_size[0],
            target_size.height() / original_size[1],
        )

        if scale_factor >= 0.75:
            # Single step for small changes
            return self._pil_lanczos(pixmap, target_size)

        # Multi-step scaling
        current_image = pil_image
        steps = []

        if scale_factor < 0.25:
            steps = [0.7, 0.5, 0.35]
        elif scale_factor < 0.5:
            steps = [0.7, 0.5]
        else:
            steps = [0.75]

        # Apply each scaling step
        for step_factor in steps:
            step_size = (
                int(original_size[0] * step_factor),
                int(original_size[1] * step_factor),
            )
            current_image = current_image.resize(step_size, PILImage.Resampling.LANCZOS)

        # Final resize to exact target
        final_size = (
            int(original_size[0] * scale_factor),
            int(original_size[1] * scale_factor),
        )
        current_image = current_image.resize(final_size, PILImage.Resampling.LANCZOS)

        # Apply final sharpening
        current_image = current_image.filter(
            ImageFilter.UnsharpMask(radius=0.8, percent=120, threshold=2)
        )

        return self._pil_to_qpixmap(current_image)

    # Utility methods for PIL conversion
    def _qpixmap_to_pil(self, pixmap: QPixmap):
        """Convert QPixmap to PIL Image."""
        if not PIL_AVAILABLE:
            return None

        try:
            # Convert to QImage first
            qimage = pixmap.toImage()

            # Convert to bytes
            buffer = qimage.bits().asstring(qimage.sizeInBytes())

            # Create PIL image
            pil_image = PILImage.frombuffer(
                "RGBA" if qimage.hasAlphaChannel() else "RGB",
                (qimage.width(), qimage.height()),
                buffer,
                "raw",
                "BGRA" if qimage.hasAlphaChannel() else "BGR",
                0,
                1,
            )

            # Convert to RGB if needed
            if pil_image.mode == "RGBA":
                # Create white background
                background = PILImage.new("RGB", pil_image.size, (255, 255, 255))
                background.paste(pil_image, mask=pil_image.split()[-1])
                return background

            return pil_image
        except Exception as e:
            print(f"Error converting QPixmap to PIL: {e}")
            return None

    def _pil_to_qpixmap(self, pil_image) -> QPixmap:
        """Convert PIL Image to QPixmap."""
        if not PIL_AVAILABLE or not pil_image:
            return QPixmap()

        try:
            # Convert to RGB if needed
            if pil_image.mode != "RGB":
                pil_image = pil_image.convert("RGB")

            # Convert to bytes
            data = pil_image.tobytes("raw", "RGB")

            # Create QImage
            qimage = QImage(
                data, pil_image.width, pil_image.height, QImage.Format.Format_RGB888
            )

            # Convert to QPixmap
            return QPixmap.fromImage(qimage)
        except Exception as e:
            print(f"Error converting PIL to QPixmap: {e}")
            return QPixmap()

    # Dictionary image management
    def _load_dictionary_images(self):
        """Load all available dictionary images."""
        self.dictionary_images = []

        try:
            # Get dictionary path
            if DICTIONARY_PATH_AVAILABLE:
                dictionary_path = get_dictionary_path()
            else:
                # Fallback paths
                possible_paths = [
                    Path("src/data/dictionary"),
                    Path("data/dictionary"),
                    Path("dictionary"),
                    Path("../data/dictionary"),
                ]

                dictionary_path = None
                for path in possible_paths:
                    if path.exists():
                        dictionary_path = str(path)
                        break

                if not dictionary_path:
                    self._show_dictionary_error("Dictionary folder not found")
                    return

            dictionary_path = Path(dictionary_path)

            if not dictionary_path.exists():
                self._show_dictionary_error(
                    f"Dictionary path does not exist: {dictionary_path}"
                )
                return

            # Scan for PNG files in all word subdirectories
            png_files = []
            for word_dir in dictionary_path.iterdir():
                if word_dir.is_dir() and not word_dir.name.startswith("__"):
                    for png_file in word_dir.glob("*.png"):
                        if not png_file.name.startswith("__"):
                            png_files.append(png_file)

            if not png_files:
                self._show_dictionary_error("No PNG files found in dictionary")
                return

            # Sort by word name, then filename
            png_files.sort(key=lambda p: (p.parent.name, p.name))

            # Store full paths and create display names
            for png_file in png_files:
                self.dictionary_images.append(str(png_file))

            # Populate dropdown
            self._populate_dictionary_dropdown()

            print(f"✅ Found {len(self.dictionary_images)} dictionary images")

        except Exception as e:
            self._show_dictionary_error(f"Error loading dictionary images: {e}")

    def _populate_dictionary_dropdown(self):
        """Populate the dictionary dropdown with image names."""
        if not self.dictionary_combo:
            return

        self.dictionary_combo.clear()

        if not self.dictionary_images:
            self.dictionary_combo.addItem("No dictionary images found")
            self.dictionary_combo.setEnabled(False)
            return

        # Add items with display names
        for image_path in self.dictionary_images:
            path = Path(image_path)
            word = path.parent.name
            filename = path.name
            display_name = f"{word}/{filename}"
            self.dictionary_combo.addItem(display_name, image_path)

        self.dictionary_combo.setEnabled(True)

        # Auto-select first item
        if self.dictionary_images:
            self.dictionary_combo.setCurrentIndex(0)

    def _show_dictionary_error(self, message: str):
        """Show dictionary loading error."""
        print(f"❌ Dictionary Error: {message}")
        if self.dictionary_combo:
            self.dictionary_combo.clear()
            self.dictionary_combo.addItem(f"Error: {message}")
            self.dictionary_combo.setEnabled(False)

    def _on_dictionary_selection_changed(self, display_name: str):
        """Handle dictionary image selection change."""
        if (
            not display_name
            or display_name.startswith("Error:")
            or display_name.startswith("No dictionary")
        ):
            return

        # Get the actual file path from combo box data
        current_index = self.dictionary_combo.currentIndex()
        if current_index >= 0:
            image_path = self.dictionary_combo.itemData(current_index)
            if image_path:
                self._load_image_from_path(image_path)

    def _load_image_from_path(self, image_path: str):
        """Load an image from the given path."""
        try:
            self.current_image_path = image_path
            self.original_pixmap = QPixmap(image_path)

            if self.original_pixmap.isNull():
                self.statusBar().showMessage(f"❌ Failed to load image: {image_path}")
                return

            # Update UI
            path = Path(image_path)
            relative_path = f"{path.parent.name}/{path.name}"
            self.image_path_label.setText(f"📁 {relative_path}")
            self.image_path_label.setStyleSheet("color: green;")

            # Auto-run tests if enabled
            if self.auto_update_checkbox.isChecked():
                self._run_all_tests()

            self.statusBar().showMessage(
                f"✅ Loaded: {relative_path} ({self.original_pixmap.width()}x{self.original_pixmap.height()})"
            )

        except Exception as e:
            self.statusBar().showMessage(f"❌ Error loading image: {e}")
            print(f"Error loading image {image_path}: {e}")

    # UI event handlers
    def _load_image(self):
        """Load an image file for testing."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Test Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff *.webp)",
        )

        if file_path:
            self.current_image_path = file_path
            self.original_pixmap = QPixmap(file_path)

            if self.original_pixmap.isNull():
                self.statusBar().showMessage("❌ Failed to load image")
                return

            # Update UI
            filename = Path(file_path).name
            self.image_path_label.setText(f"📁 {filename}")
            self.image_path_label.setStyleSheet("color: green;")

            # Auto-run tests if enabled
            if self.auto_update_checkbox.isChecked():
                self._run_all_tests()

            self.statusBar().showMessage(
                f"✅ Loaded: {filename} ({self.original_pixmap.width()}x{self.original_pixmap.height()})"
            )

    def _load_sample_image(self):
        """Try to load a sample image - prioritize dictionary images."""
        # First try to load from dictionary if available
        if self.dictionary_images:
            # Load the first dictionary image
            first_image = self.dictionary_images[0]
            self._load_image_from_path(first_image)
            return

        # Fallback: Look for sample images in common locations
        sample_paths = [
            "resources/images/sample.png",
            "assets/sample.png",
            "test_images/sample.png",
            "../test_images/sample.png",
        ]

        for path in sample_paths:
            if os.path.exists(path):
                self.current_image_path = path
                self.original_pixmap = QPixmap(path)
                if not self.original_pixmap.isNull():
                    filename = Path(path).name
                    self.image_path_label.setText(f"📁 {filename} (sample)")
                    self.image_path_label.setStyleSheet("color: blue;")
                    self._run_all_tests()
                    return

        # If no images found, show instructions
        self.image_path_label.setText(
            "Select a dictionary image or click 'Load Other Image...' to start"
        )

    def _update_target_size(self):
        """Update target size from spinboxes."""
        self.target_size = QSize(
            self.width_spinbox.value(), self.height_spinbox.value()
        )

        if self.auto_update_checkbox.isChecked() and self.original_pixmap:
            self._run_all_tests()

    def _set_preset_size(self, width: int, height: int):
        """Set preset size."""
        self.width_spinbox.setValue(width)
        self.height_spinbox.setValue(height)
        self._update_target_size()

    def _run_all_tests(self):
        """Run all scaling method tests."""
        if not self.original_pixmap or self.original_pixmap.isNull():
            self.statusBar().showMessage("❌ No image loaded")
            return

        # Clear previous results
        for i in reversed(range(self.results_layout.count())):
            child = self.results_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        self.statusBar().showMessage("🔄 Running tests...")
        QApplication.processEvents()  # Update UI

        # Run each test
        results = []
        for i, method in enumerate(self.scaling_methods):
            try:
                # Run the scaling method
                result_pixmap = method.method_func(
                    self.original_pixmap, self.target_size
                )

                # Create result display
                result_widget = self._create_result_widget(method, result_pixmap, i)

                # Add to grid (3 columns)
                row = i // 3
                col = i % 3
                self.results_layout.addWidget(result_widget, row, col)

                results.append((method.name, "✅"))

            except Exception as e:
                # Create error display
                error_widget = self._create_error_widget(method, str(e))
                row = i // 3
                col = i % 3
                self.results_layout.addWidget(error_widget, row, col)

                results.append((method.name, f"❌ {str(e)[:30]}"))

        # Update status
        success_count = sum(1 for _, status in results if status == "✅")
        self.statusBar().showMessage(
            f"✅ Completed {success_count}/{len(self.scaling_methods)} tests"
        )

    def _create_result_widget(
        self, method: ImageScalingMethod, result_pixmap: QPixmap, index: int
    ) -> QFrame:
        """Create a widget to display test results."""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setMaximumWidth(280)

        layout = QVBoxLayout(frame)
        layout.setSpacing(5)

        # Method name and description
        name_label = QLabel(f"{index + 1}. {method.name}")
        name_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        layout.addWidget(name_label)

        desc_label = QLabel(method.description)
        desc_label.setStyleSheet("font-size: 10px; color: #7f8c8d; font-style: italic;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Image display
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("border: 1px solid #bdc3c7; background: white;")
        image_label.setMinimumHeight(self.target_size.height() + 20)

        if not result_pixmap.isNull():
            image_label.setPixmap(result_pixmap)

            # Size info
            size_info = QLabel(
                f"Size: {result_pixmap.width()}×{result_pixmap.height()}"
            )
            size_info.setStyleSheet("font-size: 9px; color: #95a5a6;")
            size_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(size_info)
        else:
            image_label.setText("❌ Failed")
            image_label.setStyleSheet(
                "border: 1px solid #e74c3c; background: #fdf2f2; color: #e74c3c;"
            )

        layout.addWidget(image_label)

        return frame

    def _create_error_widget(self, method: ImageScalingMethod, error: str) -> QFrame:
        """Create a widget to display errors."""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setMaximumWidth(280)
        frame.setStyleSheet("background: #fdf2f2; border: 1px solid #e74c3c;")

        layout = QVBoxLayout(frame)

        name_label = QLabel(method.name)
        name_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
        layout.addWidget(name_label)

        error_label = QLabel(f"❌ Error: {error}")
        error_label.setStyleSheet("color: #e74c3c; font-size: 10px;")
        error_label.setWordWrap(True)
        layout.addWidget(error_label)

        return frame


# Add missing import
from PyQt6.QtGui import QImage


def main():
    """Run the image quality test widget."""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("Image Quality Test")
    app.setApplicationVersion("1.0")

    # Create and show the test widget
    test_widget = ImageQualityTestWidget()
    test_widget.show()

    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
