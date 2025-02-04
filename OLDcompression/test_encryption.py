import os
import shutil
import base64
from AesEverywhere import aes256

def generate_key():
    """Generate a random AES key."""
    from secrets import token_urlsafe
    return token_urlsafe(32)  # 32 bytes for AES-256

def compress_and_encrypt(folder_path, zip_output, encrypted_output, key_file):
    """Compress a folder, encrypt the zip file, and save the encryption key."""
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # Step 1: Compress the folder into a zip file
    zip_path = f"{zip_output}.zip"
    shutil.make_archive(zip_output, 'zip', folder_path)
    print(f"Compressed '{folder_path}' into '{zip_path}'.")

    # Step 2: Generate a key for encryption
    key = generate_key()
    with open(key_file, 'w') as f:
        f.write(key)
    print(f"Encryption key saved to '{key_file}'.")

    # Step 3: Encrypt the zip file
    with open(zip_path, 'rb') as f:
        zip_data = f.read()

    # Convert bytes to a base64 string
    zip_data_base64 = base64.b64encode(zip_data).decode('utf-8')

    # Encrypt the base64 string
    encrypted_data = aes256.encrypt(zip_data_base64, key)

    # Write the encrypted data to a file (it is already bytes)
    with open(encrypted_output, 'wb') as f:
        f.write(encrypted_data)
    print(f"Encrypted zip file saved to '{encrypted_output}'.")

    # Clean up the unencrypted zip file
    os.remove(zip_path)
    print(f"Unencrypted zip file '{zip_path}' removed.")

# Example usage
if __name__ == "__main__":
    folder_to_compress = "output_bits"  # Folder to compress and encrypt
    zip_output_name = "output_bits_compressed"  # Base name for the zip file
    encrypted_output_file = "output_bits_encrypted.aes"  # Encrypted file
    encryption_key_file = "encryption_key.txt"  # Key file

    compress_and_encrypt(folder_to_compress, zip_output_name, encrypted_output_file, encryption_key_file)
