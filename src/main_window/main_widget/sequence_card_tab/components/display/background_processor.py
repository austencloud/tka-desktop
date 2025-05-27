# src/main_window/main_widget/sequence_card_tab/components/display/background_processor.py
import logging
import time
from typing import List, Dict, Any, Callable, Optional
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication


class BackgroundImageProcessor(QObject):
    """
    Background image processing system using QTimer for non-blocking operations.
    
    Features:
    - Processes images in small batches to keep UI responsive
    - Configurable batch sizes and processing intervals
    - Priority-based processing queue
    - Automatic pause/resume based on user activity
    - Progress tracking and statistics
    """
    
    # Signals
    batch_completed = pyqtSignal(int)  # number of images processed
    processing_completed = pyqtSignal()
    progress_updated = pyqtSignal(int, int)  # current, total
    
    def __init__(self, image_processor, batch_size: int = 3, interval_ms: int = 50):
        """
        Initialize the background processor.
        
        Args:
            image_processor: ImageProcessor instance
            batch_size: Number of images to process per batch
            interval_ms: Milliseconds between batches
        """
        super().__init__()
        
        self.image_processor = image_processor
        self.batch_size = batch_size
        self.interval_ms = interval_ms
        
        # Processing queue with priority support
        self.processing_queue: List[Dict[str, Any]] = []
        self.current_batch: List[Dict[str, Any]] = []
        
        # Timer for background processing
        self.process_timer = QTimer()
        self.process_timer.timeout.connect(self._process_batch)
        
        # User activity detection
        self.activity_timer = QTimer()
        self.activity_timer.timeout.connect(self._resume_processing)
        self.activity_pause_ms = 1000  # Pause processing for 1s after user activity
        self.is_paused = False
        
        # Statistics
        self.total_processed = 0
        self.total_queued = 0
        self.processing_start_time = 0
        self.batches_processed = 0
        
        # Performance monitoring
        self.max_batch_time_ms = 0
        self.avg_batch_time_ms = 0
        self.batch_times: List[float] = []
        
        logging.info("Background image processor initialized")
    
    def queue_image_processing(self, image_path: str, callback: Callable, priority: int = 5, **kwargs) -> None:
        """
        Queue an image for background processing.
        
        Args:
            image_path: Path to the image to process
            callback: Function to call when processing is complete
            priority: Processing priority (1=highest, 10=lowest)
            **kwargs: Additional parameters for image processing
        """
        task = {
            'image_path': image_path,
            'callback': callback,
            'priority': priority,
            'params': kwargs,
            'queued_time': time.time()
        }
        
        # Insert based on priority (lower number = higher priority)
        inserted = False
        for i, existing_task in enumerate(self.processing_queue):
            if priority < existing_task['priority']:
                self.processing_queue.insert(i, task)
                inserted = True
                break
        
        if not inserted:
            self.processing_queue.append(task)
        
        self.total_queued += 1
        
        # Start processing if not already running
        if not self.process_timer.isActive() and not self.is_paused:
            self._start_processing()
    
    def _start_processing(self) -> None:
        """Start background processing."""
        if self.processing_queue and not self.process_timer.isActive():
            self.processing_start_time = time.time()
            self.process_timer.start(self.interval_ms)
            logging.debug(f"Started background processing: {len(self.processing_queue)} items queued")
    
    def _process_batch(self) -> None:
        """Process a batch of images."""
        if self.is_paused or not self.processing_queue:
            self._stop_processing()
            return
        
        batch_start_time = time.time()
        
        try:
            # Prepare batch
            batch_size = min(self.batch_size, len(self.processing_queue))
            self.current_batch = self.processing_queue[:batch_size]
            self.processing_queue = self.processing_queue[batch_size:]
            
            # Process each item in the batch
            processed_count = 0
            for task in self.current_batch:
                try:
                    self._process_single_task(task)
                    processed_count += 1
                    self.total_processed += 1
                    
                except Exception as e:
                    logging.warning(f"Error processing task {task['image_path']}: {e}")
            
            # Update statistics
            batch_time = (time.time() - batch_start_time) * 1000  # Convert to ms
            self.batch_times.append(batch_time)
            self.max_batch_time_ms = max(self.max_batch_time_ms, batch_time)
            
            # Keep only recent batch times for average calculation
            if len(self.batch_times) > 20:
                self.batch_times = self.batch_times[-20:]
            
            self.avg_batch_time_ms = sum(self.batch_times) / len(self.batch_times)
            self.batches_processed += 1
            
            # Emit progress signals
            self.batch_completed.emit(processed_count)
            remaining = len(self.processing_queue)
            total = self.total_processed + remaining
            self.progress_updated.emit(self.total_processed, total)
            
            # Check if processing is complete
            if not self.processing_queue:
                self._stop_processing()
                self.processing_completed.emit()
            
            # Adjust interval based on performance
            self._adjust_processing_interval(batch_time)
            
        except Exception as e:
            logging.error(f"Error in batch processing: {e}")
            self._stop_processing()
    
    def _process_single_task(self, task: Dict[str, Any]) -> None:
        """Process a single image task."""
        image_path = task['image_path']
        callback = task['callback']
        params = task['params']
        
        # Load the image using the image processor
        pixmap = self.image_processor.load_image_with_consistent_scaling(
            image_path, **params
        )
        
        # Call the callback with the result
        if callback and pixmap and not pixmap.isNull():
            callback(image_path, pixmap)
    
    def _adjust_processing_interval(self, batch_time_ms: float) -> None:
        """Adjust processing interval based on performance."""
        # If batch takes too long, increase interval to keep UI responsive
        if batch_time_ms > 100:  # If batch takes more than 100ms
            new_interval = min(self.interval_ms + 10, 200)  # Max 200ms interval
            if new_interval != self.interval_ms:
                self.interval_ms = new_interval
                self.process_timer.setInterval(self.interval_ms)
                logging.debug(f"Increased processing interval to {self.interval_ms}ms")
        
        # If batch is fast, decrease interval for better throughput
        elif batch_time_ms < 20 and self.interval_ms > 30:  # If batch is very fast
            new_interval = max(self.interval_ms - 5, 30)  # Min 30ms interval
            if new_interval != self.interval_ms:
                self.interval_ms = new_interval
                self.process_timer.setInterval(self.interval_ms)
                logging.debug(f"Decreased processing interval to {self.interval_ms}ms")
    
    def _stop_processing(self) -> None:
        """Stop background processing."""
        if self.process_timer.isActive():
            self.process_timer.stop()
            
            if self.processing_start_time > 0:
                total_time = time.time() - self.processing_start_time
                logging.debug(f"Background processing completed: {self.total_processed} images in {total_time:.2f}s")
    
    def pause_processing(self) -> None:
        """Pause processing (e.g., during user interaction)."""
        if not self.is_paused:
            self.is_paused = True
            if self.process_timer.isActive():
                self.process_timer.stop()
            
            # Start activity timer to resume processing after user activity stops
            self.activity_timer.start(self.activity_pause_ms)
            logging.debug("Background processing paused for user activity")
    
    def _resume_processing(self) -> None:
        """Resume processing after user activity stops."""
        if self.is_paused:
            self.is_paused = False
            self.activity_timer.stop()
            
            if self.processing_queue:
                self._start_processing()
                logging.debug("Background processing resumed")
    
    def force_complete(self) -> None:
        """Force complete all remaining processing (blocking)."""
        if self.process_timer.isActive():
            self.process_timer.stop()
        
        while self.processing_queue:
            # Process larger batches when forcing completion
            batch_size = min(10, len(self.processing_queue))
            batch = self.processing_queue[:batch_size]
            self.processing_queue = self.processing_queue[batch_size:]
            
            for task in batch:
                try:
                    self._process_single_task(task)
                    self.total_processed += 1
                except Exception as e:
                    logging.warning(f"Error in force processing: {e}")
            
            # Keep UI responsive during force processing
            QApplication.processEvents()
        
        self.processing_completed.emit()
        logging.info("Force completed all background processing")
    
    def clear_queue(self) -> None:
        """Clear all pending processing tasks."""
        cleared_count = len(self.processing_queue)
        self.processing_queue.clear()
        self.current_batch.clear()
        
        if self.process_timer.isActive():
            self.process_timer.stop()
        
        if cleared_count > 0:
            logging.info(f"Cleared {cleared_count} pending processing tasks")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get background processing statistics."""
        queue_size = len(self.processing_queue)
        is_active = self.process_timer.isActive()
        
        return {
            'queue_size': queue_size,
            'total_processed': self.total_processed,
            'total_queued': self.total_queued,
            'batches_processed': self.batches_processed,
            'is_active': is_active,
            'is_paused': self.is_paused,
            'batch_size': self.batch_size,
            'interval_ms': self.interval_ms,
            'max_batch_time_ms': round(self.max_batch_time_ms, 2),
            'avg_batch_time_ms': round(self.avg_batch_time_ms, 2)
        }
    
    def log_stats(self) -> None:
        """Log current processing statistics."""
        stats = self.get_stats()
        logging.info(f"Background Processor: Queue: {stats['queue_size']}, "
                    f"Processed: {stats['total_processed']}, "
                    f"Avg Batch Time: {stats['avg_batch_time_ms']}ms, "
                    f"Active: {stats['is_active']}")
