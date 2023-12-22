from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
from predict import predict_image_class
import os
import shutil
import json
import random

app = Flask(__name__)

training_folder = 'training'   
test_image_dir = 'training/images'
train_image_dir = 'training/train'
evaluation_good_dir = 'model/evaluation/good'
evaluation_bad_dir = 'model/evaluation/bad'
label_good_dir = 'model/labeled/good'
label_bad_dir = 'model/labeled/bad'

# Function to load image paths
def load_images(dir):
    images = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                images.append(os.path.join(root, file))
    return images

def get_username(filename):
    parts = filename.split('_')
    if len(parts) >= 2:
        return parts[1]
    else:
        return "Title" 
    
# create directory if not exists
def create_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    
 
# Function to load labeled images from JSON file
def load_labeled_images():
    labeled_images = []
    json_file = 'model/labeled_images.json'
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            labeled_images = json.load(file)
    return labeled_images

# Route to send images to frontend
@app.route('/')
def index():
    return render_template('index.html', page='index')


@app.route("/test")
def test():
    return render_template('test.html', page='test')

# Route to label images and update JSON file
@app.route('/train_label', methods=['POST'])
def label_images():
    label = request.form['label']
    image_path = request.form['image_path']
    labeled_images = load_labeled_images()  # Load labeled images from JSON

    # Move image if not already labeled
    if image_path not in labeled_images:
        if label == 'good':
            shutil.move(image_path, label_good_dir)
        elif label == 'bad':
            shutil.move(image_path, label_bad_dir)

        # Update JSON file with labeled image
        labeled_images.append(image_path)
        with open('labeled_images.json', 'w') as file:
            json.dump(labeled_images, file)

    return 'Image labeled successfully!'


# route to label images and update JSON file for test
@app.route('/test_label', methods=['POST'])
def label_test_images():
    label = request.form['label']
    image_path = request.form['image_path']
    labeled_images = load_labeled_images()
    
    # Move image if not already labeled
    if image_path not in labeled_images:
        if label == 'good':
            shutil.move(image_path, evaluation_good_dir)
        elif label == 'bad':
            shutil.move(image_path, evaluation_bad_dir)

        # Update JSON file with labeled image
        labeled_images.append(image_path)
        with open('labeled_images.json', 'w') as file:
            json.dump(labeled_images, file)
            

@app.route('/get_images')
def get_images():
  labeled_images = load_labeled_images()  # Load labeled images from JSON

  images_and_usernames = [(image, get_username(image)) for image in load_images(train_image_dir) if image not in labeled_images]
  
  random.shuffle(images_and_usernames)  
  return render_template('image_template.html', images=images_and_usernames)

@app.route('/random_image')
def random_image():
    labeled_images = load_labeled_images()
    images = load_images(test_image_dir)
    random.shuffle(images)
    
    for image in images:
        if image not in labeled_images:
            prediction = round((predict_image_class(image) * 100),2);
            response_data = {'image': image, 'prediction': prediction}
            return render_template('random_image_template.html', data=response_data)    
    
        

@app.route('/training/<path:filename>')
def serve_training_images(filename):
    response = make_response(send_from_directory(training_folder, filename));
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache for 1 day
    return response

@app.route('/get_counts')
def get_counts():
    labeled_images = load_labeled_images()  # Load labeled images from JSON
    # Get count of good and bad images, read each folder and count files
    good_count = len(os.listdir(label_good_dir))
    bad_count = len(os.listdir(label_bad_dir))
    
    counts = {'good': good_count, 'bad': bad_count}
    
    
    return render_template('count_template.html', counts=counts)

if __name__ == '__main__':
    app.run(debug=True)
