import os
import shutil

def decompress_zip(zip_file, output_folder):
    """Decompress a zip file into a folder."""
    if not os.path.exists(zip_file):
        print(f"The zip file '{zip_file}' does not exist.")
        return

    try:
        shutil.unpack_archive(zip_file, output_folder, 'zip')
        print(f"Decompressed '{zip_file}' into '{output_folder}'.")
    except Exception as e:
        print(f"Error decompressing zip file: {e}")


# Example usage
if __name__ == "__main__":
    zip_file_path = "output_bits_compressed.zip"  # Zip file to decompress
    extraction_folder = "output_bits_uncompressed"  # Folder to extract to
    decompress_zip(zip_file_path, extraction_folder)
