import cv2
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import matplotlib
import os
import re

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from loguru_log import log_data, log_debug
from matrix_gui.matrix_gui import DiGraph

def aHash(img):
    # 均值哈希算法
    # 缩放为8*8
    img = cv2.resize(img, (8, 8))
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 64
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


def dHash(img):
    # 差值哈希算法
    # 缩放8*8
    img = cv2.resize(img, (9, 8))
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


def pHash(img):
    # 感知哈希算法
    # 缩放32*32
    img = cv2.resize(img, (32, 32))  # , interpolation=cv2.INTER_CUBIC

    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 将灰度图转为浮点型，再进行dct变换
    dct = cv2.dct(np.float32(gray))
    # opencv实现的掩码操作
    dct_roi = dct[0:8, 0:8]

    hash = []
    avreage = np.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash


def calculate(image1, image2):
    # 灰度直方图算法
    # 计算单通道的直方图的相似值
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                     (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def classify_hist_with_split(image1, image2, size=(256, 256)):
    # RGB每个通道的直方图相似度
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


def cmpHash(hash1, hash2):
    # Hash值对比
    # 算法中1和0顺序组合起来的即是图片的指纹hash。顺序不固定，但是比较的时候必须是相同的顺序。
    # 对比两幅图的指纹，计算汉明距离，即两个64位的hash值有多少是不一样的，不同的位数越小，图片越相似
    # 汉明距离：一组二进制数据变成另一组数据所需要的步骤，可以衡量两图的差异，汉明距离越小，则相似度越高。汉明距离为0，即两张图片完全一样
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    return n


def getImageByUrl(url):
    # 根据图片url 获取图片对象
    html = requests.get(url, verify=False)
    image = Image.open(BytesIO(html.content))
    return image


def PILImageToCV():
    # PIL Image转换成OpenCV格式
    path = "/Users/waldenz/Documents/Work/doc/TestImages/t3.png"
    img = Image.open(path)
    plt.subplot(121)
    plt.imshow(img)
    print(isinstance(img, np.ndarray))
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    print(isinstance(img, np.ndarray))
    plt.subplot(122)
    plt.imshow(img)
    plt.show()


def CVImageToPIL():
    # OpenCV图片转换为PIL image
    path = "/Users/waldenz/Documents/Work/doc/TestImages/t3.png"
    img = cv2.imread(path)
    # cv2.imshow("OpenCV",img)
    plt.subplot(121)
    plt.imshow(img)

    img2 = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.subplot(122)
    plt.imshow(img2)
    plt.show()


def bytes_to_cvimage(filebytes):
    # 图片字节流转换为cv image
    image = Image.open(filebytes)
    img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    return img


def runAllImageSimilaryFun(para1, para2):
    # 均值、差值、感知哈希算法三种算法值越小，则越相似,相同图片值为0
    # 三直方图算法和单通道的直方图 0-1之间，值越大，越相似。 相同图片为1

    # t1,t2   14;19;10;  0.70;0.75
    # t1,t3   39 33 18   0.58 0.49
    # s1,s2  7 23 11     0.83 0.86  挺相似的图片
    # c1,c2  11 29 17    0.30 0.31

    single_dict = dict()

    single_dict['filename'] = [os.path.basename(para1), os.path.basename(para2)]
    if para1.startswith("http"):
        # 根据链接下载图片，并转换为opencv格式
        img1 = getImageByUrl(para1)
        img1 = cv2.cvtColor(np.asarray(img1), cv2.COLOR_RGB2BGR)

        img2 = getImageByUrl(para2)
        img2 = cv2.cvtColor(np.asarray(img2), cv2.COLOR_RGB2BGR)
    else:
        # 通过imread方法直接读取物理路径
        img1 = cv2.imread(para1)
        img2 = cv2.imread(para2)

    # hash1 = aHash(img1)
    # hash2 = aHash(img2)
    # n1 = cmpHash(hash1, hash2)
    # # print('均值哈希算法相似度aHash：', n1)
    # single_dict['aHash'] = n1
    #
    # hash1 = dHash(img1)
    # hash2 = dHash(img2)
    # n2 = cmpHash(hash1, hash2)
    # # print('差值哈希算法相似度dHash：', n2)
    # single_dict['dHash'] = n2
    #
    # hash1 = pHash(img1)
    # hash2 = pHash(img2)
    # n3 = cmpHash(hash1, hash2)
    # # print('感知哈希算法相似度pHash：', n3)
    # single_dict['pHash'] = n3

    n4 = classify_hist_with_split(img1, img2)

    # print('三直方图算法相似度：', n4)
    # print(type(n4))
    single_dict['SanZhiFang'] = n4

    # n5 = calculate(img1, img2)
    # # print("单通道的直方图", n5)
    # single_dict['DanTongDao'] = n5
    #
    #
    # # print("%d %d %d %.2f %.2f " % (n1, n2, n3, round(n4[0], 2), n5[0]))
    # # print("%.2f %.2f %.2f %.2f %.2f " % (1 - float(n1 / 64), 1 -
    # #                                      float(n2 / 64), 1 - float(n3 / 64), round(n4[0], 2), n5[0]))
    #
    # plt.subplot(121)
    # plt.imshow(Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)))
    # plt.subplot(122)
    # plt.imshow(Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)))
    # # plt.show()

    return single_dict

def get_max_from_res_img_similar(res_img_similar):
    # 传入的 res_img_similar 是一个列表，其元素是一个经过 'filename'字段中的两个文件比较数据 的字典
    # 返回值为 文件名， 如果返回None说明没有可比文件。
    # Eg: [
    #       {'filename': ['input_Cam000.png', 'input_Cam001.png'], 'aHash': 1, 'dHash': 4, 'pHash': 0, 'SanZhiFang': array([0.8800225], dtype=float32), 'DanTongDao': array([0.8678064], dtype=float32)},
    #       {'filename': ['input_Cam000.png', 'input_Cam002.png'], 'aHash': 2, 'dHash': 6, 'pHash': 1, 'SanZhiFang': array([0.8866753], dtype=float32), 'DanTongDao': array([0.8766418], dtype=float32)},
    #   ]

    # 变量 max 和 max_item 是本函数中用于最大值比较的中间变量
    max = 0
    max_item = None

    for single_res_img_similar in res_img_similar:
        # print(single_res_img_similar['filename'][1], single_res_img_similar['SanZhiFang'][0])
        # 如果要更改最相似匹配算法，可以在这里更改。比如，可以改为 0.4* single_res_img_similar['SanZhiFang'] + 0.6* single_res_img_similar['pHash']
        # 目前两张图最相似算法：三直方图数值算法为加权算法
        if single_res_img_similar['SanZhiFang'][0] >= max:
            max_item = single_res_img_similar['filename'][1]
            max =  single_res_img_similar['SanZhiFang'][0]
    if max_item == None:
        return None
    return max_item

def get_max_from_res_img_similar_back_one(res_img_similar):
    # 传入的 res_img_similar 是一个列表，其元素是包含两个dict的元组
    # 返回值为 文件名， 如果返回None说明没有可比文件。
    # Eg: [
    #       (
    #               {'filename':
    #                       ['input_Cam040.png', 'input_Cam000.png'],
    #                'SanZhiFang':
    #                       array([0.87966466], dtype=float32)
    #                },

    # 变量 max 和 max_item 是本函数中用于最大值比较的中间变量
    max = 0
    max_item = None

    for single_res_img_similar in res_img_similar:
        # print(single_res_img_similar['filename'][1], single_res_img_similar['SanZhiFang'][0])
        # 如果要更改最相似匹配算法，可以在这里更改。比如，可以改为 0.4* single_res_img_similar['SanZhiFang'] + 0.6* single_res_img_similar['pHash']
        # 目前两张图最相似算法：三直方图数值算法为加权算法
        target_score = single_res_img_similar[0]['SanZhiFang'][0] + single_res_img_similar[1]['SanZhiFang'][0]
        if target_score >= max:
            max_item = single_res_img_similar[0]['filename'][1]
            max =  target_score
    if max_item == None:
        return None
    return max_item

def SingleImgSimilar_Order(img_init, img_list):
    """单图寻找最像 代码中最重要的部分，用于进行排序算法"""

    # [!] 程序结果：相似度排序列表 similar_order
    similar_order = []
    similar_order.append(img_init)

    # 下一个代码段要进行排序，使用 img_list2 来进行处理
    # 对于文件名列表，这里需要深拷贝赋值给列表 img_list_cycle
    img_list2 = img_list.copy()
    # 因为入口img已经确认，待测试图片中可删去
    img_list2.remove(img_init)

    target_img = os.path.join(img_dir, img_init)

    for i in img_list:
        res_img_similar = []  # res_img_similar 用于临时存储本轮中 剩余图片 与 target_img 的相似比较结果
        for img_list_index in range(len(img_list2)):
            res_img_similar.append(runAllImageSimilaryFun(target_img, os.path.join(img_dir, img_list2[img_list_index])))
        most_similar_img_filename = get_max_from_res_img_similar(res_img_similar)
        img_list2.remove(most_similar_img_filename)
        if img_list2 == []:
            break
        similar_order.append(most_similar_img_filename)
        print(similar_order)
        target_img = os.path.join(img_dir, most_similar_img_filename)
    log_data.success("排序结果为："+str(similar_order))
    return similar_order, "单图寻找最像"


def BackOneImgSimilar_Order(img_init, img_list):
    """回溯1图寻找 代码中最重要的部分，用于进行排序算法"""

    # [!] 程序结果：相似度排序列表 similar_order
    similar_order = []
    similar_order.append(img_init)

    # 下一个代码段要进行排序，使用 img_list2 来进行处理
    # 对于文件名列表，这里需要深拷贝赋值给列表 img_list_cycle
    img_list2 = img_list.copy()
    # 因为入口img已经确认，待测试图片中可删去
    img_list2.remove(img_init)

    global img_dir
    target_img = os.path.join(img_dir, img_init)

    for i in img_list:
        res_img_similar = []  # res_img_similar 用于临时存储本轮中 剩余图片 与 target_img 的相似比较结果

        if len(similar_order)>=2:
            target_img_back_one = os.path.join(img_dir, similar_order[-2])
        else:
            target_img_back_one = os.path.join(img_dir, similar_order[-1])

        log_data.debug(" 正在测试： " + str(target_img) + "回溯: " + target_img_back_one )
        for img_list_index in range(len(img_list2)):
            # 从剩余图片拿出来要与 target 图片进行比较的图片 是  img_list2[img_list_index]

            # 本节图片比较
            target_compare_score = runAllImageSimilaryFun(target_img, os.path.join(img_dir, img_list2[img_list_index]))
            # 回溯一张图片比较

            back_target_score = runAllImageSimilaryFun(target_img_back_one, os.path.join(img_dir, img_list2[img_list_index]))
            # 添加元组 (本节图片比较, 回溯一张图片比较) 至 res_img_similar
            res_img_similar.append((target_compare_score, back_target_score))

        most_similar_img_filename = get_max_from_res_img_similar_back_one(res_img_similar)
        img_list2.remove(most_similar_img_filename)
        if img_list2 == []:
            break
        similar_order.append(most_similar_img_filename)
        print(similar_order)
        target_img = os.path.join(img_dir, most_similar_img_filename)
    log_data.success("排序结果为："+str(similar_order))
    return similar_order, "回溯1图寻找"


if __name__ == "__main__":

    # [CONFIG]
    # 数据源图片所在目录
    global img_dir
    img_dir = r"""./bicycle/"""
    # 图片入口。
    img_init = "input_Cam040.png"
    log_debug.info("图片入口: {IMG_INIT}".format(IMG_INIT=img_init))

    # [DEBUG]
    # start 如果用于测试，这里可以只匹配15张图片：os.listdir(img_dir)[:15]
    img_list = os.listdir(img_dir)
    log_debug.info("测试图片数量：{IMG_LIST_LEN}".format(IMG_LIST_LEN=str(len(img_list))))
    # end

    # DiGraph(ImgOrder(img_dir, img_init, img_list))
    # DiGraph()
    DiGraph(BackOneImgSimilar_Order(img_init, img_list))


