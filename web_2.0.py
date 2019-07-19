from flask import Flask
from flask import request
from PIL import Image
import numpy as np
import urllib3
import base64
import json
from urllib.parse import urlencode
import cv2
import os
import imageio
import shutil


def create_gif(image_list, gif_name, duration=1):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'gif', duration=duration)

    return


def processing(filename):
    # 视频文件名字

    # 采样照片的字符串数组
    save_path = []
    score_path = []

    # 保存图片的路径
    savedpath = filename.split('.')[0] + '/'
    isExists = os.path.exists(savedpath)
    if not isExists:
        os.makedirs(savedpath)
        print('path of %s is build' % savedpath)
    else:
        shutil.rmtree(savedpath)
        os.makedirs(savedpath)
        print('path of %s already exist and rebuild' % savedpath)

    # 视频帧率12
    fps = 12
    # 保存图片的帧率间隔
    count = 200

    # 开始读视频
    videoCapture = cv2.VideoCapture(filename)
    i = 0
    j = 0

    while True:
        success, frame = videoCapture.read()
        i += 1
        if i % count == 0:
            # 保存图片
            j += 1
            savedname = filename.split('.')[0] + '_' + str(j) + '.jpg'
            cv2.imwrite(savedpath + savedname, frame)
            save_path.append(savedpath + savedname)
            print('image of %s is saved' % savedname)
        if not success:
            print('video is all read')
            break

    j = 0
    access_token = '24.1d285a4974f1bb7d97f833b27ac844d2.2592000.1564811698.282335-16711976'
    http = urllib3.PoolManager()
    url = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg?access_token='+access_token

    for process_path in save_path:
        f = open(process_path, 'rb')
        # 读取长宽
        img_size = Image.open(process_path)
        # 参数image：图像base64编码
        img = base64.b64encode(f.read())
        params = {'image': img}
        # 对base64数据进行urlencode处理
        params = urlencode(params)
        request = http.request('POST', url, body=params, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        # 对返回的byte字节进行处理。Python3输出位串，而不是可读的字符串，需要进行转换
        result = str(request.data, 'utf-8')
        # 返回参数json序列化处理
        res = json.loads(result)
        score_map = res['scoremap']
        scoremap = base64.b64decode(res['scoremap'])
        nparr = np.frombuffer(scoremap, np.uint8)
        scoreimg = cv2.imdecode(nparr, 1)
        # 402,402为原图的宽高 请自定替换哦
        scoreimg = cv2.resize(scoreimg, (img_size.size[0], img_size.size[1]), interpolation=cv2.INTER_NEAREST)
        im_new = np.where(scoreimg == 1, 255, scoreimg)
        cv2.imwrite('123' + '_' + str(j) + '.png', im_new)
        score_path.append('123' + '_' + str(j) + '.png')
        j += 1

    gif_name = 'new.gif'
    create_gif(score_path, gif_name)


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello"


resSets = {}


@app.route('/postdata', methods=['POST'])
def postdata():
    f = request.files['content']
    user_input = request.form.get("name")
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    src_imgname = "123.mp4"
    upload_path = os.path.join(basepath, '')
    if os.path.exists(upload_path) == False:
        os.makedirs(upload_path)
    f.save(upload_path + src_imgname)
    save_path = os.path.join(basepath, '')
    if os.path.exists(save_path) == False:
        os.makedirs(save_path)
    save_imgname = "123.mp4"
    processing(save_imgname)
    save_gif = "/new.gif"
    resSets["resurl"] = "http://127.0.0.1:8090" + save_gif
    return json.dumps(resSets, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
