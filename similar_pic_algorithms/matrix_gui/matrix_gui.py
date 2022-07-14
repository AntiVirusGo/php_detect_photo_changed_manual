import time
import re

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# order_list = ['input_Cam000.png', 'input_Cam001.png', 'input_Cam002.png', 'input_Cam003.png', 'input_Cam004.png', 'input_Cam005.png', 'input_Cam006.png', 'input_Cam007.png', 'input_Cam008.png', 'input_Cam009.png', 'input_Cam010.png', 'input_Cam011.png']


def DiGraph(order_list, algorithm_similar_name):
    for order_list_index in range(len(order_list)):
        filename_num = re.search(r"input_Cam(\d{3}).png", order_list[order_list_index]).group(1)
        order_list[order_list_index] = filename_num
    # order_list 是排序结果。 Eg: ['003', '005', '010', '001', '009', '000', '002', '011', '012', '013', '004', '007', '008']


    # 开始绘制 矩阵有向单连线图
    FG = nx.Graph()

    arrow_edges = []


    pos = dict()
    img_filename_num = 0
    for row in range(9):
        for col in range(9):
            pos["%.3d" % img_filename_num] = (col, -row)
            print(pos)
            try:
                arrow_edges.append((order_list[img_filename_num], order_list[img_filename_num+1]))
            except:
                pass
            img_filename_num = img_filename_num + 1

    FG.add_edges_from(arrow_edges)

    # colors = list(nx.get_edge_attributes(FG, 'color').values())
    # widths = list(nx.get_edge_attributes(FG, 'width').values())
    colors = nx.get_edge_attributes(FG, 'color').values()


    nx.draw(FG, with_labels=True,pos=pos, arrows=True, connectionstyle="arc3,rad=0.3", )
    # connectionstyle="arc3,rad=0.3" 是连线的曲度，使边缘更弯曲，只需增加 "rad=x" 的 x

    local_time_str = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    plt.savefig("{TIMESTAMP}-{ALGORITHM_NAME}.png".format(TIMESTAMP=local_time_str, ALGORITHM_NAME=algorithm_similar_name))
    plt.show()

