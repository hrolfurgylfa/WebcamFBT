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
from bottle import redirect

# Sækja Python openVR library
import openvr

# Sækja allskonar annað
import json
from json import dumps
import urllib.request
from sys import argv
from sys import stdout
import time
import math
import os


#  ========================================
#  Global breytur
#  ========================================

last_poses_per_second = 0
poses_this_second = 0
time_of_last_pose = 0

running = True

poses = []

path_to_client_commandline = "client-commandline\\"

x_offset = 0
y_offset = 0
x_multiplier = 1
y_multiplier = 1


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

def cmd(command):
    if type(command) is list:
        temp_command_file_name = "temp_commands.bat"

        all_commands = "@echo off\n\n"
        for singleCommand in command:
            if all_commands == "":
                all_commands = singleCommand
            else:
                all_commands = all_commands + "\n" + singleCommand
        
        with open(temp_command_file_name, "w") as temp_command_file:
            temp_command_file.write(all_commands)

        output = os.popen(temp_command_file_name).read()
        if output != "":
            print("ERROR, failed executing a command in a list: "+output)
    else:
        return os.popen(command).read()

def canBeInt(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def createVirtualTracker(name):
    # Búa til vertual trackerinn
    createCommandReturn = cmd(path_to_client_commandline+"client_commandline.exe addcontroller "+str(name))
    
    # Tékka hvort að returnið úr skipuninni fyrir ofan sé tala, ef ekki hættir þetta fall
    try:
        trackerID = int(createCommandReturn)
        print("trackerID for "+name+":", trackerID)
    except ValueError:
        print("ERROR, faled at creating tracker:", createCommandReturn)
        return None

    # Set device properties
    commands = [
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1000 string lighthouse',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1001 string "Vive Tracker PVT"',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1003 string vr_controller_vive_1_5',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1004 bool 0',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1005 string HTC',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1006 string "1465809478 htcvrsoftware@firmware-win32 2016-06-13 FPGA 1.6/0/0 VRC 1465809477 Radio 1466630404"',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1007 string "product 129 rev 1.5.0 lot 2000/0/0 0"',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1010 bool 1',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1017 uint64 2164327680',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1018 uint64 1465809478',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1029 int32 3',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3001 uint64 12884901895',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3002 int32 1',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3003 int32 3',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3004 int32 0',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3005 int32 0',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3006 int32 0',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 5000 string icons',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 5001 string {htc}controller_status_off.png',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 5002 string {htc}controller_status_searching.gif',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 5003 string {htc}controller_status_searching_alert.gif',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 5004 string {htc}controller_status_ready.png',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 5005 string {htc}controller_status_ready_alert.png',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 5006 string {htc}controller_status_error.png',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 5007 string {htc}controller_status_standby.png',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 5008 string {htc}controller_status_ready_low.png',
        # Let OpenVR know that there is a new device
        path_to_client_commandline+'client_commandline.exe publishdevice '+str(trackerID),
        # Connect the device
        path_to_client_commandline+'client_commandline.exe setdeviceconnection '+str(trackerID)+' 1',
        # Set the device position
        path_to_client_commandline+'client_commandline.exe setdeviceposition '+str(trackerID)+' 0 0 0'
    ]

    cmd(commands)

    return trackerID

def setTrackerLocation(tracker_id, x_in, y = 0, z = 0):
    if type(x_in) is list:
        pos_list = x_in
        x = pos_list[0]
        y = pos_list[1]
        z = pos_list[2]
    else:
        x = x_in

    output = cmd(path_to_client_commandline+'client_commandline.exe setdeviceposition '+str(tracker_id)+' '+str(x)+' '+str(y)+' '+str(z))
    if output != "": print(output)

def changeTrackerStatus(id, connected):
    if connected: status = 1
    else: status = 0

    output = cmd(path_to_client_commandline+'client_commandline.exe setdeviceconnection '+str(id)+' '+str(status))
    if output != "": print(output)

def map_num(number, range_start, range_end, new_range_start, new_range_end):
    return (number-range_start)/(range_end-range_start) * (new_range_end-new_range_start) + new_range_start

def calculate_x_part(part_x):
    mapped_body_part = map_num(part_x, 0, 1000, -1, 1)
    return (mapped_body_part * x_multiplier) + x_offset

def calculate_y_part(part_y):
    mapped_body_part = map_num(part_y, 0, 562.5, 1, 0)
    return (mapped_body_part * y_multiplier) + y_offset


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
    # print("Receiving data...")

    try: JSpose = json.loads(request.body.read())
    except Exception as error: print(error)

    # Go over the extra data in the JSpose
    try:
        for data in JSpose["extraData"]:
            if data["name"] == "xOffset":
                global x_offset
                x_offset = float(data["value"])
            elif data["name"] == "yOffset":
                global y_offset
                y_offset = float(data["value"])
            elif data["name"] == "xMultiplier":
                global x_multiplier
                x_multiplier = float(data["value"])
            elif data["name"] == "yMultiplier":
                global y_multiplier
                y_multiplier = float(data["value"])
    except KeyError:
        pass

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
    #  and apply positions
    #  ====================

    # print(rightControllerPos[0], "\t", rightControllerPos[0])
    # print(leftControllerPos[0], "\t", leftControllerPos[1])
    
    if JSpose["hip"]:
        setTrackerLocation(
            hip_virtual_tracker,
            calculate_x_part(JSpose["hip"]["x"]),
            calculate_y_part(JSpose["hip"]["y"]),
            hmdPos[2]
        )
    if JSpose["left_foot"]:
        setTrackerLocation(
            left_foot_virtual_tracker,
            calculate_x_part(JSpose["left_foot"]["x"]),
            calculate_y_part(JSpose["left_foot"]["y"]),
            hmdPos[2]
        )
    if JSpose["right_foot"]:
        setTrackerLocation(
            right_foot_virtual_tracker,
            calculate_x_part(JSpose["right_foot"]["x"]),
            calculate_y_part(JSpose["right_foot"]["y"]),
            hmdPos[2]
        )

    print_string = ""
    print_string += "RightController x: "+str(rightControllerPos[0])+"\ty: "+str(rightControllerPos[1])+"\n"
    print_string += "LeftController  x: "+str(leftControllerPos[0])+"\ty: "+str(leftControllerPos[1])+"\n"
    print_string += "\n"
    if JSpose["hip"]:
        print_string += "HipTracker       x: "+str(calculate_x_part(JSpose["hip"]["x"]))+"\ty: "+str(calculate_y_part(JSpose["hip"]["y"]))+"\n"
    if JSpose["right_foot"]:
        print_string += "RightFootTracker x: "+str(calculate_x_part(JSpose["right_foot"]["x"]))+"\ty: "+str(calculate_y_part(JSpose["right_foot"]["y"]))+"\n"
    if JSpose["left_foot"]:
        print_string += "LeftFootTracker  x: "+str(calculate_x_part(JSpose["left_foot"]["x"]))+"\ty: "+str(calculate_y_part(JSpose["left_foot"]["y"]))+"\n"
    print_string += "---------------------------------------------------------------"
    print(print_string)


    #  ====================
    #  Finish
    #  ====================

    stdout.flush()
    # print()
    
    # data = [hmdPos, rightControllerPos, leftControllerPos]
    # with open("static_json/SteamVRDevices.json", "w") as tempOutFile:
    #     json.dump(data, tempOutFile)

    # return redirect("static_json/SteamVRDevices.json")


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
print()

# Búa til trackers
right_foot_virtual_tracker = createVirtualTracker("right_foot_virtual_tracker")
left_foot_virtual_tracker = createVirtualTracker("left_foot_virtual_tracker")
hip_virtual_tracker = createVirtualTracker("hip_virtual_tracker")


#  ========================================
#  Keyra bottle
#  ========================================

print("\nStarting bottle")
bottle.run(host="localhost", port=8080, quiet=True)
print("\n")