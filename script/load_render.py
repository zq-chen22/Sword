
import os
import cv2
import numpy as np

def process_images_with_blur_and_resize(source_folder, target_folder):
    # Ensure the target folder exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Traverse through all subfolders and files in the source folder
    for root, dirs, files in os.walk(source_folder):
        # if not root.endswith("move"):
        #     continue
        for file in files:
            if file.endswith('.png'):
                # Get the source subfolder and create a corresponding target subfolder
                subfolder = os.path.relpath(root, source_folder)
                target_subfolder = os.path.join(target_folder, subfolder)
                if not os.path.exists(target_subfolder):
                    os.makedirs(target_subfolder)

                # Read the image
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path)

                if img is not None:
                    # Apply Gaussian blur
                    blurred_img = cv2.GaussianBlur(img, (3, 3), 0)


                    # Convert to BGRA
                    blurred_img = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2BGRA)

                    # Set light-colored pixels to transparent
                    blurred_img[:, :, 3] = np.clip(np.sum(255 - blurred_img[:, :, :3], axis=-1)*2//3, 140, 395) - 140
                    # for y in range(blurred_img.shape[0]):
                    #     for x in range(blurred_img.shape[1]):
                    #         r, g, b, a = blurred_img[y, x]
                    #         if r > 200 and g > 200 and b > 200:
                    #             blurred_img[y, x] = [r, g, b, 0]  # Set alpha to 0

                    # Resize the image to one-fifth of its original size
                    height, width = blurred_img.shape[:2]
                    new_height, new_width = height // 3, width // 3
                    resized_img = cv2.resize(blurred_img, (new_width, new_height))

                    # Save the processed image to the target subfolder
                    output_path = os.path.join(target_subfolder, file)
                    cv2.imwrite(output_path, resized_img)

                    print(f"Processed and saved: {output_path}")
                else:
                    print(f"Failed to read image: {img_path}")

    print("Finished processing all images.")

# Define source and target folders
source_folder = '/home/zifan/Videos/sword_blue'   # Replace 'a' with the path to your source folder
target_folder = 'render/HunGuangZongBlue'  # Replace 'b' with the path to your target folder

# Process images
process_images_with_blur_and_resize(source_folder, target_folder)