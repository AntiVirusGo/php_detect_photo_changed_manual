# coding=utf-8

import os
import uuid
import random

import pymysql
from dbutils.pooled_db import PooledDB

mysql_pool = PooledDB(
    pymysql,50,host='127.0.0.1',user='root',passwd='root',db='pic',port=3306,maxconnections=2000,blocking=True
)

pic_path = r"""C:\Users\ranja\Documents\BiLing\20220207-sonatype-dev-git\vul-spider\pic_client\hdr"""


def save_pic(pic_binary_data, group_uuid, flag_raw):
    conn = mysql_pool.connection()
    try:
        pic_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()) + str(random.random()))).replace('-','')
        with conn.cursor() as cur:
            sql_precompile = """insert into `pic_store` (`uuid`,`pic`,`group_uuid`,`flag_raw`) values (%s,%s,%s,%s);"""
            exec_params = (
                pic_uuid,
                pic_binary_data,
                group_uuid,
                flag_raw
            )
            cur.execute(
                sql_precompile, exec_params
            )
            conn.commit()
        conn.commit()
    except Exception as err:
        print(err)
        conn.rollback()
        raise
    finally:
        conn.close()


for pic_file_name in range(1,501):
    if pic_file_name % 10 == 1:
        current_group_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()) + str(random.random()))).replace('-','')
        current_flag_raw = 1
    else:
        current_flag_raw = 0

    
    pic_file_path = os.path.join(pic_path, str(pic_file_name)+'.png')
    with open(pic_file_path, 'rb') as f:
        pic_binary_data = f.read()
        f.close()

    save_pic(pic_binary_data, current_group_uuid, current_flag_raw)

