from pal.products.qcar import QCar,QCarCameras
from pal.utilities.math import *

import Setup as Setup
from tensorflow import keras

from tensorflow.keras.models import load_model
import time
import numpy as np
import cv2
model = load_model('applications\MyApplications\keras_150epoch_trained_UnifiedImageData.keras')

start_time = time.time()
def elapsed_time():
    return time.time() - start_time

Setup.setup()
qcar = QCar(frequency=200)
cameras = QCarCameras(enableFront=True)

steering = 0


#while(elapsed_time()<simulationTime):
while(True):  
    cameras.readAll()
    imageDataFront = cameras.csiFront.imageData[200:,]
    image = cv2.resize(imageDataFront, (200, 66))
    # hsvBuf = cv2.cvtColor(imageDataFront, cv2.COLOR_BGR2HSV)
    # canny = cv2.Canny(hsvBuf, 100, 200)
    # binaryImage = ImageProcessing.binary_thresholding(frame= hsvBuf,
	# 	 							lowerBounds=np.array([10, 0, 0]),
	# 	 							upperBounds=np.array([45, 255, 255]))
    
    
    image3 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) / 255.0
    image4 = np.expand_dims(image3, axis=0)  # Add batch dimension
    predicted_angle = model.predict(image4)

    steering = predicted_angle[0][0]
    qcar.write(0.045,steering)
    
    
    cv2.imshow("Actual Image", imageDataFront)

    cv2.waitKey(1)