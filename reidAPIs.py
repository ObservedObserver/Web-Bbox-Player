#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import random
import numpy as np
import cv2
import sys
sys.path.append('../personDetection')
import model
import os

sess,  node, gallery_path, testDeal, gpu_now = model.build_model()
#if os.path.isfile(gallery_path):
#    with open(gallery_path, 'wb') as f:
#        gallery = json.load(f)
#else:
gallery = {}
VIDEO_PATH = "./static/videos/p2.mp4"
video = cv2.VideoCapture(VIDEO_PATH)
# 渲染进度条，用于制作某个ID在整个视频中出现的概率，这里的只用将每一帧(fps可自定)
# 参数 find 为一个list，包含若干字符串，为需要查询的bbox的ID
# 返回一个list(bbox_num,frame_num)，为每一个人在每一帧出现的概率，范围[0,1]
def renderTrackbar(find):
    print("[renderTrackbar]Picked are:",find)
    ans = []
     # 从数据库中获取每一帧的分析结果，并记录下find-list中每一个人的出现概率
    for i in range(0, len(find)):
        ans.append([])
        for j in range(0,100):
            ans[i].append([j,0])
    video = cv2.VideoCapture(VIDEO_PATH)
    success, image = video.read()
    j = 0
    while(success):
        detect_result = model.detect_reid(sess, image, gallery, testDeal, node,
                                          save_path=None)
        for detect_data in detect_result:
            ans[find.index(detect_data["id"])][j][1] = int(detect_data["prob"]*100)
        j = j + 1
        success, image = video.read()
    return ans


# 渲染视频，用于将所要查询的bbox在视频中的某一时刻出现的查询目标框出来，并返回框出的bbox信息
# 需要注意的是，这里采用的是出现的时间而非帧号,时间单位为秒
# 参数 find 为一个list，包含若干字符串，为需要查询的bbox的ID
# 返回一个list(bbox_num,6)，每一行为[y0,x0,y1,x1,time,ID]
def renderVideo(find):
    print("[renderVideo]Picked are:",find)
    video_length = video.get(video, cv2.CAP_PROP_FRAME_COUNT) / video.get(video, cv2.CAP_PROP_FPS)#90 #s
    video_length = video_length * 10 #fake frame
    resp_bboxes = []
    for i in range(video_length):
        video.set(cv2.CAP_PROP_POS_MSEC, i)
        success, image = video.read()
        detect_results = model.detect_reid(sess, image, gallery, testDeal, node)
        for detect_result in detect_results:
            _tmp = [detect_result["bbx"][0],detect_result["bbx"][1],
            detect_result["bbx"][2],detect_result["bbx"][3],
            i/10.0,
            detect_result["id"]]
            if detect_result["id"] in find:
                resp_bboxes.append(_tmp)

    return resp_bboxes

def renderImage(find, tim):
    print("[renderImage]Picked are:",find)
    video.set(cv2.CAP_PROP_POS_MSEC, tim)
    success, image = video.read()
    detect_results = model.detect_reid(sess, image, gallery, testDeal, node)
    for detect_result in detect_results:
        _tmp = [detect_result["bbx"][0],detect_result["bbx"][1],
        detect_result["bbx"][2],detect_result["bbx"][3],
        i/10.0,
        detect_result["id"]]
        if detect_result["id"] in find:
            resp_bboxes.append(_tmp)

    return resp_bboxes


# 处理并保存由用户画出的bbox，这里做提取特征并导入数据库的操作
# 参数 _bboxes 为画出的bbox字典，在这部分中，会将_bboxes先转化为bboxes numpy数组，而每个bbox的ID也会被存储在bboxesID中
# 该函数不严格要求返回值，但建议可以返回某些标识符用于代码的调试
def saveBboxes(_bboxes):
    print("[saveBboxes]_bboxes are:",_bboxes)
    _bboxes_list = []
    bboxesID = []
    for _bbox in _bboxes:
        _bboxes_list.append(list(_bbox["data"].values()))
        bboxesID.append(_bbox["id"])
    bboxes = np.array(_bboxes_list)
    bboxes = bboxes / float(_bboxes[0]["scale"])
    inputs = []
    i = 0
    for bbox in bboxes:
        t = float(_bboxes[i]["time"])
        print(t)
        video.set(cv2.CAP_PROP_POS_MSEC, int(t*1000))
        print("time--",video.get(cv2.CAP_PROP_POS_MSEC))
        success, image = video.read()
        print(success)
        inputs.append(image[bbox[0]:bbox[2],bbox[1]:bbox[3]])
        # inputs.append(image)
        i = i + 1
    # 在这里，已经获得可以使用的bboxes(np array,[N,4])与bboxesID(list)
    res_vec = model.getGallery(sess, inputs, bboxesID, gallery_path, node)
    # print(bboxes)
    # print(bboxesID)
    print("[getGallery] return:", res_vec)
    ans = []
    for i in range(len(bboxes)):
        tmp = {}
        tmp["time"] = _bboxes[i]["time"]
        tmp["id"] = bboxesID[i]
        tmp["image"] = inputs[i].tolist()
        ans.append(tmp)
    with open("bboxes.json","w+") as f:
        f.write(json.dumps(ans))
        print("[saveBboxes]:Data writen into DB(json file).")

if __name__ == "__main__":
    print(renderVideo([1,2,3]))
