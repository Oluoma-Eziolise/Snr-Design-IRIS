import os
import shutil
from roboflow import Roboflow

# Initialize Roboflow model
rf = Roboflow(api_key="9eWUjNfqx796swfi6Fhu")
project = rf.workspace().project("deathstar-kebsz")
model = project.version(3).model

# Define directories
input_dir = "./dirs/images/input"  # Directory containing input images
output_dir = "./dirs/images/output"  # Directory where detected images will be copied
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

    return Processed


# Run the script
imageDetection()
