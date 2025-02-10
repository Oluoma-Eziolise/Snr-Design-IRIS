import os
import shutil
import zipfile
import sys
import aes_everywhere
import argparse


# Configuration
zip_source_folder = "./testImages/compressed_images"  # Change to the folder you want to copy and zip
zip_destination_parent = "zipped_data"  # Folder where copied and zipped folder will be placed
zip_filename = "compressedImages.zip"  # Name of the final ZIP file

def copy_folder(zip_source_folder, zip_destination_parent):
    """Copy the entire folder to the destination directory."""
    folder_name = os.path.basename(zip_source_folder)
    zip_destination_folder = os.path.join(zip_destination_parent, folder_name)

    # Remove existing destination folder to avoid conflicts
    if os.path.exists(zip_destination_folder):
        shutil.rmtree(zip_destination_folder)

    # Copy folder and all contents
    shutil.copytree(zip_source_folder, zip_destination_folder)
    print(f"Folder copied: {zip_source_folder} -> {zip_destination_folder}")

    return zip_destination_folder

def zip_folder(folder_path, zip_filename):
    """Zip the entire folder."""
    zip_path = os.path.join(zip_destination_parent, zip_filename)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Maintain relative structure
                zipf.write(file_path, arcname)

    print(f"Folder zipped: {zip_path}")




if __name__ == "__main__":
    os.makedirs(zip_destination_parent, exist_ok=True)  # Ensure the output directory exists
    copied_folder = copy_folder(zip_source_folder, zip_destination_parent)
    zip_folder(copied_folder, zip_filename)
    print("Process complete!")

