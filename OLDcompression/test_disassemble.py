import os
import numpy as np
from PIL import Image
import hashlib

def calculate_md5(data):
    """Calculate the MD5 checksum of given data."""
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    return md5_hash.hexdigest()

def image_to_bits(image_array):
    """Convert image numpy array to a string of bits."""
    flat_array = image_array.flatten()
    bit_string = ''.join(format(byte, '08b') for byte in flat_array)
    return bit_string

def disassemble_images(input_folder, output_dir):
    """Disassemble all images in a folder into bit strings and metadata."""
    # Get all image file paths from the input folder
    image_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

    if not image_files:
        print("No image files found in the input folder.")
        return

    for index, image_path in enumerate(image_files, start=1):
        try:
            # Load the image using Pillow
            img = Image.open(image_path)
        except Exception as e:
            print(f"Error opening image {image_path}: {e}")
            continue

        # Convert to numpy array and calculate MD5 checksum on pixel data
        img_array = np.array(img, dtype=np.uint8)
        img_bytes = img_array.tobytes()
        pixel_md5_checksum = calculate_md5(img_bytes)
        print(f"Image {index}: MD5 checksum of original pixel data: {pixel_md5_checksum}")

        # Save the MD5 checksum, image shape, and bit string representation
        bit_string = image_to_bits(img_array)
        with open(os.path.join(output_dir, f'image_bits_{index}.txt'), 'w') as f:
            f.write(bit_string)

        img_height, img_width, num_channels = img_array.shape
        with open(os.path.join(output_dir, f'image_shape_{index}.txt'), 'w') as f:
            f.write(f"{img_height},{img_width},{num_channels}")

        with open(os.path.join(output_dir, f'pixel_md5_{index}.txt'), 'w') as f:
            f.write(pixel_md5_checksum)

        print(f"Image {index} processed: {os.path.basename(image_path)}. Outputs saved with _{index} appended to filenames.")

# Example usage
input_folder = "disassembly_images"  # Folder containing images
output_dir = "output_bits"
os.makedirs(output_dir, exist_ok=True)
disassemble_images(input_folder, output_dir)
