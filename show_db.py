#!/usr/bin/env python3
import os
import cv2

def show_database(path):
        # Path to the folder containing your images
        image_folder = path

        # Get a list of image files in the folder
        image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        # Create a window to display the images
        cv2.namedWindow('Images in data base', cv2.WINDOW_NORMAL)

        # Loop through the image files and display them in the same window
        for image_file in image_files:
            image_path = os.path.join(image_folder, image_file)
            img = cv2.imread(image_path)
            h, w, _ = img.shape
            # Get the filename only from the initial file path.
            basename = os.path.basename(image_path)
            (filename, _) = os.path.splitext(basename)
            x = int(h*0.1)
            y = int(w*0.1)
            size = int(0.01*w)
            cv2.putText(img, str(filename), (x, h-y), cv2.FONT_HERSHEY_SIMPLEX, size, (255, 255, 255), size)

            if img is not None:
                # Display the image
                cv2.imshow('Images in data base', img)

                # Wait for a key press or a specified delay (0 means indefinite)
                key = cv2.waitKey(10)
