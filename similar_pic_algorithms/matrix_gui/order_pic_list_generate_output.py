# coding=utf-8

import os


def order_pic_list_generate_output(order_list, img_dir, time_str, algorithm_name):

    target_output_dir = "./out_matrix_pics/{TIMESTAMP}-{ALGORITHM_NAME}/".format(TIMESTAMP=time_str, ALGORITHM_NAME=algorithm_name)
    os.mkdir(target_output_dir)
    for order_list_index in range(len(order_list)):
        with open(os.path.join(img_dir, order_list[order_list_index]), "rb") as f:
            img_content = f.read()
            f.close()
        with open(os.path.join(target_output_dir, "name{IMG_SERIAL_NUM}.png".format(IMG_SERIAL_NUM=str(order_list_index))), "wb") as f:
            f.write(img_content)
            f.close()


