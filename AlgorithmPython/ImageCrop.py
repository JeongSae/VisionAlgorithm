import cv2
import numpy as np
from PIL import Image

# cropped_image = ImageCrop.Crop(original_image, crop_area)
def ImageCrop(original_image, crop_area):
    cv_image = np.array(original_image)
    
    # Define the crop area
    x, y, w, h = crop_area
    
    # Perform cropping
    cropped_image = cv_image[y:h, x:w]
    
    # Convert back to PIL Image
    cropped_image = Image.fromarray(cropped_image)
    
    return cropped_image