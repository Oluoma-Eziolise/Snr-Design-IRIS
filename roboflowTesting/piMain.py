#!/usr/bin/env python
import os
import shutil
import zipfile
import base64
from roboflow import Roboflow
from PIL import Image
from AesEverywhere import aes256

# Initialize Roboflow model
rf = Roboflow(api_key="9eWUjNfqx796swfi6Fhu")
project = rf.workspace().project("deathstar-kebsz")
model = project.version(3).model

# Directories
input_dir = "../dirs/images/input"
output_dir = "../dirs/images/output"
compressed_folder = "../dirs/images/compressed_images"
zip_destination_parent = "../dirs/zipped_data"
zip_filename = "compressedImages.zip"
zip_file_path = os.path.join(zip_destination_parent, zip_filename)
encryption_password = "team10"
encoded_output_path = os.path.join(zip_destination_parent, "encoded_chunks.txt")

# Compression settings
compression_quality = 70
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".webp")

# Ensure directories exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(zip_destination_parent, exist_ok=True)

# Step 1: Image Detection
def image_detection():
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(SUPPORTED_FORMATS):
            image_path = os.path.join(input_dir, filename)
            try:
                prediction = model.predict(image_path, confidence=40, overlap=10).json()
                if prediction.get("predictions"):
                    shutil.copy(image_path, os.path.join(output_dir, filename))
            except Exception as e:
                print(f"[ERROR] {filename}: {e}")
    print("Image Detection Complete!")
    # Wait for user input to continue
    while True:
        user_input = input("Please verify images and type 'continue' to proceed: ").strip().lower()
        if user_input == "continue":
            break
        print("Invalid input. Please type 'continue' exactly.")

# Step 2: Compress Images
def compress_image(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img.save(image_path, optimize=True, quality=compression_quality)
    except Exception as e:
        print(f"Error compressing {image_path}: {e}")

def compress_folder():
    if os.path.exists(compressed_folder):
        shutil.rmtree(compressed_folder)
    shutil.copytree(output_dir, compressed_folder)
    for root, _, files in os.walk(compressed_folder):
        for filename in files:
            if filename.lower().endswith(SUPPORTED_FORMATS):
                compress_image(os.path.join(root, filename))
    print("Compression Complete!")

# Step 3: Zip and Encrypt
def zip_folder():
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(compressed_folder):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), compressed_folder))
    print("Zipping Complete!")

def encrypt_zip():
    with open(zip_file_path, 'rb') as f:
        zip_data = f.read()
    zip_base64 = base64.b64encode(zip_data).decode('utf-8')
    encrypted_data = aes256.encrypt(zip_base64, encryption_password).decode('utf-8')
    encrypted_filename = zip_file_path + ".enc"
    with open(encrypted_filename, 'w', encoding='utf-8') as f:
        f.write(encrypted_data)
    print("Encryption Complete!")
    return encrypted_filename

# Step 4: Encode Encrypted File to Base64 and Save for Reconstruction
def save_encoded_chunks(encrypted_file_path, output_txt_path):
    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()
        encoded = base64.b64encode(encrypted_data).decode('utf-8')
        with open(output_txt_path, 'w', encoding='utf-8') as out:
            out.write(encoded)
        print(f"Encoded data written to {output_txt_path}")


# Run the workflow
image_detection()
compress_folder()
zip_folder()
encrypted_file = encrypt_zip()
save_encoded_chunks(encrypted_file, encoded_output_path)

print("Workflow Complete!")
input("Press Enter to continue...")
