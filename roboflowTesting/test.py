from roboflow import Roboflow
rf = Roboflow(api_key="9eWUjNfqx796swfi6Fhu")
project = rf.workspace().project("deathstar-kebsz")
model = project.version(3).model

# infer on a local image
print(model.predict("./dataset/roboflow/test/images/image_variation_10_jpg.rf.6273fe65a55ed27c53f361f71ad5dea9.jpg", confidence=40, overlap=30).json())

# visualize your prediction
# model.predict("your_image.jpg", confidence=40, overlap=30).save("prediction.jpg")

# infer on an image hosted elsewhere
# print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())