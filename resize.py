from PIL import Image
import os

# Define the directory where your screenshots are stored
input_dir = 'data/images'

# Define the output directory for resized images
output_dir = 'training/images'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define the target size for resizing
target_width = 200  # Change this to your desired width
target_height = 150  # Change this to your desired height

# Loop through all images in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".png") or filename.endswith(".jpg"):  # Check for image files
        img_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Check if the output file already exists
        if os.path.exists(output_path):
            print("File " + filename + " already exists, skipping.")
            continue
        
        img = Image.open(img_path)

        # Resize the image while maintaining aspect ratio
        resized_img = img.resize((target_width, target_height), resample=Image.ANTIALIAS)

        # Save the resized image to the output directory
        resized_img.save(output_path)
        print("Resized " + filename + " to " + str(target_width) + "x" + str(target_height))

print("Resizing complete!")