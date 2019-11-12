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

# Sækja allskonar annað
import json
import urllib.request
from sys import argv
import time
import math


#  ========================================
#  Global breytur
#  ========================================

last_poses_per_second = 0
poses_this_second = 0
time_of_last_pose = 0


#  ========================================
#  Venjulegar routes
#  ========================================

@route("/")
def main():
    with open('index.html', 'r') as content_file:
        content = content_file.read()
    return content

@route("/data", method="POST")
def data():
    try: pose = json.loads(request.body.read())
    except Exception as error: print(error)

    # print("\nPose:")
    # print(pose)
    # print("Reciving pose")

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
    
    print("Poses per second:",last_poses_per_second)

    trackers = {}

    


#  ========================================
#  Static routes
#  ========================================

@route("/js/<slod:path>")
def static_js(slod):
    return static_file(slod, root="js", mimetype="text/javascript")

@route("/css/<slod:path>")
def static_css(slod):
    return static_file(slod, root="css")

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
#  Keyra bottle
#  ========================================

bottle.run(host="localhost", port=8080, reloader=True, debug=True)
