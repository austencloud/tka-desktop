"""
Qt Threading Integration for TKA Desktop

A+ Enhancement: Advanced Qt threading bridge with async/await support
for seamless integration of asynchronous operations with Qt widgets.

ARCHITECTURE: Provides threading bridge for Qt applications with async/await
support, thread-safe operations, and automatic resource management.
"""

import asyncio
import logging
import threading
import time
from typing import Dict, List, Optional, Any, Callable, TypeVar, Awaitable, Union
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, Future
import weakref

# Import Qt modules with compatibility
try:
    from PyQt6.QtCore import QObject, QThread, QTimer, pyqtSignal, QMutex, QMutexLocker
    from PyQt6.QtWidgets import QWidget, QApplication
except ImportError:
    try:
        from PyQt5.QtCore import (
            QObject,
            QThread,
            QTimer,
            pyqtSignal,
            QMutex,
            QMutexLocker,
        )
        from PyQt5.QtWidgets import QWidget, QApplication
    except ImportError:
        # Fallback for testing without Qt
        QObject = object
        QThread = object
        QTimer = object
        QMutex = object
        QMutexLocker = object
        QWidget = object
        QApplication = object

        def pyqtSignal(*args, **kwargs):
            return lambda: None


logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class ThreadingMetrics:
    """Metrics for Qt threading operations."""

    async_operations_started: int = 0
    async_operations_completed: int = 0
    async_operations_failed: int = 0
    thread_pool_tasks: int = 0
    qt_signal_emissions: int = 0
    average_operation_time_ms: float = 0.0


class QtAsyncBridge(QObject):
    """
    Qt async bridge for seamless async/await integration.

    A+ Enhancement: Provides async/await support for Qt applications
    with thread-safe operations and automatic resource management.
    """

    # Signals for async operation completion
    operation_completed = pyqtSignal(object, object)  # (result, operation_id)
    operation_failed = pyqtSignal(object, object)  # (error, operation_id)

    def __init__(self, max_workers: int = 4):
        """
        Initialize Qt async bridge.

        Args:
            max_workers: Maximum number of worker threads
        """
        super().__init__()

        self.max_workers = max_workers
        self._thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self._pending_operations: Dict[str, Future] = {}
        self._operation_callbacks: Dict[str, Callable] = {}
        self._metrics = ThreadingMetrics()
        self._mutex = QMutex() if QMutex != object else threading.Lock()

        # Connect signals
        if hasattr(self, "operation_completed"):
            self.operation_completed.connect(self._handle_operation_completed)
            self.operation_failed.connect(self._handle_operation_failed)

        logger.info(f"Qt async bridge initialized with {max_workers} workers")

    async def run_async_operation(self, operation: Callable[[], T]) -> T:
        """
        Run an operation asynchronously with Qt integration.

        Args:
            operation: Callable to execute asynchronously

        Returns:
            Result of the operation
        """
        import uuid

        operation_id = str(uuid.uuid4())

        # Create future for the operation
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        # Store callback for completion
        self._operation_callbacks[operation_id] = lambda result, error: (
            future.set_exception(error) if error else future.set_result(result)
        )

        # Submit to thread pool
        thread_future = self._thread_pool.submit(
            self._execute_operation, operation, operation_id
        )
        self._pending_operations[operation_id] = thread_future

        self._metrics.async_operations_started += 1

        try:
            # Wait for completion
            result = await future
            self._metrics.async_operations_completed += 1
            return result
        except Exception as e:
            self._metrics.async_operations_failed += 1
            raise e
        finally:
            # Cleanup
            self._cleanup_operation(operation_id)

    def _execute_operation(self, operation: Callable[[], T], operation_id: str) -> None:
        """Execute operation in thread pool."""
        try:
            result = operation()
            # Emit completion signal (thread-safe)
            if hasattr(self, "operation_completed"):
                self.operation_completed.emit(result, operation_id)
        except Exception as e:
            # Emit error signal (thread-safe)
            if hasattr(self, "operation_failed"):
                self.operation_failed.emit(e, operation_id)

    def _handle_operation_completed(self, result: Any, operation_id: str) -> None:
        """Handle operation completion."""
        if operation_id in self._operation_callbacks:
            callback = self._operation_callbacks[operation_id]
            callback(result, None)

    def _handle_operation_failed(self, error: Exception, operation_id: str) -> None:
        """Handle operation failure."""
        if operation_id in self._operation_callbacks:
            callback = self._operation_callbacks[operation_id]
            callback(None, error)

    def _cleanup_operation(self, operation_id: str) -> None:
        """Cleanup operation resources."""
        self._pending_operations.pop(operation_id, None)
        self._operation_callbacks.pop(operation_id, None)

    def run_in_qt_thread(self, operation: Callable[[], T]) -> T:
        """
        Run operation in Qt main thread (synchronous).

        Args:
            operation: Callable to execute in Qt thread

        Returns:
            Result of the operation
        """
        if QApplication != object:
            app = QApplication.instance()
            if app and threading.current_thread() != threading.main_thread():
                # Use QTimer to execute in main thread
                result_container = {"result": None, "error": None, "done": False}

                def execute():
                    try:
                        result_container["result"] = operation()
                    except Exception as e:
                        result_container["error"] = e
                    finally:
                        result_container["done"] = True

                # Schedule execution
                QTimer.singleShot(0, execute)

                # Wait for completion (simple polling)
                import time

                while not result_container["done"]:
                    time.sleep(0.001)
                    if QApplication.instance():
                        QApplication.instance().processEvents()

                if result_container["error"]:
                    raise result_container["error"]
                return result_container["result"]

        # Execute directly if in main thread or Qt not available
        return operation()

    def get_metrics(self) -> ThreadingMetrics:
        """Get threading operation metrics."""
        return ThreadingMetrics(
            async_operations_started=self._metrics.async_operations_started,
            async_operations_completed=self._metrics.async_operations_completed,
            async_operations_failed=self._metrics.async_operations_failed,
            thread_pool_tasks=len(self._pending_operations),
            qt_signal_emissions=self._metrics.qt_signal_emissions,
            average_operation_time_ms=self._metrics.average_operation_time_ms,
        )

    def shutdown(self) -> None:
        """Shutdown the async bridge and cleanup resources."""
        # Cancel pending operations
        for operation_id, future in self._pending_operations.items():
            future.cancel()

        # Shutdown thread pool
        self._thread_pool.shutdown(wait=True)

        # Clear callbacks
        self._operation_callbacks.clear()
        self._pending_operations.clear()

        logger.info("Qt async bridge shutdown completed")


