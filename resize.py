from PIL import Image
import os

# Define the directory where your screenshots are stored
input_dir = 'data/images'

# Define the output directory for resized images
output_dir = 'training/images'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define the target size for resizing
target_size = (200, 150) # Change this to your desired width and height



def resize_image(input_dir, output_dir, filename, target_size, overwrite=False):
   img_path = os.path.join(input_dir, filename)
   output_path = os.path.join(output_dir, filename)
   
   # Check if the output file already exists
   if os.path.exists(output_path) and not overwrite:
       print("File " + filename + " already exists, skipping.")
       return
   
   img = Image.open(img_path)
   
   img = img.convert('RGBA') # Convert to RGB if necessary

   # Resize the image while maintaining aspect ratio
   resized_img = img.resize(target_size, resample=Image.ANTIALIAS)

   # Save the resized image to the output directory
   resized_img.save(output_path)
   
   

if __name__ == "__main__":
    for filename in os.listdir(input_dir):
        if filename.endswith(".png") or filename.endswith(".jpg"): # Check for image files
            resize_image(input_dir, output_dir, filename, target_size)
       
       
print("Resizing complete!")