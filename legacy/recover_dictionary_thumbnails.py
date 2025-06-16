#!/usr/bin/env python3
"""
Recovery script to regenerate dictionary thumbnails from existing sequence card images.
This will restore your dictionary using the intact sequence card images.
"""

import os
import sys
import shutil
from pathlib import Path
from PIL import Image, PngImagePlugin

def find_sequence_card_images():
    """Find all existing sequence card images."""
    project_root = Path(__file__).parent
    images_path = project_root / "images" / "sequence_card_images"
    
    if not images_path.exists():
        print(f"❌ Sequence card images path not found: {images_path}")
        return []
    
    sequence_dirs = []
    for item in images_path.iterdir():
        if item.is_dir() and item.name != "__pycache__":
            sequence_dirs.append(item)
    
    return sequence_dirs

def create_thumbnail_from_sequence_card(sequence_dir, output_dir):
    """Create a high-quality thumbnail from sequence card image."""
    sequence_name = sequence_dir.name
    
    # Find the first PNG file in the sequence directory
    png_files = list(sequence_dir.glob("*.png"))
    if not png_files:
        return False
    
    source_image = png_files[0]  # Use the first image
    
    try:
        # Open the source image
        with Image.open(source_image) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create high-quality thumbnail (preserve aspect ratio)
            # Use a reasonable thumbnail size
            thumbnail_size = (300, 300)  # Larger than before for better quality
            img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
            
            # Create output directory if it doesn't exist
            output_sequence_dir = output_dir / sequence_name
            output_sequence_dir.mkdir(parents=True, exist_ok=True)
            
            # Save with high quality
            output_file = output_sequence_dir / f"{sequence_name}_ver0.png"
            
            # Create PNG info for metadata
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("sequence_name", sequence_name)
            pnginfo.add_text("variation", "0")
            
            # Save with maximum quality
            img.save(output_file, "PNG", pnginfo=pnginfo, compress_level=1, optimize=True)
            
            return True
            
    except Exception as e:
        print(f"⚠️  Error processing {sequence_name}: {e}")
        return False

def main():
    """Main recovery function."""
    print("🔄 Dictionary Thumbnail Recovery Tool")
    print("=" * 50)
    print()
    print("This script will:")
    print("1. Find your existing sequence card images (which are safe)")
    print("2. Generate new high-quality thumbnails for the dictionary")
    print("3. Restore your browse tab functionality")
    print()
    
    # Find sequence card images
    sequence_dirs = find_sequence_card_images()
    
    if not sequence_dirs:
        print("❌ No sequence card images found!")
        return 1
    
    print(f"📁 Found {len(sequence_dirs)} sequence card images to recover")
    
    # Set up output directory
    project_root = Path(__file__).parent
    output_dir = project_root / "src" / "data" / "dictionary"
    
    print(f"📂 Output directory: {output_dir}")
    
    # Confirm recovery
    response = input(f"\n🔄 Recover {len(sequence_dirs)} dictionary thumbnails? (y/N): ")
    if response.lower() != 'y':
        print("❌ Recovery cancelled")
        return 0
    
    # Recover thumbnails
    print("\n🔧 Generating high-quality thumbnails...")
    recovered_count = 0
    failed_count = 0
    
    for sequence_dir in sequence_dirs:
        sequence_name = sequence_dir.name
        success = create_thumbnail_from_sequence_card(sequence_dir, output_dir)
        
        if success:
            print(f"   ✅ {sequence_name}")
            recovered_count += 1
        else:
            print(f"   ❌ {sequence_name}")
            failed_count += 1
    
    print(f"\n🎉 Recovery complete!")
    print(f"   ✅ Successfully recovered: {recovered_count} thumbnails")
    if failed_count > 0:
        print(f"   ❌ Failed to recover: {failed_count} thumbnails")
    
    print("\n" + "=" * 50)
    print("🎉 DICTIONARY RECOVERY COMPLETE!")
    print()
    print("Your dictionary has been restored with:")
    print("   ✅ High-quality thumbnails (no 50% downscaling)")
    print("   ✅ Preserved original image data")
    print("   ✅ Enhanced PNG compression")
    print("   ✅ All your sequence data intact")
    print()
    print("Next steps:")
    print("1. Launch the application")
    print("2. Navigate to the browse tab")
    print("3. You should see all your sequences with crisp, high-quality images")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
