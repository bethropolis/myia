import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

def evaluate_and_visualize_model(model_path, test_good_dir, test_bad_dir):
    """
    Loads a trained model, evaluates its performance on testing data,
    and visualizes predictions vs. true labels for both classes.

    Args:
        model_path (str): Path to the saved model file.
        test_good_dir (str): Path to the directory containing good testing images.
        test_bad_dir (str): Path to the directory containing bad testing images.
    """
    
    graph_path = 'static/images/graph.png'

    # Load the model
    model = load_model(model_path)

    # Load and preprocess testing images for 'good' class
    test_images_good = []
    test_labels_good = []

    for filename in os.listdir(test_good_dir):
        img = Image.open(os.path.join(test_good_dir, filename))
        img = img.resize((200, 150))  # Adjust image size as needed
        img = np.array(img) / 255.0
        test_images_good.append(img)
        test_labels_good.append(1)  # Label 'good' images as 1

    test_images_good = np.array(test_images_good)
    test_labels_good = np.array(test_labels_good)

    # Load and preprocess testing images for 'bad' class
    test_images_bad = []
    test_labels_bad = []

    for filename in os.listdir(test_bad_dir):
        img = Image.open(os.path.join(test_bad_dir, filename))
        img = img.resize((200, 150))
        img = np.array(img) / 255.0
        test_images_bad.append(img)
        test_labels_bad.append(0)  # Label 'bad' images as 0

    test_images_bad = np.array(test_images_bad)
    test_labels_bad = np.array(test_labels_bad)

    # Evaluate model performance for 'good' and 'bad' classes separately
    test_loss_good, test_accuracy_good = model.evaluate(test_images_good, test_labels_good)
    test_loss_bad, test_accuracy_bad = model.evaluate(test_images_bad, test_labels_bad)
    
    print('Good Test Accuracy:', test_accuracy_good)
    print('Bad Test Accuracy:', test_accuracy_bad)

    # Generate predictions for 'good' and 'bad' classes separately
    predictions_good = model.predict(test_images_good)
    predictions_bad = model.predict(test_images_bad)

    plt.figure(figsize=(10, 6))

    # Plot predictions vs. labels for 'good' class
    plt.subplot(2, 1, 1)
    plt.plot(predictions_good, label='Predictions (Good)')
    plt.plot(test_labels_good, label='True Labels (Good)')
    plt.xlabel('Image Number')
    plt.ylabel('Probability')
    plt.title(f'Model Performance for "Good" Class (Accuracy: {test_accuracy_good:.2f})')
    plt.legend()

    # Plot predictions vs. labels for 'bad' class
    plt.subplot(2, 1, 2)
    plt.plot(predictions_bad, label='Predictions (Bad)')
    plt.plot(test_labels_bad, label='True Labels (Bad)')
    plt.xlabel('Image Number')
    plt.ylabel('Probability')
    plt.title(f'Model Performance for "Bad" Class (Accuracy: {test_accuracy_bad:.2f})')
    plt.legend()

    plt.tight_layout()
    plt.show()
    
    plt.savefig(graph_path)
    
    return graph_path;
    



# evaluate_and_visualize_model('model/image_model/updated_image_classifier.keras', 'model/labeled/good', 'model/labeled/bad')