class AsyncQtWidget(QWidget):
    """
    Qt widget with built-in async/await support.

    A+ Enhancement: Extends QWidget with async operation support
    and automatic resource management.
    """

    def __init__(self, parent: Optional[Any] = None):
        """Initialize async Qt widget."""
        super().__init__(parent)

        self._async_bridge = qt_async_bridge()
        self._async_operations: List[asyncio.Task] = []
        self._cleanup_handlers: List[Callable] = []

        logger.debug(f"AsyncQtWidget created: {self.__class__.__name__}")

    async def run_async(self, operation: Callable[[], T]) -> T:
        """
        Run async operation with automatic cleanup tracking.

        Args:
            operation: Async operation to execute

        Returns:
            Result of the operation
        """
        result = await self._async_bridge.run_async_operation(operation)
        return result

    def run_in_qt_thread(self, operation: Callable[[], T]) -> T:
        """
        Run operation in Qt main thread.

        Args:
            operation: Operation to execute in Qt thread

        Returns:
            Result of the operation
        """
        return self._async_bridge.run_in_qt_thread(operation)

    def schedule_async_task(self, coro: Awaitable[T]) -> asyncio.Task[T]:
        """
        Schedule async task with automatic tracking.

        Args:
            coro: Coroutine to schedule

        Returns:
            Async task
        """
        task = asyncio.create_task(coro)
        self._async_operations.append(task)

        # Add cleanup callback
        task.add_done_callback(
            lambda t: (
                self._async_operations.remove(t)
                if t in self._async_operations
                else None
            )
        )

        return task

    def add_cleanup_handler(self, handler: Callable) -> None:
        """Add cleanup handler for widget destruction."""
        self._cleanup_handlers.append(handler)

    def cleanup_async_operations(self) -> None:
        """Cleanup all async operations."""
        # Cancel pending tasks
        for task in self._async_operations:
            if not task.done():
                task.cancel()

        # Execute cleanup handlers
        for handler in self._cleanup_handlers:
            try:
                handler()
            except Exception as e:
                logger.error(f"Error in cleanup handler: {e}")

        # Clear lists
        self._async_operations.clear()
        self._cleanup_handlers.clear()

        logger.debug(f"AsyncQtWidget cleanup completed: {self.__class__.__name__}")

    def closeEvent(self, event) -> None:
        """Handle widget close event with async cleanup."""
        self.cleanup_async_operations()
        super().closeEvent(event)

    def __del__(self):
        """Destructor with async cleanup."""
        self.cleanup_async_operations()


