from pal.products.qcar import QCar,QCarCameras
from pal.utilities.math import *
import Setup as Setup
import time
import numpy as np
import cv2
import os
import keyboard
import json
from PIL import Image
start_time = time.time()
def elapsed_time():
    return time.time() - start_time
Setup.setup()
qcar = QCar(frequency=200)
cameras = QCarCameras(enableFront=True)
countLoop = 0
manualSteering = 0
step = 0.005
def on_press_event(event):
    global manualSteering
    if event.name == "left" and manualSteering <= 0.4:
        manualSteering += step

    elif event.name == "right" and manualSteering >= -0.4:
        manualSteering -=step
    elif event.name == "up":
        manualSteering = 0
    
def on_press_event_left(event):
    global manualSteering
    if manualSteering <= 0.5:
        manualSteering += step
def on_press_event_right(event):
    global manualSteering
    if manualSteering >= -0.5:
        manualSteering -= step
def on_loop_break(event):
    global breakLoop
    breakLoop = 1
def on_release_event(event):
    global manualSteering
    manualSteering = 0

def save_image_for_training(image, save_folder, image_name):
    # Make sure save folder exists
    os.makedirs(save_folder, exist_ok=True)

    if not image_name.lower().endswith(('.jpg', '.jpeg')):
        image_name += '.jpg'  # Automatically append .jpg if missing
    
    
    # Full path to save the image
    save_path = os.path.join(save_folder, image_name)

    try:
        # Check if the image is in float64 and convert it
        if image.dtype != np.uint8:
            print(f"Original image dtype: {image.dtype}")
            # Clip float64 images to range [0, 1] then convert to uint8
            image = np.clip(image, 0, 1)  # Clip to [0, 1] to avoid overflow
            image = (image * 255).astype(np.uint8)
            print(f"Converted image dtype: {image.dtype}")
        
        # Ensure the image has 3 channels (RGB)
        if image.ndim == 3 and image.shape[2] == 3:
            # Convert from BGR (OpenCV format) to RGB (PIL format)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
        else:
            raise ValueError(f"Image must have 3 channels (RGB), but it has {image.shape[2]} channels")

        # Check if the file name ends with '.jpg' or '.jpeg'
        if not save_path.lower().endswith(('.jpg', '.jpeg')):
            raise ValueError("The file name must end with '.jpg' or '.jpeg'")

        # Save the image as JPEG
        #print(f"Saving image to: {save_path}")
        image.save(save_path, format='JPEG')
        
        # Confirm the file format by checking the saved file
        if not save_path.lower().endswith(('.jpg', '.jpeg')):
            print("Warning: Image may not have been saved as JPEG.")
        
        #print("Image saved successfully!")
        #return save_path

    except Exception as e:
        print(f"Error saving image: {e}")
        #return None

def append_steering_angle(file_path, angle):
    try:
        # Read the existing list from the file
        with open(file_path, 'r') as file:
            steering_angles = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, start with an empty list
        steering_angles = []

    # Append the new angle to the list
    steering_angles.append(angle)

    # Write the updated list back to the file
    with open(file_path, 'w') as file:
        json.dump(steering_angles, file)



steering_Angles = []
breakLoop = 0
steering = 0
unifiedCounter = 0

#while(elapsed_time()<simulationTime):
while(True): 
   # time.sleep(0.0001)
    #manualSteering = 0
    #keyboard.on_press(on_press_event)
    keyboard.on_press_key('enter', on_loop_break)
    keyboard.on_press_key('left', on_press_event_left)
    keyboard.on_press_key('right', on_press_event_right)
    keyboard.on_release_key('left',on_release_event)
    keyboard.on_release_key('right',on_release_event)
    
    if breakLoop:
        break
    
    cameras.readAll()
    imageDataFront = cameras.csiFront.imageData[200:,]
    image = cv2.resize(imageDataFront, (200, 66))

    save_image_for_training(image,r"D:\Masters\Fall2024\Independent Study 2\Bulk_ImageDataForV2\Unified_resized", str(unifiedCounter))
    save_image_for_training(imageDataFront,r"D:\Masters\Fall2024\Independent Study 2\Bulk_ImageDataForV2\Unified_ImageData", str(unifiedCounter))
    save_image_for_training(imageDataFront,r"D:\Masters\Fall2024\Independent Study 2\Bulk_ImageDataForV2\Image_Data10", str(countLoop))
    save_image_for_training(image,r"D:\Masters\Fall2024\Independent Study 2\Bulk_ImageDataForV2\Image_Data10_resized", str(countLoop))
    append_steering_angle(r"D:\Masters\Fall2024\Independent Study 2\Bulk_ImageDataForV2\Angles10.txt", manualSteering)
    append_steering_angle(r"D:\Masters\Fall2024\Independent Study 2\Bulk_ImageDataForV2\Unified_Angles.txt", manualSteering)


    steering_Angles.append(manualSteering)
    countLoop +=1
    unifiedCounter +=1
    hsv_image = cv2.cvtColor(imageDataFront, cv2.COLOR_BGR2HSV)

    qcar.write(0.06,manualSteering)
    
    cv2.imshow("Actual Image", imageDataFront)

    cv2.waitKey(1)
print(steering_Angles)
print(len(steering_Angles), countLoop, unifiedCounter)
    



