from typing import TYPE_CHECKING, List, Optional, Callable
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject

from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from .clickable_pictograph_frame import ClickablePictographFrame

if TYPE_CHECKING:
    from application.services.data.pictograph_dataset_service import (
        PictographDatasetService,
    )


class PictographPoolManager(QObject):
    """Manages Legacy-style object pooling for pictograph frames to prevent Qt deletion cascade"""

    MAX_PICTOGRAPHS = 36  # Same as Legacy's OptionFactory.MAX_PICTOGRAPHS

    def __init__(self, parent_widget: QWidget):
        super().__init__()
        self.parent_widget = parent_widget
        self._pictograph_pool: List[ClickablePictographFrame] = []
        self._pool_initialized = False
        self._click_handler: Optional[Callable] = None
        self._beat_data_click_handler: Optional[Callable] = None

    def set_click_handler(self, handler: Callable[[str], None]) -> None:
        """Set the click handler for all pool objects"""
        self._click_handler = handler

    def set_beat_data_click_handler(self, beat_data_handler: Callable) -> None:
        """Set the beat data click handler for all pool objects"""
        self._beat_data_click_handler = beat_data_handler

    def initialize_pool(self, progress_callback: Optional[Callable] = None) -> None:
        """Initialize Legacy-style object pool with progress updates"""
        if self._pool_initialized:
            return

        if progress_callback:
            progress_callback("Starting pictograph pool initialization", 0.3)

        try:
            if progress_callback:
                progress_callback("Loading pictograph dataset service", 0.4)

            from application.services.data.pictograph_dataset_service import (
                PictographDatasetService,
            )

            dataset_service = PictographDatasetService()

            if progress_callback:
                progress_callback("Preparing start position data", 0.5)

            start_positions = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
            pool_progress_start = 0.5
            pool_progress_range = 0.3

            for i in range(self.MAX_PICTOGRAPHS):
                try:
                    if i % 6 == 0 and progress_callback:
                        progress = (
                            pool_progress_start
                            + (i / self.MAX_PICTOGRAPHS) * pool_progress_range
                        )
                        progress_callback(
                            f"Creating pool object {i+1}/{self.MAX_PICTOGRAPHS}",
                            progress,
                        )

                    position_key = start_positions[i % len(start_positions)]
                    real_beat_data = dataset_service.get_start_position_pictograph(
                        position_key, "diamond"
                    )

                    if real_beat_data is None:
                        real_beat_data = self._get_fallback_beat_data(dataset_service)

                    if real_beat_data is None:
                        real_beat_data = self._create_minimal_beat_data()

                    frame = ClickablePictographFrame(
                        real_beat_data, parent=self.parent_widget
                    )
                    if self._click_handler:
                        frame.clicked.connect(self._click_handler)
                    if self._beat_data_click_handler:
                        frame.beat_data_clicked.connect(self._beat_data_click_handler)
                    frame.setVisible(False)
                    frame.set_container_widget(self.parent_widget)

                    self._pictograph_pool.append(frame)

                except Exception as e:
                    print(f"❌ Failed to create pool object {i}: {e}")
                    break

        except Exception as e:
            print(f"❌ Failed to initialize dataset service: {e}")
            self._create_fallback_pool(progress_callback)

        self._pool_initialized = True

        if progress_callback:
            progress_callback("Pictograph pool initialization complete", 0.8)

        print(
            f"✅ Pictograph pool initialized with {len(self._pictograph_pool)} objects"
        )

    def _get_fallback_beat_data(
        self, dataset_service: "PictographDatasetService"
    ) -> Optional[BeatData]:
        """Get fallback beat data from dataset"""
        if (
            hasattr(dataset_service, "_diamond_dataset")
            and dataset_service._diamond_dataset is not None
        ):
            if not dataset_service._diamond_dataset.empty:
                first_entry = dataset_service._diamond_dataset.iloc[0]
                return dataset_service._dataset_entry_to_beat_data(first_entry)
        return None

    def _create_minimal_beat_data(self) -> BeatData:
        """Create minimal valid beat data as final fallback"""
        return BeatData(
            letter="A",
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=1.0,
                start_ori="in",
                end_ori="out",
            ),
            red_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.NORTH,
                turns=1.0,
                start_ori="in",
                end_ori="out",
            ),
        )

    def _create_fallback_pool(
        self, progress_callback: Optional[Callable] = None
    ) -> None:
        """Create fallback pool with minimal beat data"""
        if progress_callback:
            progress_callback("Dataset failed, using fallback pool", 0.7)

        for i in range(self.MAX_PICTOGRAPHS):
            try:
                dummy_beat = self._create_minimal_beat_data()
                frame = ClickablePictographFrame(dummy_beat, parent=self.parent_widget)
                if self._click_handler:
                    frame.clicked.connect(self._click_handler)
                if self._beat_data_click_handler:
                    frame.beat_data_clicked.connect(self._beat_data_click_handler)
                frame.setVisible(False)
                frame.set_container_widget(self.parent_widget)
                self._pictograph_pool.append(frame)
            except Exception as e:
                print(f"❌ Failed to create fallback pool object {i}: {e}")
                break

    def get_pool_frame(self, index: int) -> Optional[ClickablePictographFrame]:
        """Get frame from pool at specified index"""
        if 0 <= index < len(self._pictograph_pool):
            return self._pictograph_pool[index]
        return None

    def get_pool_size(self) -> int:
        """Get current pool size"""
        return len(self._pictograph_pool)

    def resize_all_frames(self) -> None:
        """Resize all frames using Legacy's algorithm"""
        for frame in self._pictograph_pool:
            if frame and hasattr(frame, "resize_frame"):
                try:
                    frame.resize_frame()
                except RuntimeError:
                    pass
