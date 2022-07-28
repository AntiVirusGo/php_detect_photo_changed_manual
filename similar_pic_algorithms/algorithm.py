# coding=utf-8

import matplotlib
import os
from similar_pic_algorithm import PicSimilarCal

matplotlib.use('TkAgg')

from loguru_log import log_data, log_debug

class SimilarOrderAlgorithm:
    """
    其中 get_max_from_res_img_similar() 和 get_max_from_res_img_similar_back_one() 两个函数和算法无关，只是用于从图像近似度算法返回的列表中根据dict计算取得加权最大值的函数

    路径算法请模仿  排序列表, 算法名称 = SingleImgSimilar_Order(self, ) ，要求返回两个值，一个是排序列表，另一个是算法名称

    本篇的路径算法：
        1. 单图寻找最像 代码中最重要的部分，用于进行排序算法
        SingleImgSimilar_Order(self, )

        2. 回溯1图寻找 代码中最重要的部分，用于进行排序算法
        BackOneImgSimilar_Order(self)
    """
    def __init__(self, img_dir=None, res_img_similar=None, img_init=None, img_list=None):
        self.res_img_similar = res_img_similar
        self.img_dir = img_dir
        self.img_init = img_init
        self.img_list = img_list

        self.picSimilarCal = PicSimilarCal()

    def get_max_from_res_img_similar(self, res_img_similar):
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

    def get_max_from_res_img_similar_back_one(self, res_img_similar):
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

    def SingleImgSimilar_Order(self, ):
        """单图寻找最像 代码中最重要的部分，用于进行排序算法"""

        # [!] 程序结果：相似度排序列表 similar_order
        similar_order = []
        similar_order.append(self.img_init)

        # 下一个代码段要进行排序，使用 img_list2 来进行处理
        # 对于文件名列表，这里需要深拷贝赋值给列表 img_list_cycle
        img_list2 = self.img_list.copy()
        # 因为入口img已经确认，待测试图片中可删去
        img_list2.remove(self.img_init)

        target_img = os.path.join(self.img_dir, self.img_init)

        for i in self.img_list:
            res_img_similar = []  # res_img_similar 用于临时存储本轮中 剩余图片 与 target_img 的相似比较结果
            for img_list_index in range(len(img_list2)):
                res_img_similar.append(self.picSimilarCal.runAllImageSimilaryFun(target_img, os.path.join(self.img_dir, img_list2[img_list_index])))
            most_similar_img_filename = self.get_max_from_res_img_similar(res_img_similar)
            img_list2.remove(most_similar_img_filename)
            similar_order.append(most_similar_img_filename)
            if img_list2 == []:
                break
            print(similar_order)
            target_img = os.path.join(self.img_dir, similar_order[-1])
        log_data.success("排序结果为："+str(similar_order))
        return similar_order, "单图寻找最像"


    def BackOneImgSimilar_Order(self):
        """回溯1图寻找 代码中最重要的部分，用于进行排序算法"""

        # [!] 程序结果：相似度排序列表 similar_order
        similar_order = []
        similar_order.append(self.img_init)

        # 下一个代码段要进行排序，使用 img_list2 来进行处理
        # 对于文件名列表，这里需要深拷贝赋值给列表 img_list_cycle
        img_list2 = self.img_list.copy()
        # 因为入口img已经确认，待测试图片中可删去
        img_list2.remove(self.img_init)

        target_img = os.path.join(self.img_dir, self.img_init)

        for i in self.img_list:
            res_img_similar = []  # res_img_similar 用于临时存储本轮中 剩余图片 与 target_img 的相似比较结果

            if len(similar_order)>=2:
                target_img_back_one = os.path.join(self.img_dir, similar_order[-2])
            else:
                target_img_back_one = os.path.join(self.img_dir, similar_order[-1])

            log_data.debug(" 正在测试： " + str(target_img) + "回溯: " + target_img_back_one )
            for img_list_index in range(len(img_list2)):
                # 从剩余图片拿出来要与 target 图片进行比较的图片 是  img_list2[img_list_index]

                # 本节图片比较
                target_compare_score = self.picSimilarCal.runAllImageSimilaryFun(target_img, os.path.join(self.img_dir, img_list2[img_list_index]))
                # 回溯一张图片比较

                back_target_score = self.picSimilarCal.runAllImageSimilaryFun(target_img_back_one, os.path.join(self.img_dir, img_list2[img_list_index]))
                # 添加元组 (本节图片比较, 回溯一张图片比较) 至 res_img_similar
                res_img_similar.append((target_compare_score, back_target_score))

            most_similar_img_filename = self.get_max_from_res_img_similar_back_one(res_img_similar)
            img_list2.remove(most_similar_img_filename)
            similar_order.append(most_similar_img_filename)
            print(similar_order)
            if img_list2 == []:
                break
            target_img = os.path.join(self.img_dir, most_similar_img_filename)
        log_data.success("排序结果为："+str(similar_order))
        return similar_order, "回溯1图寻找"

    def BackAllImgSimilar_Order(self):
        """回溯全部已匹配。"""

        # [!] 程序结果：相似度排序列表 similar_order
        similar_order = []
        similar_order.append(self.img_init)

        # 下一个代码段要进行排序，使用 img_list2 来进行处理
        # 对于文件名列表，这里需要深拷贝赋值给列表 img_list_cycle
        img_list2 = self.img_list.copy()
        # 因为入口img已经确认，待测试图片中可删去
        img_list2.remove(self.img_init)

        target_img = os.path.join(self.img_dir, self.img_init)

        for i in self.img_list:
            res_img_similar = []
            # 中间变量 res_img_similar 用于临时存储本轮中 剩余图片 与 target_img 的相似比较结果

            target_img_back_one = os.path.join(self.img_dir, similar_order[-1])

            log_data.debug(" 正在测试： " + str(target_img) + "回溯: " + target_img_back_one )
            for img_list_index in range(len(img_list2)):
                # 从 img_list2 剩余图片拿出来要与 target 图片进行比较的图片 是  img_list2[img_list_index]

                # 未排序剩余图片中待测试图片（for target_img in img_list2） 与 排序图片 res_img_similar 进行回溯匹配
                # for i in range(len(res_img_similar))

                # # 本节图片比较
                # # target_img 是 要测试的图片
                # target_compare_score = self.picSimilarCal.runAllImageSimilaryFun(target_img, os.path.join(self.img_dir, img_list2[img_list_index]))
                # # 回溯图片比较
                # # target_img_back_one 是 similar_order[-1]
                #
                # back_target_score = self.picSimilarCal.runAllImageSimilaryFun(target_img_back_one, os.path.join(self.img_dir, img_list2[img_list_index]))
                # # 添加元组 (本节图片比较, 回溯一张图片比较) 至 res_img_similar

                for single_similar_order in range(similar_order):
                    res_img_similar.append()

            most_similar_img_filename = self.get_max_from_res_img_similar_back_one(res_img_similar)
            img_list2.remove(most_similar_img_filename)
            similar_order.append(most_similar_img_filename)
            print(similar_order)
            if img_list2 == []:
                break
            target_img = os.path.join(self.img_dir, most_similar_img_filename)
        log_data.success("排序结果为："+str(similar_order))
        return similar_order, "回溯全部已匹配"