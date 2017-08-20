#ReID Player API
##Usage
###依赖

+ python-flask
+ opencv3
+ vue.js
+ jQuery
+ echarts
+ semanticUI

###使用方法
```
启动服务器，通过localhost 5000端口即可访问
python server.py
```
对于服务器端的修改如更改端口，关闭调试模式等都在server.py下修改
需要注意的是：demo中修改了flask-Jinja2所使用的默认渲染标签以避免与vue.js冲突
**接入算法API**

为了接入reid相关的算法，只需修改reidAPIs.py即可，demo的其余部分将会调用该文件中的函数。
##reidAPIs
###renderTrackbar(find)

渲染进度条，用于制作某个ID在整个视频中出现的概率，这里的只用将每一帧(fps可自定)
> **find: list[N]**, find 为一个list，包含若干字符串，为需要查询的bbox的ID

**Return => list(bbox_num,frame_num]**, 其中每一行为每一个人在每一帧出现的概率，范围[0,1]

###renderVideo(find):

渲染视频，用于将所要查询的bbox在视频中的某一时刻出现的查询目标框出来，并返回框出的bbox信息
需要注意的是，这里采用的是出现的时间而非帧号,时间单位为秒
> **find: list[N]**, find 为一个list，包含若干字符串，为需要查询的bbox的ID

**Return =>Numpy Array[total-frame-num]**, 返回一个list(bbox_num,6)，每一行为[y0,x0,y1,x1,time,ID]

###saveBboxes(\_bboxes):
处理并保存由用户画出的bbox，这里做提取特征并导入数据库的操作

> **\_bboxes**: 为画出的bbox字典，在这部分中，会将_bboxes先转化为bboxes numpy数组，而每个bbox的ID也会被存储在bboxesID中

该函数不严格要求返回值，但建议可以返回某些标识符用于代码的调试
用来将人工定义的bboxes处理后导入数据库



##Issues

部分问题将在下个版本中解决
+ 未提供方便同时修改前后端操作视频的接口
+ 视频格式仅支持H5所直接支持的播放格式
+ 未提供修改前端画bbox的fps的接口，现在默认为125ms一帧
+ trackbar与board的mouseup事件在全局冲突，所以目前的mouseup事件都是绑定在元素本身而非整个文档，这会导致在画bbox时一旦手滑画出视频就会导致鼠标松开后bbox仍黏在鼠标上，需要再完成一次点击操作才能修复。
+ 播放器太丑
+ 部分代码使用的jquery(主要是offset与ajax), 降低代码的优雅性
+ 前后端半分离的结构下的各种性能在各种情况下的表现尚不清晰，开发时采用前后端完全分离搭载不同服务器上的方式（显然这种方式并不受广大群众的欢迎但性能极优）
