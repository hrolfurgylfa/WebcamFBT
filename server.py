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
    print("Reciving pose")


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
