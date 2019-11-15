#  ========================================
#  Imports
#  ========================================

# Sækja bottle og partana af bottle sem þarf
import bottle
from bottle import route
from bottle import error
from bottle import static_file
from bottle import response
from bottle import request
from json import dumps

# Sækja Python openVR library
import openvr

# Sækja allskonar annað
import json
import urllib.request
from sys import argv
from sys import stdout
import time
import math


#  ========================================
#  Global breytur
#  ========================================

last_poses_per_second = 0
poses_this_second = 0
time_of_last_pose = 0

running = True

poses = []


#  ========================================
#  Föll
#  ========================================

def getPosOfDevice(index):
    
    absolute_pose = poses[index].mDeviceToAbsoluteTracking

    pos = [
        absolute_pose[0][3], 
        absolute_pose[1][3], 
        absolute_pose[2][3]
    ]

    return pos

def getControllers(quiet=False):
    IVRSystem = openvr.IVRSystem()

    if not quiet: print("Searching for controllers...")

    rightController = None
    leftController = None

    # Keyrir í gegnum öll tækin tengd við OpenVR
    for index in range(0, openvr.k_unMaxTrackedDeviceCount):

        # Tækið er fjarstýring
        if IVRSystem.getTrackedDeviceClass(index) == openvr.TrackedDeviceClass_Controller:

            # Ef fjarstýringin sem er verið að lúppa yfir er hægri
            if IVRSystem.getControllerRoleForTrackedDeviceIndex(index) == openvr.TrackedControllerRole_RightHand:
                rightController = index
                if not quiet: print("Right controller found, ID:",rightController)
            # Ef fjarstýringin sem er verið að lúppa yfir er vinstri
            elif IVRSystem.getControllerRoleForTrackedDeviceIndex(index) == openvr.TrackedControllerRole_LeftHand:
                leftController = index
                if not quiet: print("Left controller found, ID:",leftController)
        
        # Stoppa ef það er búið að finna báðar fjarstýringarnar
        if rightController is not None and leftController is not None:
            break
    else:
        return None
    
    return (rightController, leftController)


#  ========================================
#  Venjulegar routes
#  ========================================

@route("/")
def main():
    print("\nServing website\n")
    with open('index.html', 'r') as content_file:
        content = content_file.read()
    return content

@route("/data", method="POST")
def data():
    print("Receiving data...")

    try: JSpose = json.loads(request.body.read())
    except Exception as error: print(error)

    # Telja hversu oft er verið að uppfæra
    global last_poses_per_second
    global poses_this_second
    global time_of_last_pose

    if math.floor(time.time()) == time_of_last_pose:
        poses_this_second += 1
    else:
        time_of_last_pose = math.floor(time.time())
        last_poses_per_second = poses_this_second
        poses_this_second = 0
    
    # print("Poses per second:",last_poses_per_second)


    #  ====================
    #  OpenVR
    #  ====================

    # Uppfæra staðsetningar fjastrýnga og 
    global poses
    poses = openvr.VRSystem().getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, poses)
    
    # HMD
    hmdPos = getPosOfDevice(openvr.k_unTrackedDeviceIndex_Hmd)
    # print(hmdPos)

    # Right controller
    rightControllerPos = getPosOfDevice(rightController)
    
    # Left controller
    leftControllerPos = getPosOfDevice(leftController)
    

    #  ====================
    #  Calculate diffrence 
    #  ====================

    print(rightControllerPos[0], "\t", rightControllerPos[0])
    print(leftControllerPos[0], "\t", leftControllerPos[1])


    #  ====================
    #  Finish
    #  ====================

    stdout.flush()
    print()
    
    data = [hmdPos, rightControllerPos, leftControllerPos]
    with open("static_json/SteamVRDevices.json", "w") as tempOutFile:
        json.dump(data, tempOutFile)

#  ========================================
#  Static routes
#  ========================================

@route("/js/<slod:path>")
def static_js(slod):
    return static_file(slod, root="js", mimetype="text/javascript")

@route("/css/<slod:path>")
def static_css(slod):
    return static_file(slod, root="css")

@route("/static_json/<slod:path>")
def static_json(slod):
    return static_file(slod, root="static_json")

@route("/test_images/<slod:path>")
def static_test_images(slod):
    return static_file(slod, root="test_images")


#  ========================================
#  Error síður
#  ========================================
@error(404)
def notFound(error):
    return '<h2 style="color:red;text-align: center;">Þessi síða finnst ekki</h2>'


#  ========================================
#  Get OpenVR ready
#  ========================================

print("Getting OpenVR ready")
openvr.init(openvr.VRApplication_Background)

# Sækja fjarstýringar
rightController, leftController = getControllers()


#  ========================================
#  Keyra bottle
#  ========================================

print("\nStarting bottle")
bottle.run(host="localhost", port=8080, quiet=True)
print("\n")