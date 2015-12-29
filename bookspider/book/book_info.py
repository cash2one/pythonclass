#!/bin/env python
#encoding:utf8
#
# 蜘蛛抓取引擎
# author eric
from core.Db import Db
import SpiderEngine
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def existsBook(name):
	sql = 'select id from sg_book where name = "%s"'
	val = db.query(sql % name).fetchone()
	return val

def existsChapter(book_id, name):
	table = getChapterTable(book_id)
	sql = 'select id from %s where bk_id = "%s" and name = "%s"'
	val = db.query(sql % (table, book_id, name)).fetchone()
	return val

def existsSpiderChapter(book_id, name):
	table = getSpiderChapterTable(book_id)
	sql = 'select id from %s where bk_id = "%s" and name = "%s"'
	val = db.query(sql % (table, book_id, name)).fetchone()
	return val

def addBook(res):
	sql = 'insert into `sg_book`(`name`,`author`,`category`,`desc`,`write_status`,`img_url`) values("%s","%s","%s","%s","%s","%s")'
	db.execute(sql % (res['name'],res['author'],res['category'],res['desc'],res['write_status'],res['img_url']))
	return db.getLastId()

# 获取正式章节信息表
def getChapterTable(book_id):
	table = 'sg_chapter_%s' % (int(book_id) / 2000)
	sql = """
CREATE TABLE IF NOT EXISTS `%s` (                                        
`id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '章节id',  
`bk_id` int(10) unsigned NOT NULL COMMENT '作品id',              
`name` varchar(100) NOT NULL COMMENT '章节名称',               
`content` text NOT NULL COMMENT '章节内容',                    
`publish_time` datetime NOT NULL COMMENT '发布时间',
`ch_sort` int(10) unsigned NOT NULL COMMENT '章节排序',             
PRIMARY KEY (`id`),                                                
KEY `book_id` (`bk_id`)                                            
) ENGINE=InnoDB DEFAULT CHARSET=utf8 
	"""
	db.execute(sql % table)
	return table

# 获取采集章节信息
def getSpiderChapterTable(book_id):
	table = 'spider_chapter_%s' % (int(book_id) / 2000)
	sql = """
CREATE TABLE IF NOT EXISTS `%s` (                        
`id` int(10) unsigned NOT NULL AUTO_INCREMENT,         
`bk_id` int(10) unsigned NOT NULL,                     
`name` varchar(100) NOT NULL,                          
`spider_url` varchar(200) NOT NULL,                    
`is_spider` tinyint(3) unsigned NOT NULL DEFAULT '0',  
`ch_sort` int(10) unsigned NOT NULL COMMENT '章节排序',
PRIMARY KEY (`id`),                                    
KEY `book_id` (`bk_id`)                                
) ENGINE=InnoDB DEFAULT CHARSET=utf8
	"""
	db.execute(sql % table)
	return table

# 获取章节的顺序
def getMaxSort(book_id):
	chapter_table = getSpiderChapterTable(book_id)
	sql = 'select max(ch_sort) as ch_sort from %s where bk_id = "%s"'
	val = db.query(sql % (chapter_table, book_id)).fetchone()

	if not val['ch_sort']:
		return 1
	else:
		return int(val['ch_sort']) + 1

# 获取作品的最后一章名称
def getLastChapter(book_id):
	chapter_table = getSpiderChapterTable(book_id)
	sql = 'select name from %s where bk_id = "%s" order by ch_sort desc limit 1'
	val = db.query(sql % (chapter_table, book_id)).fetchone()

	return val['name']

# 插入章节到采集表中
def addSpiderChapter(book_id, res):
	chapter_table = getSpiderChapterTable(book_id)

	sql = 'insert into %s(ch_sort,bk_id,`name`,spider_url,is_spider) values'
	insert_val = [chapter_table]
	ch_sort = getMaxSort(book_id)

	for c in res['chapter']:

		# 如果章节存在，则不插入
		if existsSpiderChapter(book_id, c['name']):
			print('作品%s，章节%s已经存在' % (book_id, c['name']))
			continue

		sql += "('%s','%s','%s','%s',0),"
		insert_val.append(ch_sort)
		insert_val.append(book_id)
		insert_val.append(c['name'])
		insert_val.append(c['spider_url'])
		ch_sort += 1

	try:
		sql = sql[0:-1]
		# print(sql)
		# print(sql % tuple(insert_val))
		# sys.exit(0)
		db.execute(sql % tuple(insert_val))
		return True
	except:
		return False

