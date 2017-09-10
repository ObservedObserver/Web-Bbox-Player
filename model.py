from __future__ import print_function
import  RPNplus._init_paths
import inspect
import os
import shutil
import time
import sys
import numpy as np
import tensorflow as tf
from RPNplus.image_pylib import IMGLIB
from datetime import datetime
from  RPNplus import data_engine
from scipy import misc
from RPNplus.detect import RPN
from  Tfaprnet import tf_aprnet
from Tfaprnet.util import reid

# 全局变量
# gallery_path = os.path.expanduser('../DATA/testData/ourImage/gallery')

##建立tensorflow模型

def build_model():
#   Parameter setting
    gpuNow = '/gpu:0'

    #   RPNplus model path
    modelPath = '../DATA/models/RPNplus/models/model.npy'

    vggModelPath = '../DATA/models/RPNplus/models/vgg16.npy'

    #   Aprnet model path
    Aprnet_path = '../DATA/models/aprnet/model'


    save_img_path = None

    imageDir = '../DATA/testData/ourImage/testimg'
    #resultsDir= './results/'
    #  checkDir(imageDir,False)
    #checkDir(resultsDir,True)
    #    checkFile(vggModelPath)
    #   checkFile(modelPath)

    resultsDir = '../DATA/testData/ourImage/Result'

    image_height = 480
    image_width = 720

    testDeal = data_engine.RPN_Test()

    gallery_path = os.path.expanduser('../DATA/testData/ourImage/gallery')
    gpu_memory_fraction = 0.25
    node = {}

    sess = tf.Session()
        ### Build model

    image = tf.placeholder(tf.float32, [1, image_height, image_width, 3])


    cnn = RPN(vggModelPath, modelPath)


    with tf.name_scope('content_rpn'):
        cnn.build(image)

    ckpt = tf.train.get_checkpoint_state(Aprnet_path)
    init = tf.global_variables_initializer()
    bbxs = tf.placeholder(tf.float32, [None, 4], name='bbxs')
    idxs = tf.placeholder(tf.int32,[None], name='idx')
    det_output = tf.image.crop_and_resize(image, bbxs, idxs, crop_size=(224,224),name='detection_output')
    inputs = tf.placeholder(tf.float32,[None,224,224,3])
    img_vec, _= tf_aprnet.create_resnet50(inputs)
    saver = tf.train.Saver()
    sess.run(init)
    saver.restore(sess,ckpt.model_checkpoint_path)
    print("Build model successfully")
    node['cnn_prob'] = cnn.prob
    node['cnn_bbox_pred'] = cnn_bbox_pred
    node['image_node']=image
    node['detection_output'] = det_output
    node['apr_input'] = inputs
    node['img_vec'] = img_vec
    node['gallery_path'] = gallery_path
    return sess,node

### 输入inputs为所有行人的bbx，一般是demo手动截取的那一组bbox，name_lst是为每幅图片取的id名
### 该函数用于构建数据库，最终函数将结果保存为json文件，格式为{id0:特征向量，id1:特征向量}
def getGallery(sess, inputs, name_lst, gallery_path, apr_input, img_vec):
    gallery = json.load(gallery_path)
    res_vec = sess.run(img_vec, feed_dict={apr_input:inputs})
    for name in name_lst:
        gallery[name] = res_vec
    with open(gallery_path, 'w') as f:
        json.dump(gallery, f)
    return res_vec

### inputs为行人的bbx，输出为id的列表
### 该函数用于计算出所有行人bbx对应的id，也用于对人工截取的bbox计算id时使用
def getID(sess, inputs, apr_input, gallery_path):

    res_vec = sess.run(img_vec, feed_dict={apr_input:inputs})
    id_lst = reid(res_vec, gallery_path)
    return id_lst


### image为检测图像，输出result为列表，里面各元素为一个字典，有id，bbx键
### 该函数用于检测出一副图像中所有的行人的bbx，并给出其对应的id
def detect_reid(sess, image, image_node, gallery_path):
    imglib = IMGLIB()
    [test_prob, test_bbox_pred] = sess.run([cnn_prob, cnn_bbox_pred], feed_dict={image_node: image })
    bbox = testDeal.rpn_nms(test_prob, test_bbox_pred)
    imglib.setGoodBBXs(bbox, 'person', 0.99)
    bb = imglib.bbxs
    bb_pos = imglib.getBBxs()
    bb_norm = np.array(bb_pos,dtype=np.float32)/div
    bb_idxs = np.zeros(len(bb_pos))
    res_vec = sess.run(img_vec, feed_dict={image:pix2, bbxs:bb_norm, idxs:bb_idxs})
    id_lst = reid(res_vec, gallery_path)
    result = []
    for i,bbx in enumerate(bb):
        data = {}
        bbx_pos = [bbx.x,bbx.y,bbx.w+bbx.x,bbx.h+bbx.y]
        bbx.name = id_lst[i]
        data['bbx'] = bbx_pos
        data['id'] = id_lst[i]
        # 需要提供 data['prob'], 即概率值
        result.append(data)
    return result
