def create_directories():
    from extra.dir import create_directory

    model_dir = 'model'
    training_folder = 'training'
    models_dir = 'model/image_model'
    test_image_dir = 'training/test'
    train_image_dir = 'training/train'
    label_image_dir = 'model/labeled'
    evaluation_image_dir = 'model/evaluation'
    evaluation_good_dir = 'model/evaluation/good'
    evaluation_bad_dir = 'model/evaluation/bad'
    label_good_dir = 'model/labeled/good'
    label_bad_dir = 'model/labeled/bad'
    usr_upload_dir = 'model/user_upload'

    dirs = [
        model_dir,
        training_folder,
        models_dir,
        test_image_dir,
        train_image_dir,
        label_image_dir,
        evaluation_image_dir,
        evaluation_good_dir,
        evaluation_bad_dir,
        label_good_dir,
        label_bad_dir,
        usr_upload_dir
    ]

    for dir in dirs:
        create_directory(dir)

if __name__ == "__main__":
    create_directories()