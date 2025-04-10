from PIL import Image

def png_to_binary(png_path, bin_path, size=(32, 32)):
    img = Image.open("./dirs/circleOutput/circle_1.png").convert("1")  # Convert to 1-bit
    img = img.resize(size)

    width, height = img.size
    print(f"Image size: {width}x{height}")

    with open(bin_path, "wb") as f:
        # Write header: width and height as single bytes
        f.write(bytes([width, height]))

        for y in range(height):
            byte = 0
            bit_count = 0
            for x in range(width):
                pixel = 0 if img.getpixel((x, y)) else 1  # 1 = black, 0 = white
                byte = (byte << 1) | pixel
                bit_count += 1

                if bit_count == 8:
                    f.write(bytes([byte]))
                    byte = 0
                    bit_count = 0

            if bit_count != 0:
                byte <<= (8 - bit_count)  # pad the remaining bits
                f.write(bytes([byte]))

    print(f"Saved binary image to {bin_path}")

# Example usage:
png_to_binary("image.png", "image.bin", size=(32, 32))
