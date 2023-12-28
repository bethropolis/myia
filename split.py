import os
import shutil
import random

# Define the directory containing your preprocessed images
image_dir = 'training/images'

# Define the directories for training, validation, and testing sets
train_dir = 'training/train'
test_dir = 'training/test'

# Define the percentage split for training, validation, and testing
train_split = 0.7
test_split = 0.3

# Create the directories if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Get a list of all image filenames in the directory
image_files = os.listdir(image_dir)

# Shuffle the list of filenames
random.shuffle(image_files)

# Calculate the number of images for each split
num_images = len(image_files)
num_train = int(train_split * num_images)

# Split the images into train, validation, and test sets
train_images = image_files[:num_train]
test_images = image_files[num_train + 1:]
# Move images to their respective directories
for image in train_images:
    shutil.move(os.path.join(image_dir, image), os.path.join(train_dir, image))

for image in test_images:
    shutil.move(os.path.join(image_dir, image), os.path.join(test_dir, image))

print("Data splitting complete!")
