import tensorflow as tf
from tensorflow.keras import layers, models
from extra.version import generate_version_name 
import numpy as np
from PIL import Image
import os

def create_model(train_good_dir, train_bad_dir, config):
    """Creates and trains an image classification model.

    Args:
        train_good_dir (str): Path to the directory containing good images.
        train_bad_dir (str): Path to the directory containing bad images.
        config (dict): Configuration dictionary with the following keys:
            epochs (int): Number of epochs to train the model.
            no_layers (int): Number of dense layers to include in the model.

    Returns:
        dict: A dictionary containing the model name and path, or False on error.
    """



    try:
        # Check directory existence
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
            

        # Define the model architecture
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 200, 4)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            *[layers.Dense(64, activation='relu') for _ in range(config['no_layers'] - 1)],  # Add dense layers based on config
            layers.Dense(1, activation='sigmoid')
        ])

        # Compile the model
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        # Train the model
        model.fit(train_images, train_labels, epochs=config['epochs'])

        model_name = generate_version_name(f"{config['model_name']}.keras", "model/image_model")
        model_path = f"model/image_model/{model_name}"

        # Save the model
        model.save(model_path)

        return {"model_name": model_name, "model_path": model_path}

    except Exception as e:
        print(f"Error creating model: {str(e)}")
        return False


if __name__ == "__main__":
    config = {"epochs": 15, "no_layers": 2}
    model = create_model("model/labeled/good", "model/labeled/bad", config)
    print(model)