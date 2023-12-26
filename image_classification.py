import tensorflow as tf
from tensorflow.keras import layers, models
from extra.random import random_string
import numpy as np
from PIL import Image
import os

from extra.version import generate_version_name

model_path = 'model/image_model'
# Define paths to your labeled 'good' and 'bad' image directories
train_good_dir = 'model/labeled/good'
train_bad_dir = 'model/labeled/bad'

# Check if directories exist
if not os.path.exists(train_good_dir) or not os.path.exists(train_bad_dir):
    raise Exception("Training directories do not exist")

# Load and preprocess images
train_images = []
train_labels = []

for filename in os.listdir(train_good_dir):
    if not filename.lower().endswith(('.png', '.jpg')):
        continue
    try:
        img = Image.open(os.path.join(train_good_dir, filename))
        img = img.resize((200, 150)) 
        img = np.array(img) / 255.0
        train_images.append(img)
        train_labels.append(1)  # Label 'good' images as 1
    except Exception as e:
        print(f"Error processing file {filename}: {str(e)}")

for filename in os.listdir(train_bad_dir):
    if not filename.lower().endswith(('.png', '.jpg')):
        continue
    try:
        img = Image.open(os.path.join(train_bad_dir, filename))
        img = img.resize((200, 150))
        img = np.array(img) / 255.0
        train_images.append(img)
        train_labels.append(0)  # Label 'bad' images as 0
    except Exception as e:
        print(f"Error processing file {filename}: {str(e)}")

# Check if any images were loaded
if not train_images:
    raise Exception("No images found in training directories")

# Convert to NumPy arrays
train_images = np.array(train_images)
train_labels = np.array(train_labels)

# Rest of the code...


# Define the model architecture (example CNN)
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 200, 4)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),  
    layers.Dense(64, activation='relu'), 
    layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(train_images, train_labels, epochs=10)  # Adjust epochs as needed

model_name = generate_version_name("myia_image_classifier.keras", model_path)
model_path = f"{model_path}/{model_name}"
# Save the model
model.save(model_path)
