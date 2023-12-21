from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import shutil
import json

app = Flask(__name__)

# Function to load image paths
def load_images():
    images = []
    # Get all image paths from a directory
    image_dir = './training/test'
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                images.append(os.path.join(root, file))
    return images

# Function to load labeled images from JSON file
def load_labeled_images():
    labeled_images = []
    json_file = 'labeled_images.json'
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            labeled_images = json.load(file)
    return labeled_images

# Route to send images to frontend
@app.route('/')
def index():
    images = load_images()  # Load images
    labeled_images = load_labeled_images()  # Load labeled images from JSON
    images_to_send = [image for image in images if image not in labeled_images]
    return render_template('index.html', images=images_to_send)

# Route to label images and update JSON file
@app.route('/label', methods=['POST'])
def label_images():
    label = request.form['label']
    image_path = request.form['image_path']
    labeled_images = load_labeled_images()  # Load labeled images from JSON

    # Move image if not already labeled
    if image_path not in labeled_images:
        if label == 'good':
            shutil.move(image_path, 'training/good')
        elif label == 'bad':
            shutil.move(image_path, 'training/bad')

        # Update JSON file with labeled image
        labeled_images.append(image_path)
        with open('labeled_images.json', 'w') as file:
            json.dump(labeled_images, file)

    return 'Image labeled successfully!'

@app.route('/get_images')
def get_images():
    images = load_images()  # Load images from directory
    labeled_images = load_labeled_images()  # Load labeled images from JSON

    # Filter images to send (unlabeled)
    images_to_send = [image for image in images if image not in labeled_images]

    return render_template('image_template.html', images=images_to_send)

@app.route('/training/<path:filename>')
def serve_training_images(filename):
    training_folder = 'training'  
    return send_from_directory(training_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
