from PIL import Image
import os


input_dir = 'data/images'

# Define the output directory for resized images
output_dir = 'training/images'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define the target size for resizing
target_size = (200, 150) # Change this to your desired width and height

def resize_single_image(img_path, output_path, target_size):
    img = Image.open(img_path)
    img = img.convert('RGBA') # Convert to RGB if necessary

    # Resize the image while maintaining aspect ratio
    resized_img = img.resize(target_size, resample=Image.LANCZOS)

    if output_path.endswith('.png'):   
        resized_img.save(output_path)
    else:
        resized_img.save(output_path, 'PNG')

def resize_image(input_dir, output_dir, filename, target_size, overwrite=False):
    img_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename)
   
    # Check if the output file already exists
    if os.path.exists(output_path) and not overwrite:
        print("File " + filename + " already exists, skipping.")
        return

    resize_single_image(img_path, output_path, target_size)

if __name__ == "__main__":
    for filename in os.listdir(input_dir):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            resize_image(input_dir, output_dir, filename, target_size, True)
    print("Resizing complete!")
