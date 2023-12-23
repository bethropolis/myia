from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os

# Load the saved model
model = load_model('model/image_model/my_image_classifier.keras')

# Define paths to your labeled 'good' and 'bad' test image directories
test_good_dir = 'model/evaluation/good'
test_bad_dir = 'model/evaluation/bad'

# Evaluate each image individually
for directory in [test_good_dir, test_bad_dir]:
    for filename in os.listdir(directory):
        img_path = os.path.join(directory, filename)

        # Load and preprocess the image
        img = Image.open(img_path)
        img = img.resize((200, 150))  # Adjust image size as needed
        img = np.expand_dims(np.array(img) / 255.0, axis=0)  # Add batch dimension

        # Predict the class
        prediction = model.predict(img)[0][0]  # Extract the prediction value
        predicted_class = 1 if prediction >= 0.5 else 0  # Threshold for binary classification

        # Print the results
        print(f"Image: {img_path}")
        print(f"Predicted class: {predicted_class}")
        print(f"Prediction score: {prediction:.4f}")
        print("----------------------------------")
