import base64

def encode_image_to_base64(input_image_path, output_txt_path):
    try:
        with open(input_image_path, "rb") as image_file:
            image_bytes = image_file.read()
            base64_str = base64.b64encode(image_bytes).decode("utf-8")

        with open(output_txt_path, "w", encoding="utf-8") as out_file:
            out_file.write(base64_str)

        print(f"Image encoded successfully to {output_txt_path}")
        print(f"Length of encoded string: {len(base64_str)} characters")
    except Exception as e:
        print(f"[ERROR] {e}")

# === Example Usage ===
encode_image_to_base64("REAL_image35.png", "encoded_chunks.txt")
