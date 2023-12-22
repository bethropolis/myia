import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
from PIL import Image
import os

# Define paths to your labeled 'good' and 'bad' image directories
train_good_dir = 'training/good'
train_bad_dir = 'training/bad'

# Load and preprocess images
train_images = []
train_labels = []

for filename in os.listdir(train_good_dir):
    img = Image.open(os.path.join(train_good_dir, filename))
    img = img.resize((200, 150))  # Adjust image size as needed
    img = np.array(img) / 255.0
    train_images.append(img)
    train_labels.append(1)  # Label 'good' images as 1

for filename in os.listdir(train_bad_dir):
    img = Image.open(os.path.join(train_bad_dir, filename))
    img = img.resize((200, 150))
    img = np.array(img) / 255.0
    train_images.append(img)
    train_labels.append(0)  # Label 'bad' images as 0

# Convert to NumPy arrays
train_images = np.array(train_images)
train_labels = np.array(train_labels)

print(train_images[0].shape)

# Define the model architecture (example CNN)
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 200, 4)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # Output layer for binary classification
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(train_images, train_labels, epochs=10)  # Adjust epochs as needed

# Save the model
model.save('my_image_classifier.keras')
