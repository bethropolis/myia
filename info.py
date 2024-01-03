import json
import os
import re
import time
from extra.dir import create_directory
from pathlib import Path


def get_directory_info(directory_path, labels):
    
    create_directory(directory_path);
    
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
                    'evaluation': get_model_evaluation(file), 
                    'path': model_path
                })

    # Sort the models 
    models = sorted(models, key=lambda model: [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', model['name'])])

    return {
        'no_models': len(models),
        'path': model_dir,
        'data': models
    }
    
    


def get_model_evaluation(model_name):
    file_path = Path('model/model_evaluations.json')

    if file_path.exists():
        with file_path.open('r', encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "accuracy_good": 0.0,
            "accuracy_bad": 0.0,
            "loss_good": 0.0,
            "loss_bad": 0.0,
            "average_accuracy": 0.0,
            "average_loss": 0.0,
            "graph_path": "",
            "static_path": ""
        }

    return data.get(model_name, data)
