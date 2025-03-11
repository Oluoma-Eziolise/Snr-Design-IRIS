import os
import base64
import zipfile
import sys
import cv2
import numpy as np
from AesEverywhere import aes256
import subprocess
import time

# Configuration
# ENCODED_INPUT = "./dirs/encoded_chunks.txt"  # File containing encoded chunks
# ENCRYPTED_FILE_PATH = "./dirs/received_file.zip.enc"  # Encrypted file path
# DECRYPTION_PASSWORD = "team10"  # Default decryption password
ZIP_FILE_PATH = "./dirs/received_file.zip"  # Path to the ZIP file
EXTRACT_DIR = "./dirs/unzippedFiles/"  # Output directory
SOURCE_FOLDER = './dirs/unzippedFiles/'  # Folder containing images to process
OUTPUT_FOLDER = './dirs/circleOutput'  # Folder to save cropped images


# def reconstruct_file():
#     """Reassembles Base64 chunks and decodes back to the original file."""
#     try:
#         with open(ENCODED_INPUT, "r") as input_file:
#             chunks = input_file.readlines()
        
#         encoded_data = "".join(chunk.strip() for chunk in chunks)  # Reassemble chunks
#         file_data = base64.b64decode(encoded_data)  # Decode Base64

#         with open(ENCRYPTED_FILE_PATH, "wb") as output_file:
#             output_file.write(file_data)

#         print(f"File successfully reconstructed as {ENCRYPTED_FILE_PATH}")
#     except Exception as e:
#         print(f"Error reconstructing file: {e}")


# def decrypt_zip():
#     """Decrypt an AES-256 encrypted ZIP file and restore the original ZIP."""
#     if not os.path.exists(ENCRYPTED_FILE_PATH):
#         print(f"Error: Encrypted file '{ENCRYPTED_FILE_PATH}' does not exist.")
#         sys.exit(1)

#     with open(ENCRYPTED_FILE_PATH, 'r', encoding='utf-8') as f:
#         encrypted_data = f.read()

#     try:
#         decrypted_base64 = aes256.decrypt(encrypted_data, DECRYPTION_PASSWORD)
#         zip_data = base64.b64decode(decrypted_base64)
#         decrypted_filename = ENCRYPTED_FILE_PATH.replace(".enc", "")
#         with open(decrypted_filename, 'wb') as f:
#             f.write(zip_data)
#         print(f"Decryption successful! Restored ZIP file: {decrypted_filename}")
#     except Exception as e:
#         print(f"Decryption failed: {e}")
#         sys.exit(1)


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
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red1, upper_red1 = np.array([0, 120, 70]), np.array([10, 255, 255])
    lower_red2, upper_red2 = np.array([170, 120, 70]), np.array([180, 255, 255])
    mask1, mask2 = cv2.inRange(hsv, lower_red1, upper_red1), cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2
    red_gray = cv2.GaussianBlur(red_mask, (9, 9), 2)
    circles = cv2.HoughCircles(red_gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50, param1=100, param2=30, minRadius=20, maxRadius=60)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for i, (x, y, r) in enumerate(circles):
            x_min, x_max = max(0, x - r), min(image.shape[1], x + r)
            y_min, y_max = max(0, y - r), min(image.shape[0], y + r)
            cropped_circle = image[y_min:y_max, x_min:x_max]
            cropped_circle_path = os.path.join(output_folder, f"cropped_circle_{i}_{os.path.basename(image_path)}")
            cv2.imwrite(cropped_circle_path, cropped_circle)
            print(f"[SAVED] Cropped circle saved: {cropped_circle_path}")


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

git_repo_path = "C:/Users/kiese/OneDrive/Documents/snrdes/Snr-Design-IRIS"

def git_commit_and_push():
    """Automate Git commit and push workflow after processing images."""
    try:
        os.chdir(git_repo_path)  # Navigate to the Git repository
        print("Navigating to Git repository...")

        # Check if Git is initialized
        if not os.path.exists(os.path.join(git_repo_path, ".git")):
            print("Error: No Git repository found in the specified path.")
            return

        # Add only new/modified files
        subprocess.run(["git", "add", "."], check=True)
        print("Staged changes for commit.")

        # Commit with a timestamp message
        commit_message = f"Auto-update: Added processed circle images - {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("Committed changes.")

        # Push changes to remote repository
        subprocess.run(["git", "push", "origin", "main"], check=True)  # Change 'main' if needed
        print("Changes pushed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}")
        print("Ensure that Git is set up properly with authentication (SSH or HTTPS).")
    except Exception as e:
        print(f" Unexpected error: {e}")

if __name__ == "__main__":
    # reconstruct_file()
    # decrypt_zip()
    unzip_file()
    process_images_in_folder()
