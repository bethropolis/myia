import json
import tensorflow as tf
from tensorflow.keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

from image_enhance import enhance_image
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
from threading import Thread


def evaluate_and_visualize_model(model_path, test_good_dir, test_bad_dir, model_name, configs={}):
    """
    Loads a trained model, evaluates its performance on testing data,
    and visualizes predictions vs. true labels for both classes.

    Args:
        model_path (str): Path to the saved model file.
        test_good_dir (str): Path to the directory containing good testing images.
        test_bad_dir (str): Path to the directory containing bad testing images.
        model_name (str): Name of the model for watermarking.
    """
    
    graph_path = 'static/images/graph.png'
    temperature = float(configs.get('temperature', 1.0))
    data_augmentation = configs.get('data_augmentation', False)

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

    if temperature != 1.0:
            predictions_good = np.power(predictions_good, 1.0 / temperature)
            predictions_bad = np.power(predictions_bad, 1.0 / temperature)
            
            
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
    
    # Add watermark with model name at the bottom right
    plt.text(0.99, 0.01, f'Model: {model_name}', ha='right', va='bottom', transform=plt.gcf().transFigure, color='grey', fontsize=10, fontweight='bold')
    
    plt.show()
    
    plt.savefig(graph_path)
    
    model_graph_name = f"graph_{model_name}.png"
    model_graph_path = f"static/images/{model_graph_name}";
    
    Thread(target=save_graph, args=(model_graph_path,)).start()
    
    evaluation_results = {
        'accuracy_good': float(test_accuracy_good),
        'accuracy_bad': float(test_accuracy_bad),
        'loss_good': float(test_loss_good),
        'loss_bad': float(test_loss_bad),
        'temperature': temperature,
        'data_augmentation': data_augmentation,
        'average_accuracy': float((test_accuracy_good + test_accuracy_bad) / 2),
        'average_loss': float((test_loss_good + test_loss_bad) / 2),
        'graph_path': model_graph_name,
        "static_path": model_graph_path
        }

    try:
        with open('model/model_evaluations.json', 'r+', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                data = {}

            data[model_name] = evaluation_results
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    except FileNotFoundError:
        with open('model/model_evaluations.json', 'w', encoding='utf-8') as f:
            data = {model_name: evaluation_results}
            json.dump(data, f, indent=4)
        
    # Enhance graph image in background thread
    Thread(target=enhance_image, args=(graph_path,)).start()
            
    return graph_path;

def save_graph(graph_path):
    plt.savefig(graph_path)