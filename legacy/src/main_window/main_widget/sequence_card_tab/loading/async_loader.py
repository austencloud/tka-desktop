# src/main_window/main_widget/sequence_card_tab/loading/async_loader.py
import os
import queue
import threading
from typing import Dict, List, Optional
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap

from ..core.models import ImageLoadRequest


class AsyncImageLoader(QObject):
    """
    Asynchronous image loader for sequence card images.

    This class provides:
    1. Background loading of images to avoid UI freezing
    2. Priority-based loading queue
    3. Callback mechanism for loaded images
    4. Memory-efficient image processing
    """

    # Signal emitted when an image is loaded
    image_loaded = pyqtSignal(str, QPixmap)

    # Signal emitted when all images in the queue are loaded
    all_images_loaded = pyqtSignal()

    # Signal emitted when an error occurs
    error_occurred = pyqtSignal(str, str)  # path, error message

    def __init__(self, max_threads: int = 2):
        """
        Initialize the async image loader.

        Args:
            max_threads: Maximum number of worker threads (default: 2)
        """
        super().__init__()

        # Queue for image loading requests
        self.queue = queue.PriorityQueue()

        # Flag to indicate if the loader is running
        self.running = False

        # Flag to indicate if the loader should stop
        self.stop_requested = False

        # Worker threads
        self.threads: List[threading.Thread] = []
        self.max_threads = max_threads

        # Cache of loaded images
        self.cache: Dict[str, QPixmap] = {}

        # Lock for thread safety
        self.lock = threading.Lock()

    def start(self):
        """Start the image loader."""
        if self.running:
            return

        self.running = True
        self.stop_requested = False

        # Create and start worker threads
        for _ in range(self.max_threads):
            thread = threading.Thread(target=self._worker, daemon=True)
            thread.start()
            self.threads.append(thread)

    def stop(self):
        """Stop the image loader."""
        self.stop_requested = True

        # Clear the queue
        with self.lock:
            while not self.queue.empty():
                try:
                    self.queue.get_nowait()
                    self.queue.task_done()
                except queue.Empty:
                    break

        # Wait for threads to finish
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=1.0)

        self.threads.clear()
        self.running = False

    def queue_image(self, request: ImageLoadRequest):
        """
        Queue an image for loading.

        Args:
            request: Image load request
        """
        # Start the loader if not running
        if not self.running:
            self.start()

        # Add to queue
        self.queue.put((request.priority, request))

    def queue_images(self, requests: List[ImageLoadRequest]):
        """
        Queue multiple images for loading.

        Args:
            requests: List of image load requests
        """
        # Start the loader if not running
        if not self.running:
            self.start()

        # Add all requests to queue
        for request in requests:
            self.queue.put((request.priority, request))

    def clear_queue(self):
        """Clear the image loading queue."""
        with self.lock:
            while not self.queue.empty():
                try:
                    self.queue.get_nowait()
                    self.queue.task_done()
                except queue.Empty:
                    break

    def clear_cache(self):
        """Clear the image cache."""
        with self.lock:
            self.cache.clear()

    def get_cached_image(self, path: str) -> Optional[QPixmap]:
        """
        Get an image from the cache.

        Args:
            path: Path to the image

        Returns:
            QPixmap or None if not in cache
        """
        with self.lock:
            return self.cache.get(path)

    def _worker(self):
        """Worker thread function."""
        while not self.stop_requested:
            try:
                # Get a request from the queue
                _, request = self.queue.get(timeout=0.5)

                # Check if we should stop
                if self.stop_requested:
                    self.queue.task_done()
                    break

                # Process the request
                self._process_request(request)

                # Mark the task as done
                self.queue.task_done()

            except queue.Empty:
                # No more requests, check if we should emit all_images_loaded
                if self.queue.empty():
                    self.all_images_loaded.emit()
                continue
            except Exception as e:
                print(f"Error in AsyncImageLoader worker: {e}")
                continue

    def _process_request(self, request: ImageLoadRequest):
        """
        Process an image load request.

        Args:
            request: Image load request
        """
        try:
            # Check if the file exists
            if not os.path.exists(request.path):
                self.error_occurred.emit(request.path, "File not found")
                return

            # Check if already in cache
            cached_image = self.get_cached_image(request.path)
            if cached_image is not None:
                # Emit the signal
                self.image_loaded.emit(request.path, cached_image)

                # Call the callback if provided
                if request.callback:
                    request.callback(request.path, cached_image)

                return

            # Load the image
            image = QImage(request.path)
            if image.isNull():
                self.error_occurred.emit(request.path, "Failed to load image")
                return

            # Convert to pixmap
            pixmap = QPixmap.fromImage(image)

            # Add to cache
            with self.lock:
                self.cache[request.path] = pixmap

            # Emit the signal
            self.image_loaded.emit(request.path, pixmap)

            # Call the callback if provided
            if request.callback:
                request.callback(request.path, pixmap)

        except Exception as e:
            self.error_occurred.emit(request.path, str(e))

    def __del__(self):
        """Destructor."""
        self.stop()
