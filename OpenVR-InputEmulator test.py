# ====================
#        Import       
# ====================
import os

# ====================
#         Föll        
# ====================
def cmd(command):
    if type(command) is list:
        for singleCommand in command:
            output = os.popen(singleCommand).read()
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

def createVirtualTracker(name, path_to_client_commandline):
    # Create virtual controller
    createCommandReturn = cmd(path_to_client_commandline+"client_commandline.exe addcontroller "+name) # Writes virtual device id to stdout
    
    # Tékka hvort að returnið úr skipuninni fyrir ofan sé tala, ef ekki breakar þetta
    try:
        trackerID = int(createCommandReturn)
        print("trackerID:", trackerID)
    except ValueError:
        print("ERROR, faled at creating controller:", createCommandReturn)
        return None

    # Set device properties
    commands = [
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1000 string lighthouse',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1001 string "Vive Controller MV"',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1003 string vr_controller_vive_1_5',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1004 bool 0',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1005 string HTC',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1006 string "1465809478 htcvrsoftware@firmware-win32 2016-06-13 FPGA 1.6/0/0 VRC 1465809477 Radio 1466630404"',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1007 string "product 129 rev 1.5.0 lot 2000/0/0 0"',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1010 bool 1',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1017 uint64 2164327680',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1018 uint64 1465809478',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 1029 int32 2',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3001 uint64 12884901895',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3002 int32 1',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3003 int32 3',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3004 int32 0',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3005 int32 0',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3006 int32 0',
        path_to_client_commandline+'client_commandline.exe setdeviceproperty '+str(trackerID)+' 3007 int32 0',
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
        path_to_client_commandline+'client_commandline.exe setdeviceposition '+str(trackerID)+' -1 -1 -1'
    ]

    cmd(commands)

    return trackerID

# ====================
#         Kóði        
# ====================
trackerID = createVirtualTracker("controller02", "client-commandline\\")

print("Keeping controller connected")

positions = [
    [-1, -1, -1], 
    [-1.10, -1, -1], 
    [-1.20, -1, -1], 
    [-1.30, -1, -1], 
    [-1.40, -1, -1], 
    [-1.50, -1, -1], 
    [-1.40, -1, -1], 
    [-1.30, -1, -1], 
    [-1.20, -1, -1], 
    [-1.10, -1, -1], 
    [-1, -1, -1]
]

while True:
    for pos in positions:
        print(cmd("client-commandline\\client_commandline.exe setdeviceposition "+str(trackerID)+" "+str(pos[0])+" "+str(pos[1])+" "+str(pos[2])))

print("Done")