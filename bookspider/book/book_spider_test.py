#!/bin/env python
#encoding:utf8
#
# 蜘蛛抓取引擎 测试的test
# author eric
from core.Db import Db
import urllib2
import BeautifulSoup
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def testChapterContent(url):
	req = urllib2.Request(url)
	html = urllib2.urlopen(req).read()
	re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
	html = re_script.sub('',html)
	soup = BeautifulSoup.BeautifulSoup(html)
	cont = soup.find('div', id="content")

	del_dev = cont.findAll('div')

	for del_item in del_dev:
		if del_item.has_key('class') or del_item.has_key('id'):
			del_item.extract()

	cont = str(cont)
	cont = cont.replace('<div id="content">', '')
	cont = cont.replace('</div>', '')
	cont = cont.replace('<div>', '')
	cont = cont.strip()
	cont = Db.escape(cont)
	print(cont)
	sql = 'insert into sg_chapter_0(bk_id,name,content,publish_time,ch_sort) values("%s","%s","%s","%s", "%s")'
	print(sql % ('9', 'test', cont, '2015-09-13 23:25:32', '1'))
	db.execute(sql % ('9', 'test', cont, '2015-09-13 23:25:32', '1'))

if __name__ == '__main__':
	
	db = Db()
	url = 'http://www.biquge.la/book/3607/2737400.html'
	testChapterContent(url)


	
	
	
