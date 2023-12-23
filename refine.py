from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os

# Load the saved model
model = load_model('model/image_model/my_image_classifier.keras')

# Define paths to your additional labeled 'good' and 'bad' image directories
additional_good_dir = 'model/evaluation/good'
additional_bad_dir = 'model/evaluation/bad'

# Load and preprocess additional 'good' images
additional_good_images = []
additional_good_labels = []

for filename in os.listdir(additional_good_dir):
    img = Image.open(os.path.join(additional_good_dir, filename))
    img = img.resize((200, 150))  # Adjust image size as needed
    img = np.array(img) / 255.0
    additional_good_images.append(img)
    additional_good_labels.append(1)  # Label 'good' images as 1

# Load and preprocess additional 'bad' images
additional_bad_images = []
additional_bad_labels = []

for filename in os.listdir(additional_bad_dir):
    img = Image.open(os.path.join(additional_bad_dir, filename))
    img = img.resize((200, 150))  # Adjust image size as needed
    img = np.array(img) / 255.0
    additional_bad_images.append(img)
    additional_bad_labels.append(0)  # Label 'bad' images as 0

# Convert to NumPy arrays
additional_good_images = np.array(additional_good_images)
additional_good_labels = np.array(additional_good_labels)
additional_bad_images = np.array(additional_bad_images)
additional_bad_labels = np.array(additional_bad_labels)

# Combine new and existing data
combined_images = np.concatenate((additional_good_images, additional_bad_images), axis=0)
combined_labels = np.concatenate((additional_good_labels, additional_bad_labels), axis=0)

# Retrain the model with combined data
model.fit(combined_images, combined_labels, epochs=5)  # Adjust epochs as needed

# Save the updated model
model.save('model/image_model/updated_image_classifier.keras')
