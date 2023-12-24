from PIL import ImageEnhance, Image

def enhance_image(image_path):
    # Open the generated image
    image = Image.open(image_path)
    
    # Apply enhancement (e.g., sharpness, brightness, contrast)
    enhancer = ImageEnhance.Contrast(image)
    enhanced_image = enhancer.enhance(1.5)  # Adjust enhancement factor as needed
    
    # Save the enhanced image
    enhanced_image_path = 'static/images/enhanced_graph.png'
    enhanced_image.save(enhanced_image_path)
    
    return enhanced_image_path