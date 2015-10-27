#!/bin/env python
# encoding:utf8
# 
# 解析日志类
#
# author 	songmw
# date 		2015-07-27
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')
	

# 读取一行信息
# 返回字典类型
# dict['university_id'] = uid
# dict['user_id'] = userid
# dict['time'] = time
# dict['ip'] = ip
def parseLine(line):
	res = {}

	# 从右开始获取 [ 字符
	log_content = line.rsplit('[', 1)[1]
	log_content = log_content[1:len(log_content)-2]

	log_dict = log_content.split('##')

	# 大学的统计 大学id不存在，或者 大学id 数值过大，都返回False
	try:
		if log_dict[0] != 'university_stat' or not log_dict[1] or int(log_dict[1]) > 3319 :
			return False
	except:
		return False

	res['university_id'] = int(log_dict[1])
	res['user_id'] = int(log_dict[2])
	res['time'] = log_dict[3]
	res['ip'] = log_dict[4]

	return res

# 格式化时间
# 将字符串时间，转换为 datetime类型
def parseDateTime(stringDate, format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(stringDate ,"%Y-%m-%d %H:%M:%S")))