class QtThreadManager:
    """
    Qt thread manager for advanced threading operations.

    A+ Enhancement: Provides advanced thread management with
    automatic resource cleanup and performance monitoring.
    """

    def __init__(self):
        """Initialize Qt thread manager."""
        self._active_threads: Dict[str, QThread] = {}
        self._thread_metrics: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

        logger.info("Qt thread manager initialized")

    def create_worker_thread(
        self, worker_class: type, thread_name: str, *args, **kwargs
    ) -> QThread:
        """
        Create and start a worker thread.

        Args:
            worker_class: Worker class to instantiate
            thread_name: Name for the thread
            *args: Worker constructor arguments
            **kwargs: Worker constructor keyword arguments

        Returns:
            QThread instance
        """
        if QThread == object:
            logger.warning("Qt not available, cannot create worker thread")
            return None

        with self._lock:
            # Create thread and worker
            thread = QThread()
            worker = worker_class(*args, **kwargs)

            # Move worker to thread
            worker.moveToThread(thread)

            # Connect signals for cleanup
            thread.finished.connect(lambda: self._cleanup_thread(thread_name))

            # Store thread
            self._active_threads[thread_name] = thread
            self._thread_metrics[thread_name] = {
                "created_at": time.time(),
                "worker_class": worker_class.__name__,
                "status": "created",
            }

            # Start thread
            thread.start()
            self._thread_metrics[thread_name]["status"] = "running"

            logger.info(f"Worker thread created: {thread_name}")
            return thread

    def stop_thread(self, thread_name: str, timeout_ms: int = 5000) -> bool:
        """
        Stop a worker thread gracefully.

        Args:
            thread_name: Name of thread to stop
            timeout_ms: Timeout in milliseconds

        Returns:
            True if thread stopped successfully
        """
        with self._lock:
            if thread_name not in self._active_threads:
                return False

            thread = self._active_threads[thread_name]

            # Request thread to quit
            thread.quit()

            # Wait for thread to finish
            if thread.wait(timeout_ms):
                self._cleanup_thread(thread_name)
                logger.info(f"Thread stopped gracefully: {thread_name}")
                return True
            else:
                # Force termination if timeout
                thread.terminate()
                thread.wait(1000)  # Wait 1 second for termination
                self._cleanup_thread(thread_name)
                logger.warning(f"Thread terminated forcefully: {thread_name}")
                return False

    def _cleanup_thread(self, thread_name: str) -> None:
        """Cleanup thread resources."""
        with self._lock:
            if thread_name in self._active_threads:
                del self._active_threads[thread_name]

            if thread_name in self._thread_metrics:
                self._thread_metrics[thread_name]["status"] = "finished"
                self._thread_metrics[thread_name]["finished_at"] = time.time()

    def get_thread_metrics(self) -> Dict[str, Any]:
        """Get thread management metrics."""
        with self._lock:
            return {
                "active_threads": len(self._active_threads),
                "thread_details": dict(self._thread_metrics),
                "total_threads_created": len(self._thread_metrics),
            }

    def shutdown_all_threads(self) -> None:
        """Shutdown all managed threads."""
        with self._lock:
            thread_names = list(self._active_threads.keys())

        for thread_name in thread_names:
            self.stop_thread(thread_name)

        logger.info("All threads shutdown completed")


# Global instances
_qt_async_bridge: Optional[QtAsyncBridge] = None
_qt_thread_manager: Optional[QtThreadManager] = None


def qt_async_bridge() -> QtAsyncBridge:
    """Get global Qt async bridge instance."""
    global _qt_async_bridge
    if _qt_async_bridge is None:
        _qt_async_bridge = QtAsyncBridge()
    return _qt_async_bridge


def qt_thread_manager() -> QtThreadManager:
    """Get global Qt thread manager instance."""
    global _qt_thread_manager
    if _qt_thread_manager is None:
        _qt_thread_manager = QtThreadManager()
    return _qt_thread_manager
