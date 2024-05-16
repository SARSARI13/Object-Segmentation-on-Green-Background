import os
import sys
import cv2
import numpy as np
import rembg

def load_images_from_folder(folder_path):
    images = []
    for file in os.listdir(folder_path):
        image_path = os.path.join(folder_path, file)
        if is_image_extension(file):
            images.append(image_path)
    return images

def is_image_extension(file_name):
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    return file_name.lower().endswith(image_extensions)

def remove_background(image):
    try:
        # Load the image using OpenCV
        image_cv = cv2.imread(image)
        
        # Convert the image to a numpy array
        image_np = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)

        # Apply background removal using rembg
        masked_image = rembg.remove(image_np)

        return masked_image
    except Exception as e:
        print(f"Error processing {image}: {str(e)}")
        return None

def save_binary_mask(mask, output_path):
    # Convert the mask to grayscale
    gray_mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)

    # Apply a threshold to get a binary mask (black and white)
    _, binary_mask = cv2.threshold(gray_mask, 1, 255, cv2.THRESH_BINARY)

    # Save the binary mask in JPEG format
    cv2.imwrite(output_path, binary_mask)

def main(image_folder_path):
    images = load_images_from_folder(image_folder_path)

    if not images:
        print(f"No images found in the folder {image_folder_path}.")
        return

    for image in images:
        mask = remove_background(image)
        if mask is not None:
            output_path = os.path.splitext(image)[0] + '_mask.jpg'
            save_binary_mask(mask, output_path)
            print(f"Processing {image} completed. Binary mask saved at {output_path}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Main.py /path/to/image_folder")
        sys.exit(1)

    image_folder_path = sys.argv[1]
    main(image_folder_path)
