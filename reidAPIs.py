import json
import random
import numpy as np

def renderTrackbar(find):
    print("[renderTrackbar]Picked are:",find)
    ans = []
    for i in range(0, len(find)):
        ans.append([])
        for j in range(0,100):
            ans[i].append([j,int(random.random()*100)])

    return ans
def renderVideo(find):
    print("[renderVideo]Picked are:",find)
    resp_bboxes = []
    for i in range(900):
        _tmp = [int(random.random()*225),int(random.random()*400),
        int(random.random()*420),int(random.random()*760),
        i/10.0,
        find[int(random.random()*(len(find)-1))]]

        resp_bboxes.append(_tmp)

    return resp_bboxes

def saveBboxes(_bboxes):
    _bboxes_list = []
    bboxesID = []
    for _bbox in _bboxes:
        _bboxes_list.append(list(_bbox["data"].values()))
        bboxesID.append(_bbox["id"])
    bboxes = np.array(_bboxes_list)
    print(bboxes)
    print(bboxesID)

if __name__ == "__main__":
    print(renderVideo([1,2,3]))
