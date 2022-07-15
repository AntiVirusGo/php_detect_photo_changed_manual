# coding=utf-8

import matplotlib
import os

matplotlib.use('TkAgg')

from loguru_log import log_data, log_debug

from matrix_gui.matrix_gui import DiGraph
from algorithm import SimilarOrderAlgorithm

if __name__ == "__main__":

    # [CONFIG]
    # 数据源图片所在目录
    # img_dir = r"""./bicycle/"""
    img_dir = r"""./bedroom/"""


    # 图片入口。
    img_init = "input_Cam040.png"
    log_debug.info("图片入口: {IMG_INIT}".format(IMG_INIT=img_init))

    # [DEBUG]
    # start 如果用于测试，这里可以只匹配15张图片：os.listdir(img_dir)[:15]
    img_list = os.listdir(img_dir)
    log_debug.info("测试图片数量：{IMG_LIST_LEN}".format(IMG_LIST_LEN=str(len(img_list))))
    # end

    # ---运行算法生成排序列表-------------------------------------------------------------------
    # 初始化图像近似度算法类
    similar_order_algorithm = SimilarOrderAlgorithm(img_dir=img_dir, img_init=img_init, img_list=img_list)

    # 回溯1图寻找 算法
    # res_order_list, algorithm_similar_name = similar_order_algorithm.BackOneImgSimilar_Order()
    # 单图寻找最像 算法
    res_order_list, algorithm_similar_name = similar_order_algorithm.SingleImgSimilar_Order()

    # ---生成结果目录图集，生成矩阵连线图-------------------------------------------------------------------

    # 生成矩阵单向连线图，绘制为GUI
    DiGraph(res_order_list, algorithm_similar_name, img_dir)


