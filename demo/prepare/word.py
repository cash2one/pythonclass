#!/bin/env python
# encoding:utf8
#
# author songmw<imphp@qq.com>
# date 	 2015.11.19
import os
import sys

# 必添加设置加载路径为 上一级目录
path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(path + '/../')

# 加载必须的类库
from Base import *

if __name__ == '__main__' :
	
	db = getDbInstance()

	sql = 'select * from beikao.prepare_module_type'
	val = db.query(sql).fetchall()

	de(val)


