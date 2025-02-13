import os
import cv2
import numpy as np

# Function to detect and crop red circles from an image
def detect_and_crop_red_circles(image_path, output_folder):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to HSV color space to detect red
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the red color range in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create masks to detect red in the image
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2

    # Convert the red areas mask to grayscale and blur it
    red_gray = cv2.GaussianBlur(red_mask, (9, 9), 2)

    # Detect circles using HoughCircles in the red-only masked image
    circles = cv2.HoughCircles(red_gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50, param1=100, param2=30, minRadius=20, maxRadius=60)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        for i, (x, y, r) in enumerate(circles):
            # Crop the area inside the circle
            x_min = max(0, x - r)
            x_max = min(image.shape[1], x + r)
            y_min = max(0, y - r)
            y_max = min(image.shape[0], y + r)

            cropped_circle = image[y_min:y_max, x_min:x_max]

            # Save the cropped image
            cropped_circle_path = os.path.join(output_folder, f"cropped_circle_{i}_{os.path.basename(image_path)}")
            cv2.imwrite(cropped_circle_path, cropped_circle)
            print(f"[SAVED] Red circle detected! Cropped circle saved: {cropped_circle_path}")

# Main function to process all images in a folder
def process_images_in_folder(source_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all files in the source folder
    for img_filename in os.listdir(source_folder):
        img_path = os.path.join(source_folder, img_filename)

        # Check if it's an image
        if img_filename.lower().endswith(('.jpg', '.png', '.jpeg')):
            print(f"Processing {img_filename}...")

            # Detect and crop red circles
            detect_and_crop_red_circles(img_path, output_folder)

    print("Processing complete.")

# Set the input folder containing images and output folder for cropped images
source_folder = './Dirs/receivedImages'  # Folder containing images to process
output_folder = './dirs/circleOutput'  # Folder to save cropped images

# Run the script
process_images_in_folder(source_folder, output_folder)
