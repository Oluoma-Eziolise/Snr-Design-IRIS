import os
import shutil
import zipfile
import sys
import base64  # Import base64 for encoding binary data
from AesEverywhere import aes256

print("AesEverywhere module loaded successfully!")

# Configuration
zip_source_folder = "./testImages/compressed_images"  # Source folder to copy and zip
zip_destination_parent = "./zipped_data"  # Destination folder
zip_filename = "compressedImages.zip"  # Name of the ZIP file
zip_file_path = os.path.join(zip_destination_parent, zip_filename)  # Full ZIP file path
encryption_password = "team10"  # Default encryption password

def copy_folder(zip_source_folder, zip_destination_parent):
    """Copy the entire folder to the destination directory."""
    if not os.path.exists(zip_source_folder):
        print(f"Error: Source folder '{zip_source_folder}' does not exist.")
        sys.exit(1)

    folder_name = os.path.basename(zip_source_folder)
    zip_destination_folder = os.path.join(zip_destination_parent, folder_name)

    # Remove existing destination folder to avoid conflicts
    if os.path.exists(zip_destination_folder):
        shutil.rmtree(zip_destination_folder)

    # Copy folder and all contents
    shutil.copytree(zip_source_folder, zip_destination_folder)
    print(f"Folder copied: {zip_source_folder} -> {zip_destination_folder}")

    return zip_destination_folder

def zip_folder(folder_path, zip_file_path):
    """Zip the entire folder."""
    os.makedirs(zip_destination_parent, exist_ok=True)  # Ensure output directory exists

    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Maintain relative structure
                zipf.write(file_path, arcname)

    print(f"Folder zipped successfully: {zip_file_path}")
    return zip_file_path

def encrypt_zip(input_zip, password):
    """Encrypt the ZIP file using AES-256 (Base64 encoding)."""
    if not os.path.exists(input_zip):
        print(f"Error: ZIP file '{input_zip}' does not exist.")
        sys.exit(1)

    with open(input_zip, 'rb') as f:
        zip_data = f.read()
    
    # Encode binary data to Base64 before encrypting
    zip_base64 = base64.b64encode(zip_data).decode('utf-8')
    encrypted_data = aes256.encrypt(zip_base64, password).decode('utf-8')  # Ensure it's a string

    encrypted_filename = input_zip + ".enc"
    with open(encrypted_filename, 'w', encoding='utf-8') as f:
        f.write(encrypted_data)  # Now correctly writing a string

    print(f"File encrypted successfully: {encrypted_filename}")
    return encrypted_filename



if __name__ == "__main__":
    os.makedirs(zip_destination_parent, exist_ok=True)  # Ensure the output directory exists

    copied_folder = copy_folder(zip_source_folder, zip_destination_parent)
    zip_file_path = zip_folder(copied_folder, zip_file_path)
    encrypted_file_path = encrypt_zip(zip_file_path, encryption_password)

    print(f"Encryption complete! Encrypted file saved as: {encrypted_file_path}")

    # Test decryption (optional)
    #decrypted_file_path = decrypt_zip(encrypted_file_path, encryption_password)
    #print(f"Decryption complete! Decrypted file saved as: {decrypted_file_path}")
