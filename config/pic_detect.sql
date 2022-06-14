
create database pic;

use pic;

CREATE TABLE `pic_store` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `uuid` varchar(36) NOT NULL UNIQUE COMMENT '图片的uuid',

  `pic` LONGBLOB NOT NULL COMMENT '存储图片,不为空',

  `group_uuid` varchar(36) NOT NULL COMMENT '组别的uuid',
  `flag_raw` int(4) NOT NULL COMMENT '标志位,1为原图,0非原图',

  `description` varchar(100) DEFAULT NULL COMMENT '描述，暂时为空',

  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `pic_score` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增id',

  `group_uuid` varchar(36) NOT NULL COMMENT '组别的uuid',
  `uuid`  varchar(36) NOT NULL COMMENT '被打分的图片的uuid',
  `auditor_name` varchar(255) DEFAULT NULL COMMENT '审计者名字',
  `score` int(4) NOT NULL COMMENT '评分',

  `description` varchar(100) DEFAULT NULL COMMENT '描述，暂时为空',

  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
