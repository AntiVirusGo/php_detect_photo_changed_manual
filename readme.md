

# 概述

用来进行图片美颜程度识别，使用php，用于给志愿者提供人工判断美颜程度的WEB站点。

# 目录结构

`config/pic_detect.sql`是MYSQL（或MariaDB）的创建数据库**pic**和数据表`pic_store`及`pic_score`的sql脚本。可以直接在服务器端或者mysql的二进制命令下使用`mysql -uroot -p < pic_detect.sql`的方式创建数据库的表结构。

`tmp_import_pic_2_mysql.py`是python3写的脚本，在一开始没有图片的二进制数据入库的情况下，用于导入紧凑挨着的10个一组的500张图片的脚本。更改代码中的`pic_path`变量，即可本地导入500张图片。如果导入非一开始的1-500命名的png图片，需要修改python程序。

# 界面

![](images/mdmd2022-06-14-12-30-28.png)




