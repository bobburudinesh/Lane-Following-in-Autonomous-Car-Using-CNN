from pal.products.qcar import QCar,QCarCameras
from hal.utilities.image_processing import ImageProcessing
from pal.utilities.math import *
import Setup as Setup
import time
import numpy as np
import cv2
start_time = time.time()
def elapsed_time():
    return time.time() - start_time

sampleRate = 30.0
sampleTime = 1/sampleRate
simulationTime = 45.0
imageWidth = 640    
imageHeight = 480
#Setting Filter
steeringFilter = Filter().low_pass_first_order_variable(25, 0.033)
next(steeringFilter)
dt = 0.033
Setup.setup()
qcar = QCar(frequency=200)
cameras = QCarCameras(enableFront=True)

#while(elapsed_time()<simulationTime):
while(True):
    start = time.time()
    cameras.readAll()
    imageDataFront = cameras.csiFront.imageData
    imageDataFrontTest = cameras.csiFront.imageData[250:,:]
    hsvBuf = cv2.cvtColor(imageDataFront, cv2.COLOR_BGR2HSV)
    binaryImage = ImageProcessing.binary_thresholding(frame= hsvBuf,
		 							lowerBounds=np.array([10, 0, 0]),
		 							upperBounds=np.array([45, 255, 255]))
    slope, intercept = ImageProcessing.find_slope_intercept_from_binary(binary=binaryImage)
    rawSteering = 1.75*(slope - 0.3419) + (1/150)*(intercept+5)
    steering = steeringFilter.send((np.clip(rawSteering, -0.5, 0.5), dt))
    #print("Slope: " + str(slope) + "  InterCept: "+ str(intercept) + "  Steering: " + str(steering))
    cv2.imshow('Combined View', cv2.resize(binaryImage,
                                        (int(2*imageWidth),
                                        int(imageHeight/2))))
    cv2.waitKey(1)
    end = time.time()
    qcar.write(0.04*np.cos(steering),steering)
    dt = end - start
    