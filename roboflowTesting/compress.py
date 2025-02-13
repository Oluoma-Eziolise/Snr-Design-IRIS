import os
import shutil
from PIL import Image
import zipfile

# Configuration
source_folder = "./dirs/images/output"  # Folder you want to copy and compress
destination_parent = "./dirs/images"  # Where the compressed folder will be placed
compressed_folder = "./dirs/images/compressed_images"  # This folder will hold compressed files
compression_quality = 70  # Adjust quality (1-100), lower means smaller file size

# Supported image formats
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".webp")

# ZIP Configuration
zip_destination_parent = "zipped_data"  # Folder where copied and zipped folder will be placed
zip_filename = "compressedImages.zip"  # Name of the final ZIP file


def compress_image(image_path):
    """Compress an image in place by reducing its quality."""
    try:
        with Image.open(image_path) as img:
            if img.mode in ("RGBA", "P"):  # Convert PNG to avoid transparency issues
                img = img.convert("RGB")
            
            img.save(image_path, optimize=True, quality=compression_quality)
            print(f"Compressed: {image_path}")
    except Exception as e:
        print(f"Error compressing {image_path}: {e}")

def copy_and_compress_folder(source_folder, compressed_folder):
    """Copy a folder and compress all images inside it."""
    # Ensure we don't delete the source folder
    if os.path.exists(compressed_folder):
        shutil.rmtree(compressed_folder)  # Remove only the compressed folder
    
    shutil.copytree(source_folder, compressed_folder)  # Copy files
    print(f"Folder copied: {source_folder} -> {compressed_folder}")

    for root, _, files in os.walk(compressed_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.lower().endswith(SUPPORTED_FORMATS):
                compress_image(file_path)

    print("Compression complete!")

if __name__ == "__main__":
    copy_and_compress_folder(source_folder, compressed_folder)

    print("Process complete!")
