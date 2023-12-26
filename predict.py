import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from resize import resize_single_image

def predict_image_class(model_path, image_path, target_size=(200, 150)):
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
    
    
    
    resize_single_image(image_path, image_path, target_size)


    # Load and preprocess the image
    img = Image.open(image_path)
    img = img.resize(target_size)
    img = np.expand_dims(np.array(img) / 255.0, axis=0)  # Add batch dimension
  
    # Predict the class probability
    prediction = round(float(model.predict(img)[0][0]), 4)

    return prediction

    