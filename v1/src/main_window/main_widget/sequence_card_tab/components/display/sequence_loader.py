# src/main_window/main_widget/sequence_card_tab/components/display/sequence_loader.py
import os
from typing import Dict, List, Any
from main_window.main_widget.metadata_extractor import MetaDataExtractor


class SequenceLoader:
    """
    Responsible for loading and filtering sequence card images.
    
    This class:
    1. Loads sequence card images from the file system
    2. Extracts metadata from images
    3. Filters sequences based on length
    4. Provides a consistent interface for accessing sequence data
    """
    
    def __init__(self):
        self.metadata_extractor = MetaDataExtractor()
        
    def get_all_sequences(self, images_path: str) -> List[Dict[str, Any]]:
        """
        Get all sequences from the sequence_card_images directory.
        
        Args:
            images_path: Path to the sequence card images directory
            
        Returns:
            List[Dict[str, Any]]: List of sequence data dictionaries
        """
        sequences = []

        # Validate the images path
        if not os.path.exists(images_path):
            print(
                f"Warning: Sequence card images directory does not exist: {images_path}"
            )
            return sequences

        # Process each word folder
        for word in os.listdir(images_path):
            word_path = os.path.join(images_path, word)

            # Skip non-directories and special directories
            if not os.path.isdir(word_path) or word.startswith("__"):
                continue

            # Process each image file
            for file in os.listdir(word_path):
                if file.endswith(".png") and not file.startswith("__"):
                    file_path = os.path.join(word_path, file)

                    # Extract sequence length using the metadata extractor
                    try:
                        # Get the sequence length from the metadata
                        sequence_length = self.metadata_extractor.get_length(file_path)

                        # If we couldn't get the length from metadata, default to 0
                        if sequence_length is None:
                            sequence_length = 0

                    except Exception as e:
                        print(f"Error extracting metadata from {file_path}: {e}")
                        sequence_length = 0

                    sequences.append(
                        {
                            "path": file_path,
                            "word": word,
                            "metadata": {
                                "sequence_length": sequence_length,
                                "sequence": word,
                            },
                        }
                    )

        return sequences
        
    def filter_sequences_by_length(
        self, sequences: List[Dict[str, Any]], length: int
    ) -> List[Dict[str, Any]]:
        """
        Filter sequences by the specified length.
        
        Args:
            sequences: List of sequence data dictionaries
            length: Length to filter by (0 for all)
            
        Returns:
            List[Dict[str, Any]]: Filtered list of sequence data dictionaries
        """
        if length == 0:
            return sequences

        filtered_sequences = []

        for sequence in sequences:
            metadata = sequence.get("metadata", {})
            sequence_length = metadata.get("sequence_length", 0)

            if sequence_length == length:
                filtered_sequences.append(sequence)

        return filtered_sequences
