import zipfile
import os

# Configuration
ZIP_FILE_PATH = "./dirs/received_file.zip"  # Path to the ZIP file
EXTRACT_DIR = "./dirs/unzippedFIles/"  # Output directory

def unzip_file():
    """Extracts a ZIP file to a specified directory."""
    if not os.path.exists(ZIP_FILE_PATH):
        print(f"Error: {ZIP_FILE_PATH} not found!")
        return

    # Create the extraction directory if it doesn't exist
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    try:
        with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)
            print(f"Extracted {ZIP_FILE_PATH} to {EXTRACT_DIR}")

    except zipfile.BadZipFile:
        print("Error: Not a valid ZIP file!")

if __name__ == "__main__":
    unzip_file()
