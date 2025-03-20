import os
import sys
import base64
from AesEverywhere import aes256

# Configuration
encrypted_file_path = "./dirs/received_file.zip.enc"  # Path to the encrypted file
decryption_password = "team10"  # Default decryption password

def decrypt_zip(encrypted_file, password):
    """Decrypt an AES-256 encrypted ZIP file and restore the original ZIP."""
    if not os.path.exists(encrypted_file):
        print(f"Error: Encrypted file '{encrypted_file}' does not exist.")
        sys.exit(1)

    with open(encrypted_file, 'r', encoding='utf-8') as f:
        encrypted_data = f.read()

    try:
        # Decrypt the encrypted data
        decrypted_base64 = aes256.decrypt(encrypted_data, password)
        
        # Decode Base64 back to binary ZIP data
        zip_data = base64.b64decode(decrypted_base64)

        # Restore the original ZIP filename by removing .enc extension
        decrypted_filename = encrypted_file.replace(".enc", "")

        with open(decrypted_filename, 'wb') as f:
            f.write(zip_data)

        print(f"Decryption successful! Restored ZIP file: {decrypted_filename}")
        return decrypted_filename

    except Exception as e:
        print(f"Decryption failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    decrypted_file = decrypt_zip(encrypted_file_path, decryption_password)
