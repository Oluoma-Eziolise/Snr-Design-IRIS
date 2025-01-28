import os
import base64
import shutil
from AesEverywhere import aes256

def decrypt_and_extract(encrypted_file, key_file, output_folder):
    """Decrypt the AES-encrypted zip file and extract its contents."""
    if not os.path.exists(encrypted_file):
        print(f"The encrypted file '{encrypted_file}' does not exist.")
        return

    if not os.path.exists(key_file):
        print(f"The key file '{key_file}' does not exist.")
        return

    # Step 1: Load the key
    with open(key_file, 'r') as f:
        key = f.read().strip()

    # Step 2: Decrypt the file
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()

    try:
        decrypted_base64 = aes256.decrypt(encrypted_data, key)
        zip_data = base64.b64decode(decrypted_base64)
    except Exception as e:
        print(f"Error decrypting the file: {e}")
        return

    # Step 3: Save the decrypted zip file
    decrypted_zip_path = "decrypted_output_bits.zip"
    with open(decrypted_zip_path, 'wb') as f:
        f.write(zip_data)
    print(f"Decrypted zip file saved to '{decrypted_zip_path}'.")

    # Step 4: Extract the decrypted zip file
    shutil.unpack_archive(decrypted_zip_path, output_folder, 'zip')
    print(f"Extracted contents into '{output_folder}'.")

    # Optional: Clean up the decrypted zip file
    os.remove(decrypted_zip_path)
    print(f"Decrypted zip file '{decrypted_zip_path}' removed.")

# Example usage
if __name__ == "__main__":
    encrypted_file_path = "output_bits_encrypted.aes"  # Encrypted zip file
    key_file_path = "encryption_key.txt"  # Key file
    extraction_folder = "output_bits_uncompressed"  # Folder to extract contents

    decrypt_and_extract(encrypted_file_path, key_file_path, extraction_folder)
