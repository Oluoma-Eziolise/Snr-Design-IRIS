#!/usr/bin/env python
import os
import base64
import zipfile
import sys
import cv2
import numpy as np
from AesEverywhere import aes256
import subprocess
import time
from pathlib import Path

# Configuration
# ENCODED_INPUT = "./dirs/encoded_chunks.txt"  # File containing encoded chunks
ENCRYPTED_FILE_PATH = "../dirs/zipped_data/compressedImages.zip.enc"  # Encrypted file path
DECRYPTION_PASSWORD = "team10"  # Default decryption password
ZIP_FILE_PATH = "../dirs/zipped_data/compressedImages.zip"  # Path to the ZIP file
EXTRACT_DIR = "../dirs/unzippedFiles/"  # Output directory
SOURCE_FOLDER = '../dirs/unzippedFiles/'  # Folder containing images to process
OUTPUT_FOLDER = '../server/images/'  # Folder to save cropped images
# Global counter for saving circles
circle_counter = 1
MAX_CIRCLES = 10  # Limit the number of saved circles to 10
ENCODED_INPUT = "../dirs/zipped_data/encoded_chunks.txt"  # File containing base64-encoded encrypted .zip
def reconstruct_file():
    """Reassembles Base64-encoded data and writes it as the encrypted .zip.enc file."""
    try:
        with open(ENCODED_INPUT, "r", encoding="utf-8") as input_file:
            encoded_data = input_file.read().strip()

        file_data = base64.b64decode(encoded_data)

        with open(ENCRYPTED_FILE_PATH, "wb") as output_file:
            output_file.write(file_data)

        print(f" Reconstructed encrypted file: {ENCRYPTED_FILE_PATH}")

    except Exception as e:
        print(f" Error reconstructing file: {e}")
        sys.exit(1)
def find_git_root(path):
    """Finds the nearest parent directory with a .git folder."""
    path = Path(path).resolve()
    while not (path / '.git').exists():
        if path.parent == path:
            raise FileNotFoundError(".git directory not found in any parent folder.")
        path = path.parent
    return str(path)

def decrypt_zip():
    """Decrypt an AES-256 encrypted ZIP file and restore the original ZIP."""
    if not os.path.exists(ENCRYPTED_FILE_PATH):
        print(f"Error: Encrypted file '{ENCRYPTED_FILE_PATH}' does not exist.")
        sys.exit(1)

    with open(ENCRYPTED_FILE_PATH, 'r', encoding='utf-8') as f:
        encrypted_data = f.read()

    try:
        decrypted_base64 = aes256.decrypt(encrypted_data, DECRYPTION_PASSWORD)
        zip_data = base64.b64decode(decrypted_base64)
        decrypted_filename = ENCRYPTED_FILE_PATH.replace(".enc", "")
        with open(decrypted_filename, 'wb') as f:
            f.write(zip_data)
        print(f"Decryption successful! Restored ZIP file: {decrypted_filename}")

    except Exception as e:
        print(f"Decryption failed: {e}")
        sys.exit(1)


def unzip_file():
    """Extracts a ZIP file to a specified directory."""
    if not os.path.exists(ZIP_FILE_PATH):
        print(f"Error: {ZIP_FILE_PATH} not found!")
        return

    os.makedirs(EXTRACT_DIR, exist_ok=True)
    try:
        with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)
            print(f"Extracted {ZIP_FILE_PATH} to {EXTRACT_DIR}")

    except zipfile.BadZipFile:
        print("Error: Not a valid ZIP file!")
        


def detect_and_crop_red_circles(image_path, output_folder):
    """Detect and crop red circles from an image."""
    global circle_counter  # Use global counter to track saved images

    print(f"Processing image: {image_path}")  # Debugging output

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image {image_path}")
        return

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red1, upper_red1 = np.array([0, 120, 70]), np.array([10, 255, 255])
    lower_red2, upper_red2 = np.array([170, 120, 70]), np.array([180, 255, 255])
    mask1, mask2 = cv2.inRange(hsv, lower_red1, upper_red1), cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2
    red_gray = cv2.GaussianBlur(red_mask, (9, 9), 2)
    
    circles = cv2.HoughCircles(
        red_gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
        param1=100, param2=30, minRadius=20, maxRadius=60
    )

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for i, (x, y, r) in enumerate(circles):
            if circle_counter > MAX_CIRCLES:  # Stop after saving 10 circles
                print("Max circle count reached. Stopping...")
                return

            x_min, x_max = max(0, x - r), min(image.shape[1], x + r)
            y_min, y_max = max(0, y - r), min(image.shape[0], y + r)
            cropped_circle = image[y_min:y_max, x_min:x_max]
            
            # Ensure filename is correct
            cropped_circle_path = os.path.join(output_folder, f"circle_{circle_counter}.png")

            # Debugging output to verify the path
            print(f"Saving cropped circle: {cropped_circle_path}")

            # Ensure the output directory exists
            os.makedirs(output_folder, exist_ok=True)

            # Save the cropped circle
            success = cv2.imwrite(cropped_circle_path, cropped_circle)

            if success:
                print(f"[SAVED] Cropped circle {circle_counter}: {cropped_circle_path}")
            else:
                print(f"[ERROR] Failed to save image: {cropped_circle_path}")

            circle_counter += 1  # Increment counter after saving

    else:
        print(f"No circles detected in {image_path}")



def process_images_in_folder():
    """Process all images in a folder to detect and crop red circles."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    for img_filename in os.listdir(SOURCE_FOLDER):
        img_path = os.path.join(SOURCE_FOLDER, img_filename)
        if img_filename.lower().endswith(('.jpg', '.png', '.jpeg')):
            print(f"Processing {img_filename}...")
            detect_and_crop_red_circles(img_path, OUTPUT_FOLDER)
    print("Processing complete.")

    git_commit_and_push()


git_repo_path = ".."
print("Git repo path detected as:", git_repo_path)
def git_commit_and_push():
    """Automate Git commit and push workflow after processing images."""
    try:
        script_dir = Path(__file__).resolve().parent
        repo_root = script_dir.parent
        git_repo_path = str(repo_root)

        print("Navigating to Git repository...")

        if not (repo_root / ".git").exists():
            print("Error: No Git repository found in the specified path.")
            return

        os.chdir(git_repo_path)

        subprocess.run(["git", "add", "."], check=True)
        print("Staged changes for commit.")

        commit_message = f"Auto-update: Added processed circle images - {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("Committed changes.")

        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Changes pushed successfully!")
        

    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}")
        print("Ensure that Git is set up properly with authentication (SSH or HTTPS).")
    except Exception as e:
        print(f"Unexpected error: {e}")
    


if __name__ == "__main__":
    print("Waiting for encoded chunk file to appear...")

    # Wait for the encoded chunks to be written (e.g., via IR or Pi)
    while not os.path.exists(ENCODED_INPUT):
        print(f"File not found: {ENCODED_INPUT}. Retrying in 5 seconds...")
        time.sleep(5)

    print("Encoded chunk file detected. Reconstructing encrypted .zip...\n")
    reconstruct_file()
    decrypt_zip()
    git_commit_and_push()
    input("input")
