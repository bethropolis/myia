from flask import Flask, config, render_template, request, jsonify, send_from_directory, make_response
from extra.random import random_string
from info import get_directory_info, get_model_info
from predict import predict_image_class
from resize import resize_image
from validation import evaluate_and_visualize_model
import os
import shutil
import json
import random


app = Flask(__name__)

model_dir = 'model'
training_folder = 'training'   
models_dir = 'model/image_model'
test_image_dir = 'training/images'
train_image_dir = 'training/train'
label_image_dir = 'model/labeled'
evaluation_image_dir = 'model/evaluation'

evaluation_good_dir = 'model/evaluation/good'
evaluation_bad_dir = 'model/evaluation/bad'
label_good_dir = 'model/labeled/good'
label_bad_dir = 'model/labeled/bad'
usr_upload_dir = 'model/user_upload'

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

        
# check if file exists
def file_exists(file):
    return os.path.exists(file)
    
def get_models():
    models = []
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            if file.lower().endswith(('.keras', '.h5')):
                models.append(file)
    return models
     
# Function to load labeled images from JSON file
def load_labeled_images():
    labeled_images = []
    json_file = 'model/labeled_images.json'
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding="utf-8") as file:
            labeled_images = json.load(file)
    return labeled_images

# Route to send images to frontend
@app.route('/')
def index():
    return render_template('home.html', page='index')

@app.route('/train')
def train():
    return render_template('train.html', page='train')

@app.route("/test")
def test():
    models = get_models()
    return render_template('test.html', page='test' , models=models)

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
        with open('model/labeled_images.json', 'w', encoding="utf-8") as file:
            json.dump(labeled_images, file)

    return 'Image labeled successfully!'



# Route to fetch home data
@app.route('/home_data')
def get_home_data():
    directories = {
        'training': get_directory_info(train_image_dir, []),
        'test': get_directory_info(test_image_dir, []),
        'evaluation': get_directory_info(evaluation_image_dir, ['good', 'bad']),
        'labeled': get_directory_info(label_image_dir, ['good', 'bad']),
    }

    models = get_model_info(models_dir)
    
    data ={
        'directories': directories,
        'models': models
    }
    
    return render_template('home_data.html', data=data)
    
    
# route to label images and update JSON file for test
@app.route('/test_label', methods=['POST'])
def label_test_images():
    label = request.form['label']
    image_path = request.form['image_path']
    prediction = request.form['prediction']
    labeled_images = load_labeled_images()
    
    # Move image if not already labeled
    if image_path not in labeled_images:
        if label == 'good':
            if float(prediction) >= 50:
                shutil.move(image_path, evaluation_good_dir)
                result_label = 'good'
            else:
                shutil.move(image_path, evaluation_bad_dir)
                result_label = 'bad'
        elif label == 'bad':
            if float(prediction) >= 50:
                shutil.move(image_path, evaluation_bad_dir)
                result_label = 'bad'    
            else:
                shutil.move(image_path, evaluation_good_dir)
                result_label = 'good'

        labeled_images.append(image_path)
        with open('model/labeled_images.json', 'w', encoding='utf-8') as file:
            json.dump(labeled_images, file)
        
        return f"Image labeled as {result_label}!"
            

# Route to upload image
@app.route('/upload', methods=['POST'])
async def upload_image():
    path_type = request.args.get('type', default = "user_upload", type = str)
    image = request.files['image']
    
    list_of_path_type = {
        "test": test_image_dir,
        "train": train_image_dir,
        "user_upload": usr_upload_dir
    }
    
    if path_type not in list_of_path_type:
        return jsonify(error="Invalid path type"), 400
    
    storage_path = list_of_path_type.get(path_type) or test_image_dir
    
    # allow only images type png, jpg
    if image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        file_name = "user_upload_" + random_string() + ".png"  # Ensure PNG extension
        image_path = os.path.join(storage_path, file_name)

        try:
            image.save(image_path)  # Save as PNG
            resize_image(storage_path, storage_path, file_name, (200, 150), overwrite=True)

        except Exception as e:
            return jsonify(error=str(e)), 500
        
        return render_template('upload_image.html', image=image_path)
    else:
        return jsonify(error="Invalid image type"), 415
    
    


@app.route('/directory')
def directory():
    path = request.args.get('path', default = ".", type = str)
    
    if not os.path.commonpath([path]).startswith(os.path.commonpath([model_dir, training_folder])):
        return jsonify(error="Invalid path"), 400

    if not os.path.exists(path):
        return jsonify(error="Directory does not exist"), 404


    return render_template('directory.html', path=path)

