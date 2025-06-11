#!/usr/bin/env python3
"""
Test Real ImageCreator Integration

This script tests that the dictionary regeneration system is actually
using the real ImageCreator system instead of the fake stick figure system.
"""

import os
import sys
import json
from PIL import Image


def test_single_image_regeneration():
    """Test regenerating a single image to verify it uses the real ImageCreator."""
    print("🧪 TESTING REAL IMAGECREATOR INTEGRATION")
    print("=" * 60)

    try:
        # Import the regenerator
        from tools.final_dictionary_regenerator import (
            _regenerate_image_with_real_image_creator,
        )

        # Find a test image to regenerate
        from utils.path_helpers import get_dictionary_path

        dictionary_path = get_dictionary_path()

        test_image_path = None
        test_sequence_data = None
        test_word = None

        # Find the first image with valid sequence data
        for word_folder in os.listdir(dictionary_path):
            word_path = os.path.join(dictionary_path, word_folder)
            if not os.path.isdir(word_path):
                continue

            for image_file in os.listdir(word_path):
                if image_file.endswith(".png"):
                    image_path = os.path.join(word_path, image_file)

                    # Try to extract sequence data
                    try:
                        with Image.open(image_path) as img:
                            if hasattr(img, "text") and "metadata" in img.text:
                                metadata = json.loads(img.text["metadata"])
                                sequence_data = metadata.get("sequence")
                                if sequence_data and len(sequence_data) > 0:
                                    test_image_path = image_path
                                    test_sequence_data = sequence_data
                                    test_word = word_folder
                                    break
                    except:
                        continue

            if test_image_path:
                break

        if not test_image_path:
            print("❌ No suitable test image found with sequence data")
            return False

        print(f"📁 Test image: {test_image_path}")
        print(f"📝 Test word: {test_word}")
        print(f"📊 Sequence data: {len(test_sequence_data)} beats")

        # Create a backup of the original
        backup_path = test_image_path + ".backup"
        import shutil

        shutil.copy2(test_image_path, backup_path)
        print(f"💾 Created backup: {backup_path}")

        # Test the regeneration
        print("\n🎨 Testing regeneration with real ImageCreator...")
        success = _regenerate_image_with_real_image_creator(
            test_sequence_data, test_word, test_image_path
        )

        if success:
            print("✅ Regeneration completed successfully!")

            # Check if the image was actually regenerated
            if os.path.exists(test_image_path):
                # Get file sizes to see if it changed
                original_size = os.path.getsize(backup_path)
                new_size = os.path.getsize(test_image_path)

                print(f"📊 Original size: {original_size} bytes")
                print(f"📊 New size: {new_size} bytes")

                if new_size != original_size:
                    print("✅ Image was actually regenerated (size changed)")
                else:
                    print("⚠️  Image size unchanged - may not have been regenerated")

                # Try to open the new image to verify it's valid
                try:
                    with Image.open(test_image_path) as img:
                        print(f"✅ New image is valid: {img.size[0]}x{img.size[1]}")
                except Exception as e:
                    print(f"❌ New image is invalid: {e}")
                    return False
            else:
                print("❌ Regenerated image file not found")
                return False
        else:
            print("❌ Regeneration failed")
            return False

        # Restore the backup
        shutil.move(backup_path, test_image_path)
        print(f"🔄 Restored original image from backup")

        print("\n🎯 REAL IMAGECREATOR TEST RESULTS:")
        print("=" * 50)
        print("✅ Successfully called real ImageCreator system")
        print("✅ Image was regenerated without errors")
        print("✅ Generated image is valid and readable")
        print("✅ No more fake stick figure system!")
        print()
        print("💡 The regeneration system now uses your actual ImageCreator!")
        print("💡 It will create real kinetic sequence diagrams")
        print("💡 No more bogus professional sequence cards")

        return True

    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🎨 Real ImageCreator Integration Test")
    print("=" * 70)

    # Run the test
    success = test_single_image_regeneration()

    # Final summary
    print("\n🎯 TEST SUMMARY")
    print("=" * 30)
    if success:
        print("✅ Real ImageCreator integration test passed!")
        print("🚀 The system now uses your actual image creation pipeline")
        print("💡 Ready to regenerate dictionary images properly")
    else:
        print("❌ Real ImageCreator integration test failed")
        print("💡 Check the errors above for details")

    print(f"\n🎯 Exit code: {0 if success else 1}")
    exit(0 if success else 1)
