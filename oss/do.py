#!/bin/env python
#encoding:utf8
# 
# 将服务器文件上传到oss上
# 
# author songmw<imphp@qq.com>
import os
import time
import sys
import optparse
from optparse import OptionParser
# ------------------------------------ 需要手动修改的配置
# 配置选项 sdk目录
SDK_DIR = '/data/python/test/oss/sdk'
# 资源父目录 (img的上一级目录)
IMG_DIR = '/data/python/test';
# 资源目录名称
RESOURCE_NAME = 'img'
# ------------------------------------ 需要手动修改的配置 end

# 添加sdk目录到package path中
sys.path.append(SDK_DIR)
# 引用sdk
from oss_api import *
from oss_xml_handler import *
os.chdir(IMG_DIR)

# ------------------------------------ oss参数
KEY = 'keyid'
SECRET = 'keysecret'
HOST = 'host'
BUCKET = 'bucket'
OSS_DIR = 'dirname'
DEBUG = False 
INTERVAL = 1
# ------------------------------------ oss参数 end 

def log(msg):

	if not os.path.isdir('log'):
		os.mkdir('log')

	fp = open('log/err.log', 'a')
	fp.write(msg + "\n")
	fp.close()

# 上传文件
def upload(object_file, source_file):
	object_file = OSS_DIR + '/' + object_file
	res = oss.put_object_from_file(bucket, object_file, source_file)

	if res.status / 100 != 2:
		log( "文件：%s 上传失败 (%s)" % (object_file, res.status) )
	else:
		print("文件：%s 上传成功 (%s)" % (object_file, res.status))

# 传输img目录名
def readFile(file_name):

	if os.path.isdir(file_name):
		# print('目录：%s' % file_name)
		for item in os.listdir(file_name):
			item_dir = file_name + '/' + item
			readFile(item_dir)
	else:
		# 文件的话，就上传到oss上
		# print('文件：%s' % file_name)
		# 普通方式上传文件
		upload(file_name, file_name)

def do():	
	readFile(RESOURCE_NAME)

if __name__ == '__main__':
	# 初始化oss对象 
	oss = OssAPI(HOST, KEY, SECRET)
	bucket = BUCKET 

	do()