# 插入章节到采集表，从作品的最后一章进行
def addSpiderChapterForEnd(book_id, res):
	chapter_table = getSpiderChapterTable(book_id)

	sql = 'insert into %s(ch_sort,bk_id,`name`,spider_url,is_spider) values'
	insert_val = [chapter_table]
	ch_sort = getMaxSort(book_id)
	ch_last_name = getLastChapter(book_id)

	is_ok = False
	for c in res['chapter']:

		# 当循环到采集的最后一章时，从下一个章节开始进行采集
		if c['name'] == ch_last_name:
			is_ok = True
			continue

		if is_ok:
			print("章节%s之前不存在，已经采集到" % c['name'])
			sql += "('%s','%s','%s','%s',0),"
			insert_val.append(ch_sort)
			insert_val.append(book_id)
			insert_val.append(c['name'])
			insert_val.append(c['spider_url'])
			ch_sort += 1

	try:
		sql = sql[0:-1]
		# print(sql)
		# print(sql % tuple(insert_val))
		# sys.exit(0)
		db.execute(sql % tuple(insert_val))
		return True
	except:
		return False


# 采集章节信息，插入到主章节信息中
def addChapter(book_id, chapter, ch_sort):

	if existsChapter(book_id, chapter['name']):
		print("作品%s下，该章节名已经存在%s" % (book_id, chapter['name']))
		return False

	table = getChapterTable(book_id)
	sql = 'insert into %s(bk_id,name,content,publish_time,ch_sort) values("%s","%s","%s","%s", "%s")'
	db.execute(sql % (table, book_id, chapter['name'], chapter['content'], chapter['publish_time'], ch_sort))
	print("作品：%s 添加章节 %s 成功!" % (book_id, chapter['name']))
	return True

# 刷新采集章节表状态
def refreshSpiderChapter(book_id, tid):
	table = getSpiderChapterTable(book_id)
	sql = 'update %s set is_spider = 1 where id = "%s"'
	db.execute(sql % (table, tid))

# 获取采集作品
def getSpiderBook():
	sql = 'select * from spider_book where spider_status = 1'
	val = db.query(sql).fetchall()
	return val

def do(name, url, engine):

	obj = __import__('SpiderEngine')
	s = getattr(obj, engine)(name, url)

	# s = SpiderEngine.biquge(name, url)
	try:
		info = s.spider()
		book_info = existsBook(info['name'])

		if book_info :
			print('该作品%s已经存在' % info['name'])
			book_id = book_info['id']

			# 从最后一章进行添加
			addSpiderChapterForEnd(book_id, info)
		else:
			book_id = addBook(info)
			print("已创建作品%s" % info['name'])
			addSpiderChapter(book_id, info)

		doChapter(book_id, engine)
		return True
	except:
		print("作品%s采集失败" % name)
		return False

def doChapter(book_id, engine):

	table = getSpiderChapterTable(book_id)
	sql = 'select * from %s where bk_id = "%s" and is_spider = 0 order by id asc'
	# print(sql % (table, book_id))
	chapters = db.query(sql % (table, book_id)).fetchall()

	for c in chapters:

		obj = __import__('SpiderEngine')
		s = getattr(obj, engine)(c['name'], c['spider_url'])

		# s = SpiderEngine.biquge(c['name'], c['spider_url'])
		try:
			chapter_info = s.chapter()
			boo = addChapter(book_id, chapter_info, c['ch_sort'])
			refreshSpiderChapter(book_id, c['id'])
		except:
			print('章节%s 添加失败' % c['name'])

# url to engine
def urlToEngine(url):
	url = url[url.find('.')+1:url.rfind('.')]
	if url == '365xs':
		url = 'lewen'
	return url

if __name__ == '__main__':
	db = Db()

	# books = [
	# 			# {'name':'斗破苍穹', 'url':'http://quanben.biquge.la/book/1/'},
	# 			# {'name':'佣兵天下', 'url':'http://quanben.biquge.la/book/3079/'},
	# 			# {'name':'极品家丁', 'url':'http://quanben.biquge.la/book/2737/'},
	# 			# {'name':'凡人修仙传', 'url':'http://quanben.biquge.la/book/4955/'},
	# 			# {'name':'傲世九重天', 'url':'http://quanben.biquge.la/book/3130/'},
	# 			# {'name':'校花的贴身高手', 'url':'http://www.365xs.org/book/3780/index.html', 'engine':'lewen'},
	# 			{'name':'花千骨', 'url':'http://quanben.biquge.la/book/15437/', 'engine':'biquge'},
	# 		]
	
	books = getSpiderBook()

	for b in books:

		if not b['spider_engine']:
			engine = urlToEngine(b['spider_url'])
		else:
			engine = b['spider_engine']

		do(b['name'], b['spider_url'], engine)