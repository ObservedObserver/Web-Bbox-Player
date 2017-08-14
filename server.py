import flask
import cv2
import numpy as np
from flask import request
import json
import base64
import time

app = flask.Flask(__name__)
video = cv2.VideoCapture("init.mp4")

@app.route('/',methods=['POST'])
def video_frame():
    fid = int(request.values.get("fid"))
    video.set(cv2.CAP_PROP_POS_FRAMES,fid)
    # response = flask.make_response(json_du)
    # response = flask.make_response("/var/www/html/frame/p-v-"+str(fid)+".jpg")
    # response.headers["Access-Control-Allow-Origin"] = "*"
    _, frame = video.read()
    time1 = time.time()
    cv2.imwrite("/var/www/html/frame/p-v-"+str(fid)+".jpg", frame)
    time2 = time.time()
    print(time1 - time2)
    f = open("/var/www/html/frame/p-v-"+str(fid)+".jpg","rb")
    frame_str = base64.b64encode(f.read())
    print(frame_str[:3])
    f.close()
    response = flask.make_response(json.dumps({
        "img":frame_str
    }))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
@app.route("/save",methods = ["POST"])
def save_images():
    print("***"*10)
    print(request)
    print(eval(request.get_data()))
    print("***"*10)
    data = eval(request.get_data())
    images = data.get("images")
    #
    scale = float(data.get("scale"))
    #
    currentTime = float(data.get("currentTime"))
    video.set(cv2.CAP_PROP_POS_MSEC, currentTime)
    _, frame = video.read()

    for image in images:
        print(image["x"])
        print("###"*3)
        image["x"] = image["x"] * scale
        image["y"] = image["y"] * scale
        image["width"] = image["width"] * scale
        image["height"] = image["height"] * scale
        print(frame)
        # cv2.imshow("tmp"+str(image["x"]),frame[image["y"]:image["y"]+image["height"],image["x"],image["x"]+image["width"]])

    response = flask.make_response("success")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True)
