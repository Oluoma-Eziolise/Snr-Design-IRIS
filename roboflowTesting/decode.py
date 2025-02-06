import base64

# Configuration
ENCODED_INPUT = "encoded_chunks.txt"  # File containing encoded chunks
OUTPUT_FILE_PATH = "received_file.zip.enc"  # Output file path

def reconstruct_file():
    """Reassembles Base64 chunks and decodes back to the original file."""
    try:
        with open(ENCODED_INPUT, "r") as input_file:
            chunks = input_file.readlines()

        encoded_data = "".join(chunk.strip() for chunk in chunks)  # Reassemble chunks
        file_data = base64.b64decode(encoded_data)  # Decode Base64

        with open(OUTPUT_FILE_PATH, "wb") as output_file:
            output_file.write(file_data)

        print(f"File successfully reconstructed as {OUTPUT_FILE_PATH}")

    except Exception as e:
        print(f"Error reconstructing file: {e}")

if __name__ == "__main__":
    reconstruct_file()
