from PIL import Image
import io

# Load the image
image_path = './dirs/circleOutput/circle_1.png'  # Replace with your image path
with Image.open(image_path) as img:
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='png')  # or PNG, etc.
    img_bytes = img_byte_arr.getvalue()

# Convert bytes to integers
byte_values = list(img_bytes)

# Save to a text file as space-separated numbers
with open('image_bytes.txt', 'w') as f:
    f.write(' '.join(str(b) for b in byte_values))

print("Image bytes saved as plain numbers in 'image_bytes.txt'")
