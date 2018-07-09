# Author: Alan

admin_table_create_sql='''CREATE TABLE IF NOT EXISTS admin(
                          id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                          `name` VARCHAR (20) NOT  NULL UNIQUE ,
                          pwd CHAR (32) NOT NULL 
                          ) ENGINE=INNODB CHARSET=UTF8'''

user_table_create_sql='''CREATE TABLE IF NOT EXISTS `user`(
                          id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                          phone BIGINT(11) NOT  NULL UNIQUE ,
                          pwd CHAR (32) NOT NULL,
                          money DECIMAL (9,2) NOT NULL comment '余额',
                          is_member TINYINT(1) NOT NULL DEFAULT 0 comment '是否是会员',
                          is_delete TINYINT(1) NOT NULL DEFAULT 0 comment '是否删除'
                          ) ENGINE=INNODB CHARSET=UTF8'''

video_table_create_sql='''CREATE TABLE IF NOT EXISTS video(
                          id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                          `url` VARCHAR (255) NOT  NULL  comment '视频地址',
                          cost DECIMAL (9,2) NOT NULL comment '普通价格',
                          member_cost DECIMAL (9,2) NOT NULL comment '会员价格',
                          is_charge TINYINT(1) NOT NULL DEFAULT 0 comment '是否收费',
                          is_delete TINYINT(1) NOT NULL DEFAULT 0 comment '是否删除'
                          ) ENGINE=INNODB CHARSET=UTF8'''

dwn_records_table_create_sql='''CREATE TABLE IF NOT EXISTS dwn_records(
                          id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                          user_id int NOT  NULL  ,
                          video_id int NOT  NULL  ,
                          cost DECIMAL (9,2) NOT NULL comment '当时付费价格'
                          ) ENGINE=INNODB CHARSET=UTF8'''


notice_table_create_sql='''CREATE TABLE IF NOT EXISTS notice(
                          id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                          content LONGTEXT NOT  NULL  comment '公告内容',
                          is_delete TINYINT(1) NOT NULL DEFAULT 0 comment '是否删除'
                          ) ENGINE=INNODB CHARSET=UTF8'''