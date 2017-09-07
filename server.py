import flask
import cv2
import numpy as np
from flask import request
import json
import base64
import time
import reidAPIs
import model
app = flask.Flask(__name__)

app.jinja_env.variable_start_string = '<<:'
app.jinja_env.variable_end_string = ':>>'

video = cv2.VideoCapture("init.mp4")

@app.route('/',methods=['GET'])
def index():
    return flask.render_template('index.html')
@app.route("/oldsave",methods = ["POST"])
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

    response = flask.make_response(json.dumps({
        "prob":[[0,1]]
    }))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/render/trackbar",methods=['POST'])
def render_request():
    print("/render/trackbar -- reqquset data:===")
    print(request.get_data())
    postData = eval(request.get_data())
    # find apperance
    data = reidAPIs.renderTrackbar(postData["find"])
    bboxes = reidAPIs.renderVideo(postData["find"])
    js_bboxes = []
    i = 0
    for bbox in bboxes:
        js_bbox = {
                "id":bbox[5],
                "time":bbox[4],
                "style":{
                  "left":str(bbox[1]) + "px",
                  "top":str(bbox[0]) + "px",
                  "width":str(bbox[3] - bbox[1]) + "px",
                  "height":str(bbox[2] - bbox[0]) + "px",
                  "borderColor":"hsla(0, 100%, 78%, 0.78)"
                },
                "infoStyle":{
                  "left":str(bbox[1]) + "px",
                  "top":str(bbox[2] + 6) + "px",
                  "width":str(bbox[3] - bbox[1]) + "px",
                  "backgroundColor":"hsla(0, 100%, 78%, 0.78)",
                }
              }
        js_bboxes.append(js_bbox)
        i += 1
    response = flask.make_response(json.dumps({"prob":data,"bboxes":js_bboxes}))

    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/api/bboxes", methods=['POST'])
def get_bboxes():
    postData = eval(request.get_data())
    # find apperance
    data = reidAPIs.saveBboxes(postData["bboxes"])
    response = flask.make_response(json.dumps({}))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0')
    # model.build_model()