# Route to get directory images
@app.route('/get_directory_images')
def get_directory_images():
    path = request.args.get('path', default = ".", type = str)
    offset = request.args.get('offset', default = 0, type = int)
    limit = request.args.get('limit', default = 50, type = int)

    if not os.path.commonpath([path]).startswith(os.path.commonpath([model_dir, training_folder])):
        return jsonify(error="Invalid path"), 400

    if not os.path.exists(path):
        return jsonify(error="Directory does not exist"), 404

    directories = [os.path.join(path, name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    images_and_titles = [(os.path.join(path, image), get_username(image)) for image in os.listdir(path) if image.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Apply offset and limit only to images
    images_and_titles = images_and_titles[offset : offset + limit]
    
    next_offset = offset + limit
    
    return render_template('image_card.html', path=path, directories=directories, images=images_and_titles, offset=next_offset)


# Route to delete an image
@app.route('/delete_image', methods=['POST'])
def delete_image():
    image_path = request.form['image_path']

    if not os.path.commonpath([image_path]).startswith(os.path.commonpath([model_dir, training_folder])):
        return jsonify(error="Invalid image path"), 400

    if not os.path.exists(image_path):
        return jsonify(error="Image does not exist"), 404

    try:
        os.remove(image_path)
    except Exception as e:
        return jsonify(error=str(e)), 500

    return 'Image deleted successfully!'


    
@app.route('/get_images')
def get_images():
    offset = request.args.get('offset', default = 0, type = int)
    limit = request.args.get('limit', default = 50, type = int)

    labeled_images = load_labeled_images()  # Load labeled images from JSON

    images_and_usernames = [(image, get_username(image)) for image in load_images(train_image_dir) if image not in labeled_images]

    # Apply offset and limit
    images_and_usernames = images_and_usernames[offset : offset + limit]
    
    next_offset = offset + limit
    
    return render_template('image_template.html', images=images_and_usernames, offset=next_offset)



@app.route('/random_image')
def random_image():
    models = get_models()
    choosen_model = request.args.get('model', default = models[0], type = str)
    passed_image = request.args.get('image', default = None, type = str)
    
    if not file_exists(os.path.join(models_dir, choosen_model)):
        return jsonify(error="Model does not exist"), 404
    
    
    
    model_path = os.path.join(models_dir, choosen_model)
    labeled_images = load_labeled_images()
    images = load_images(test_image_dir)
    random.shuffle(images)
    
    def get_random_image():
        for image in images:
            if image not in labeled_images:
                return image
            
    
    if passed_image is None:
        image = get_random_image()
    else:
        image = passed_image  
    
    prediction = round((predict_image_class(model_path, image) * 100),2)
    response_data = {'image': image, 'prediction': prediction}
    return render_template('random_image_template.html', data=response_data)     



# route to get available models
@app.route('/models')
def get_available_models():
    models = get_models()
    return jsonify(models)

   
# Route to get test validation of models
@app.route('/validation')
def test_validation():
    models = get_models()
    choosen_model = request.args.get('model', default = models[0], type = str)
    return render_template('validation.html', models=models, page='validation', choosen_model=choosen_model)

# route to get validation results
@app.route('/validation_results', methods=['POST'])
async def get_validation_results():
    model = request.form['model']
    model_path = os.path.join(models_dir, model) 
    temperature = request.form.get("temperature", 1.0)
    augmentation = request.form.get('augmentation', '')
    
    configs = {
        "temperature": temperature,
        "data_augmentation": augmentation == "on"
    }
    
    graph_image = evaluate_and_visualize_model(model_path, label_good_dir, label_bad_dir,model, configs)
    return render_template('validation_results.html', graph_image=graph_image, random_string=random_string)


@app.route('/training/<path:filename>')
def serve_training_images(filename):
    response = make_response(send_from_directory(training_folder, filename))
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache for 1 day
    return response

@app.route('/model/<path:filename>')
def serve_model_images(filename):
    response = make_response(send_from_directory(model_dir, filename))
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache for 1 day 
    return response


@app.route('/get_counts')
def get_counts():
    train_good_count = len(os.listdir(label_good_dir))
    train_bad_count = len(os.listdir(label_bad_dir))
    test_good_count = len(os.listdir(evaluation_good_dir))
    test_bad_count = len(os.listdir(evaluation_bad_dir))
    counts = {'train_good': train_good_count, 'train_bad': train_bad_count, 'test_good': test_good_count, 'test_bad': test_bad_count}
    return render_template('count_template.html', counts=counts)

if __name__ == '__main__': 
    app.run(debug=True) 
