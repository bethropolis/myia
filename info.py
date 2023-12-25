import json
import os
import time

def get_directory_info(directory_path, labels):
    
    info = {
        'path': directory_path,
        'no_images': len(os.listdir(directory_path)),
        'date_modified': time.ctime(os.path.getmtime(directory_path)),
        'labels': {}
    }

    for label in labels:
        label_dir = os.path.join(directory_path, label)
        info['labels'][label] = {
            'path': label_dir,
            'no_images': len(os.listdir(label_dir)),
            'date_modified': time.ctime(os.path.getmtime(label_dir))
        }

    return info

def get_model_info(model_dir):
    models = []
    for root, dirs, files in os.walk(model_dir):
        for file in files:
            if file.lower().endswith(('.keras', '.h5')):
                model_path = os.path.join(root, file)
                models.append({
                    'name': file,
                    'size': os.path.getsize(model_path),
                    'evaluation': get_model_evaluation(file) 
                })

    return {
        'no_models': len(models),
        'path': model_dir,
        'data': models
    }
    
    
def get_model_evaluation(model_name):

    # Load evaluation results from the JSON file
    with open('model/model_evaluations.json', 'r', encoding="utf-8") as f:
        data = json.load(f)

    if model_name in data:
        return data[model_name]
    else:
        return {
            'accuracy_good': 0.0,
            'accuracy_bad': 0.0,
            'loss_good': 0.0,
            'loss_bad': 0.0,
            'graph_path': ''
        }