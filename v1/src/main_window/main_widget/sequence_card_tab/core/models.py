from pathlib import Path
from typing import Dict, Optional, Any, List
from dataclasses import dataclass


@dataclass
class SequenceCardData:
    """Immutable data structure for sequence card information."""

    path: Path
    word: str
    length: int
    metadata: Dict[str, Any]
    thumbnail_path: Optional[Path] = None
    high_res_path: Optional[Path] = None


@dataclass
class ImageLoadRequest:
    """Data structure for image loading requests."""

    path: str
    word: str
    sequence_file: str
    metadata: Dict[str, Any]
    priority: int = 0
    callback: Optional[callable] = None


@dataclass
class SequenceCardBatch:
    """Data structure for batched sequence card processing."""

    sequences: List[Dict[str, Any]]
    batch_size: int
    start_index: int
    end_index: int
    total_count: int
