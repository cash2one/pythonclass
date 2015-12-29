#!/bin/env python
# encoding:utf8
# 导出英语单词
# author songmw<imphp@qq.com>
# date 	 2015.11.19
import os
import sys
import json

# 必添加设置加载路径为 上一级目录
path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(path + '/../')

# 加载必须的类库
from Base import *

debug = False

# 获取动名词
def getWordAction(word_id):

	sql = 'select * from yingyu_word.gk_word_action where uid = %d'
	act = db.query(sql % word_id).fetchall()
	res = []

	for item in act:
		tmp = {}
		tmp['type'] = item['type']
		tmp['content'] = item['content']
		res.append(tmp)
	return res

# 获取词性变化
def getWordChange(word_id):

	sql = 'select * from yingyu_word.gk_word_change where uid = %d'
	change = db.query(sql % word_id).fetchall()
	res = {}

	for item in change:
		if item['content'] not in res:
			res[item['content']] = item['type']
	return res

# 获取例子
def getWordExample(word_id):

	sql = 'select * from yingyu_word.gk_word_example where uid = %d'
	example = db.query(sql % word_id).fetchall()
	res = []

	for item in example:
		tmp = {}
		tmp['example'] = item['example']
		tmp['translate'] = item['translate']
		tmp['voice'] = item['voice']
		res.append(tmp)
	return res

# 获取单词的列表
def getEnWords():

	if debug:
		sql = 'select * from yingyu_word.gk_word_user where status = 1 order by id asc limit 5'
	else:
		sql = 'select * from yingyu_word.gk_word_user where status = 1 order by id asc'

	words = []
	data = db.query(sql).fetchall()

	sql = 'insert into beikao.prepare_word(type,content,status) values '
	insert_val = []

	for item in data:
		word_id = int(item['id'])

		# 获取动名词
		act = []
		act = getWordAction(word_id)

		# 获取词性变化 
		cha = {}
		cha = getWordChange(word_id)

		# 获取例子
		example = []
		example = getWordExample(word_id)

		word = {}
		voice = item['enMp3']
		voice = voice.split('&&')
		word['voice'] = voice[0]
		word['yinbiao'] = voice[1]
		word['name'] = item['name']
		word['action'] = act
		word['change'] = cha
		word['example'] = example

		word_json = json.dumps(word)
		word_json = db.escape(word_json)
		# print type(word_json)
		# print type(json.loads(word_json))
		sql += '(1, "%s", 1),'
		insert_val.append(word_json)

	sql = sql[0:-1]
	db.execute(sql % tuple(insert_val))

if __name__ == '__main__' :
	
	db = getDbInstance()

	getEnWords()

