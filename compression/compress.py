import os
import shutil

def compress_folder(folder_path, output_zip):
    """Compress a folder into a zip file."""
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return
    
    try:
        shutil.make_archive(output_zip, 'zip', folder_path)
        print(f"Compressed '{folder_path}' into '{output_zip}.zip'.")
    except Exception as e:
        print(f"Error compressing folder: {e}")

# Example usage
if __name__ == "__main__":
    folder_to_compress = "output_bits"  # Folder to compress
    output_zip_name = "output_bits_compressed"  # Name of the zip file (without extension)
    compress_folder(folder_to_compress, output_zip_name)
