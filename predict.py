import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model


model_path = "my_image_classifier.keras"

def predict_image_class(image_path, target_size=(200, 150)):
    """Predicts the class of an image using a loaded Keras model.

    Args:
        model_path (str): Path to the saved Keras model.
        image_path (str): Path to the image to be classified.
        target_size (tuple, optional): Desired image size for model input. Defaults to (200, 150).

    Returns:
        float: The predicted class probability (0.0 to 1.0).
    """
    # Load the model
    model = load_model(model_path)

    # Load and preprocess the image
    img = Image.open(image_path)
    img = img.resize(target_size)
    img = np.expand_dims(np.array(img) / 255.0, axis=0)  # Add batch dimension

    # Predict the class probability
    prediction = round(float(model.predict(img)[0][0]), 4)

    return prediction
