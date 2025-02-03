import os
import shutil
from roboflow import Roboflow
import cv2
import numpy as np
# Initialize Roboflow model
rf = Roboflow(api_key="9eWUjNfqx796swfi6Fhu")
project = rf.workspace().project("deathstar-kebsz")
model = project.version(3).model

# Define directories
input_dir = "./testImages/input"  # Directory containing input images
output_dir = "./testImages/output"  # Directory where detected images will be copied
Processed = False
# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Confidence and overlap thresholds
CONFIDENCE_THRESHOLD = 40  # Adjust as needed
OVERLAP_THRESHOLD = 10  # Adjust as needed

# Process each image in the directory
def imageDetection ():
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Process only image files
            image_path = os.path.join(input_dir, filename)

            try:
                # Run prediction
                prediction = model.predict(image_path, confidence=CONFIDENCE_THRESHOLD, overlap=OVERLAP_THRESHOLD).json()

                # Check if "death scar" is detected in predictions
                if prediction.get("predictions"):  # If there are any detected objects
                    confidence_scores = [obj["confidence"] for obj in prediction["predictions"]]
                    max_confidence = max(confidence_scores)  # Get the highest confidence score

                    print(f"[MATCH] {filename} - Death scar detected! (Max Confidence: {max_confidence:.2f}%)")

                    # Copy the image to the output directory
                    shutil.copy(image_path, os.path.join(output_dir, filename))
                else:
                    print(f"[NO MATCH] {filename} - No death scar detected.")
            
            except Exception as e:
                print(f"[ERROR] Failed to process {filename}: {e}")
    Processed = True
    print("Processing complete!")
    print(Processed)
    process_images_in_folder(source_folder, output_folder)
    return Processed

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

    print("Processing circles complete.")

# Set the input folder containing images and output folder for cropped images
source_folder = './testImages/output'  # Folder containing images to process
output_folder = './circleOutput'  # Folder to save cropped images

# Run the script
imageDetection()
