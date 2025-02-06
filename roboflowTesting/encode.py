import base64

# Configuration
FILE_PATH = "./zipped_data/compressedIMages.zip.enc"  # File to encode
CHUNK_SIZE = 64  # Size of each chunk in bytes
ENCODED_OUTPUT = "encoded_chunks.txt"  # Output file storing encoded chunks

def encode_and_split_file():
    """Encodes a file in Base64 and splits it into chunks."""
    if not FILE_PATH:
        print("Error: No file specified!")
        return

    try:
        with open(FILE_PATH, "rb") as file:
            file_data = file.read()

        encoded_data = base64.b64encode(file_data).decode()
        print(f"Total encoded length: {len(encoded_data)} characters")

        # Split into chunks
        chunks = [encoded_data[i:i+CHUNK_SIZE] for i in range(0, len(encoded_data), CHUNK_SIZE)]

        # Save chunks to a file (for transmission)
        with open(ENCODED_OUTPUT, "w") as output_file:
            for chunk in chunks:
                output_file.write(chunk + "\n")

        print(f"Encoded data split into {len(chunks)} chunks and saved to {ENCODED_OUTPUT}")

        return chunks  # Return chunks if needed for transmission

    except Exception as e:
        print(f"Error encoding file: {e}")

if __name__ == "__main__":
    encode_and_split_file()
