#!/bin/env python
# encoding:utf8
# 基础库
# author songmw<imphp@qq.com>
# date 	 2015.11.19
import sys
import os
from lib import Db
from pprint import pprint
import ConfigParser

ROOT_PATH = os.path.split(os.path.realpath(__file__))[0]

# 调试函数
def de(var):
	pprint(var)
	sys.exit(0)

# 获取数据库对象
def getDbInstance():

	db_conf = ROOT_PATH + '/config/db.ini'
	confIns = loadConf(db_conf)

	db_args = {}
	db_args['host'] = confIns.get('db', 'host')
	db_args['db'] = confIns.get('db', 'db')
	db_args['user'] = confIns.get('db', 'user')
	db_args['passwd'] = confIns.get('db', 'passwd')
	db_args['charset'] = confIns.get('db', 'charset')

	return Db.Mysql(db_args)

# 加载配置文件
# 传递配置文件地址，返回加载对象
# 使用 获取到的对象 .get('[父类]', '[子类]')
def loadConf(config_file):

	if not os.path.exists(config_file) :
		return False

	cnf = ConfigParser.ConfigParser()
	cnf.read(config_file)
	return cnf
