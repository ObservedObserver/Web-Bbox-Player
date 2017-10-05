import flask
import os
import cv2
import numpy as np
from flask import request
import json
import base64
import time
import reidAPIs
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
def render_trackebar():
    print("/render/trackbar -- reqquset data:===")
    print(request.get_data())
    postData = eval(request.get_data())
    scale = postData["scale"]
    # find apperance
    data = reidAPIs.renderTrackbar(postData["find"], postData["video_url"])
    response = flask.make_response(json.dumps({"prob":data}))

    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/render/package",methods=['POST'])
def render_package():
	print("/render/package -- request data:===")
	postData = eval(request.get_data())
	# print postData["find"]
	scale = postData["scale"]
	bash_bboxes = reidAPIs.renderPackage(postData["find"], int(1000*float(postData["start_time"])), postData["video_url"])
	js_bboxes = []
	for bboxes in bash_bboxes:
		js_bboxes.append([])
		for bbox in bboxes:
        	# bbox[0:3] /= scale
			for _pos in range(4):
				bbox[_pos] /= scale
			js_bbox = {
            	    "id":bbox[5],
               	 # "time":bbox[4],
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
			js_bboxes[-1].append(js_bbox)
	print("detected people info:", js_bboxes)
	response = flask.make_response(json.dumps({"hashBboxes":js_bboxes}))

	response.headers["Access-Control-Allow-Origin"] = "*"
	return response



@app.route("/render/request",methods=['POST'])
def render_request():
    print("/render/request -- reqquset data:===")
    print(request.get_data())
    postData = eval(request.get_data())
    scale = postData["scale"]
    # find apperance
    data = reidAPIs.renderTrackbar(postData["find"], postData["video_url"])
    bboxes = reidAPIs.renderVideo(postData["find"], postData["video_url"])
    js_bboxes = []
    i = 0
    for bbox in bboxes:
	# bbox[0:3] /= scale 
	for _pos in range(4):
        	bbox[_pos] /= scale

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
    print(postData["bboxes"])
    # find apperance
    data = reidAPIs.saveBboxes(postData["bboxes"], postData["video_url"])
    response = flask.make_response(json.dumps({}))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/render/image", methods=["POST"])
def render_image():
    print("[server.render_image].")
    postData = eval(request.get_data())
    print postData["find"]
    scale = postData["scale"]
    bboxes = reidAPIs.renderImage(postData["find"], 1000*float(postData["time"]), postData["video_url"])
    js_bboxes = []
    i = 0
    for bbox in bboxes:
	# bbox[0:3] /= scale
	for _pos in range(4):
		bbox[_pos] /= scale
        js_bbox = {
                "id":bbox[5],
                # "time":bbox[4],
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
    print("detected people info:", js_bboxes)
    response = flask.make_response(json.dumps({"bboxes":js_bboxes}))

    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
if __name__ == "__main__":
    # gallery_path = os.path.expanduser('/home/hantian/Reid/DATA/ourImage/gallery/gallery.json')
    #with open('/home/hantian/Reid/DATA/ourImage/gallery/gallery.json',"w") as f:
    #    f.write("")
    app.run(debug=True, use_reloader = False)
