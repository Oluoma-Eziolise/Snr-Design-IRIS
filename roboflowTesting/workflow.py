import os
import shutil
from roboflow import Roboflow

# Initialize Roboflow model
rf = Roboflow(api_key="9eWUjNfqx796swfi6Fhu")
project = rf.workspace().project("deathstar-kebsz")
model = project.version(2).model

# Define directories
input_dir = "./testImages/input"  # Directory containing input images
output_dir = "./testImages/output"  # Directory where detected images will be copied

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Confidence and overlap thresholds
CONFIDENCE_THRESHOLD = 60  # Adjust as needed
OVERLAP_THRESHOLD = 20  # Adjust as needed

# Process each image in the directory
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

print("Processing complete!")
