# region: package imports
import os
import numpy as np

from qvl.qlabs import QuanserInteractiveLabs
from qvl.qcar import QLabsQCar
from qvl.free_camera import QLabsFreeCamera
from qvl.real_time import QLabsRealTime
from qvl.environment_outdoors import QLabsEnvironmentOutdoors

# environment objects
from qvl.basic_shape import QLabsBasicShape
import pal.resources.rtmodels as rtmodels

cuberefX = -18.5
cuberefY = 35
cuberefZ = 1

#endregion

def setup(
        initialPosition=[-3, 11, 0.000],
        initialOrientation=[0, 0, np.pi],
        rtModel=rtmodels.QCAR
    ):

    # Try to connect to Qlabs
    os.system('cls')
    qlabs = QuanserInteractiveLabs()
    print("Connecting to QLabs...")
    try:
        qlabs.open("localhost")
        print("Connected to QLabs")
    except:
        print("Unable to connect to QLabs")
        quit()

    # Delete any previous QCar instances and stop any running spawn models
    qlabs.destroy_all_spawned_actors()
    QLabsRealTime().terminate_all_real_time_models()
    environment = QLabsEnvironmentOutdoors(qlabs)

    # environment.ID_ENVIRONMENT_OUTDOORS = 1001
    # environment.set_outdoor_lighting(1)

    environment.set_weather_preset(environment.SNOW)
    # region: QCar spawn description

    cube0 = QLabsBasicShape(qlabs)
    cube1 = QLabsBasicShape(qlabs)
    cube2 = QLabsBasicShape(qlabs)
    cube3 = QLabsBasicShape(qlabs)
    # cube0.spawn_id(actorNumber=0, location=[cuberefX, cuberefY, cuberefZ], rotation=[0,0,0], scale=[5,1,5], configuration=cube0.SHAPE_CUBE, waitForConfirmation=True)
    # cube1.spawn_id(actorNumber=1, location=[cuberefX+1, cuberefY, cuberefZ], rotation=[0,0,0], scale=[5,1,5], configuration=cube0.SHAPE_CUBE, waitForConfirmation=True)
    # cube2.spawn_id(actorNumber=2, location=[cuberefX+2, cuberefY, cuberefZ], rotation=[0,0,0], scale=[5,1,5], configuration=cube0.SHAPE_CUBE, waitForConfirmation=True)
    # cube3.spawn_id(actorNumber=3, location=[cuberefX+3, cuberefY, cuberefZ], rotation=[0,0,0], scale=[5,1,5], configuration=cube0.SHAPE_CUBE, waitForConfirmation=True)
    
    #Spawn a QCar at the given initial pose
    hqcar = QLabsQCar(qlabs)
    hqcar.spawn_id(
        actorNumber=0,
        location=[x for x in initialPosition],
        rotation=initialOrientation,
        waitForConfirmation=True
    )

    # Create a new camera view and attach it to the QCar
    hcamera = QLabsFreeCamera(qlabs)
    hcamera.spawn([8.484, 1.973, 12.209], [-0, 0.748, 0.792])
    hqcar.possess()

    QLabsRealTime().start_real_time_model(rtModel)

    return hqcar


if __name__ == '__main__':
    # XXX Add processing of command line arguments
    setup()