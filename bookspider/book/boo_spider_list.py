#!/bin/env python
#encoding:utf8
#
# 采集biquge首页的最近更新 和 最新添加小说
# author eric
import sys
sys.path.pop()
sys.path.pop()
sys.path.append('/data/python/spider/book_spider')
from core.Db import Db
import urllib2
import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')

def getSoup():

	try:
		header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
		rep = urllib2.Request('http://www.biquge.la', headers=header)
		html = urllib2.urlopen(rep).read()
		soup = BeautifulSoup.BeautifulSoup(html)
		return soup
	except:
		print("首页打开失败")
		return False

def existsBook(name):
	sql = 'select id from spider_book where name = "%s"'
	val = db.query(sql % name).fetchone()
	return val

def do(soup):
	books = []
	last_update_book = soup.findAll('div', {'class':'l'})
	last_update_book = last_update_book[1].findAll('span', {'class':'s2'})

	for item in last_update_book :
		book_item = {}
		book_href = item.find('a')['href']
		book_name = item.find('a').text
		book_item['spider_url'] = domain + book_href
		book_item['name'] = book_name
		books.append(book_item)

	last_update_book = soup.findAll('div', {'class':'r'})
	last_update_book = last_update_book[1].findAll('span', {'class':'s2'})

	for item in last_update_book :
		book_item = {}
		book_href = item.find('a')['href']
		book_name = item.find('a').text
		book_item['spider_url'] = domain + book_href
		book_item['name'] = book_name
		books.append(book_item)

	sql = 'insert into spider_book(name, spider_url, spider_engine) values '
	insert_val = []
	for book in books:

		if existsBook(book['name']):
			# print("作品：%s已经存在啦" % book['name'])
			continue

		sql += '("%s", "%s", "%s"),'
		insert_val.append(book['name'])
		insert_val.append(book['spider_url'])
		insert_val.append('biquge')

	if len(insert_val) > 0:
		sql = sql[0:-1]
		db.execute(sql % tuple(insert_val))
	
if __name__ == '__main__':

	domain = 'http://www.biquge.la'

	db = Db()
	soup = getSoup()

	if soup :
		do(soup)