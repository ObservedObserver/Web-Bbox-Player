#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import random
import numpy as np
import cv2
import model
sess, node = model.build_model()
VIDEO_PATH = "init.mp4"
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
        detect_result = model.detect_reid(sess, image, node["image_node"], node["gallery_path"])
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
    video = cv2.VideoCapture(VIDEO_PATH)
    video_length = cv2.get(video, cv2.CAP_PROP_FRAME_COUNT) / cv2.get(video, cv2.CAP_PROP_FPS)#90 #s
    video_length = video_length * 10 #fake frame
    resp_bboxes = []
    for i in range(video_length):
        video.set(cv2.CAP_PROP_POS_MSEC, i)
        success, image = video.read()
        detect_result = model.detect_reid(sess, image, node["image_node"], node["gallery_path"])

        # _tmp = [int(random.random()*225),int(random.random()*400),
        # int(random.random()*420),int(random.random()*760),
        # i/10.0,
        # find[int(random.random()*(len(find)-1))]]
        _tmp = [detect_result["bbx"][0],detect_result["bbx"][1],
        detect_result["bbx"][2],detect_result["bbx"][3],
        i/10.0,
        detect_result["id"]]
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
    # 在这里，已经获得可以使用的bboxes(np array,[N,4])与bboxesID(list)
    inputs = []
    for bbox in bboxes:
        t = int(bbox["time"])
        video.set(cv2.CAP_PROP_POS_MSEC, t*1000)
        success, image = video.read()
        inputs.append(image[bbox[0]:bbox[2],bbox[1]:bbox[3]])
    res_vec = model.getGallery(sess, inputs, bboxesID, node["gallery_path"], node["apr_input"], node["img_vec"])
    # print(bboxes)
    # print(bboxesID)
    print("[getGallery] return:", res_vec)

if __name__ == "__main__":
    print(renderVideo([1,2,3]))
