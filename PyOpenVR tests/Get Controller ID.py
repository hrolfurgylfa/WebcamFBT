import openvr
from sys import stdout

# Init kóði
poses = []
openvr.init(openvr.VRApplication_Background)


# Finna fjarstýringu
# for index in range(openvr.length):
# print(openvr.VRSystem().getTrackedDeviceClass(3))
print(openvr.IVRSystem().getStringTrackedDeviceProperty(1, 1000))

IVRSystem = openvr.IVRSystem()

print("Searching for controllers...")
# Keyrir í gegnum öll tækin tengd við OpenVR

rightController = None
leftController = None

for index in range(0, openvr.k_unMaxTrackedDeviceCount):

    # Tækið er fjarstýring
    if IVRSystem.getTrackedDeviceClass(index) == openvr.TrackedDeviceClass_Controller:
        print("ID:",index," Controller role:",IVRSystem.getControllerRoleForTrackedDeviceIndex(index))
        
        # Ef fjarstýringin sem er verið að lúppa yfir er hægri
        if IVRSystem.getControllerRoleForTrackedDeviceIndex(index) == openvr.TrackedControllerRole_RightHand:
            rightController = index
        # Ef fjarstýringin sem er verið að lúppa yfir er vinstri
        elif IVRSystem.getControllerRoleForTrackedDeviceIndex(index) == openvr.TrackedControllerRole_LeftHand:
            leftController = index
    
    # Stoppa ef það er búið að finna báðar fjarstýringarnar
    if rightController is not None and leftController is not None:
        break

print("rightControllerID:",rightController)
print("leftControllerID:",leftController)


# Þarf held ég að vera í lokin
stdout.flush()