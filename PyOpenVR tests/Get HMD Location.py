import openvr
from sys import stdout
from time import sleep
import pprint

poses = []
pp = pprint.PrettyPrinter(indent=4)
openvr.init(openvr.VRApplication_Background)

while True:
    poses = openvr.VRSystem().getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, poses)
    hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
    absolute_hmd_pose = hmd_pose.mDeviceToAbsoluteTracking

    hmd_pos = [
        absolute_hmd_pose[0][3], 
        absolute_hmd_pose[1][3], 
        absolute_hmd_pose[2][3]
    ]

    pp.pprint(hmd_pos)

    stdout.flush()
    sleep(.5)