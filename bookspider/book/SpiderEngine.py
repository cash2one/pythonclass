#!/bin/env python
#encoding:utf8
#
# 蜘蛛抓取引擎
# author eric
from core.Db import Db
import urllib2
import BeautifulSoup
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class BaseSpider(object):

	def __init__(self, name, url):
		self.name = name
		self.url = url
		self.html = None
		self.soup = None
		self._init()

	def _init(self):
		try:
			header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
			req = urllib2.Request(self.url, headers=header)
			self.html = urllib2.urlopen(req, timeout=20).read()

			# 去除script
			re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
			self.html = re_script.sub('', self.html)

			self.soup = BeautifulSoup.BeautifulSoup(self.html)
		except:
			print("作品：%s， 采集失败，地址：%s" % (self.name, self.url))
			return False

	# 采集主程序，返回内容有
	"""
		{
			'name' : '',
			'author' : '',
			'category' : '',
			'desc' : '',
			'write_status' : '',
			'img_url' : '',
			'chapter' : [{'name':'', 'spider_url':''}, ],
		}
	"""
	def spider(self):
		pass

# www.365xs.org 乐文引擎
class lewen(BaseSpider):
	def __init__(self, name, url):
		super(lewen, self).__init__(name, url)

	# 采集作品信息
	def spider(self):
		bread = self.soup.find('ul', {'class':'bread-crumbs'}).findAll('li')
		bk_name = bread[2].text
		category = bread[1].text
		author = self.soup.find('table', {'class':'ui_tb1'}).find('em').text
		author = author.replace('作者：', '')
		desc = str(self.soup.find('div', {'class':'intro'}))
		desc = desc.replace('<div class="intro" style="text-indent:2em;">', '')
		desc = desc.replace('</div>', '')
		desc = desc.strip()

		img_url = self.soup.find('div', {'class':'pic'}).find('img')['src']
		tr = self.soup.find('table', {'class':'ui_tb1'}).findAll('tr')
		write_status = tr[4].findAll('td')[2].text
		write_status = write_status.replace('小说状态：', '')

		if write_status == '连载中':
			write_status = 0
		else:
			write_status = 1

		chapter_url = self.soup.find('span', {'class':'btopt'}).find('a')['href']
		domain = self.url[0: self.url.find('/', 8)]
		chapter_url = domain + chapter_url

		try:
			header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
			req = urllib2.Request(chapter_url, headers=header)
			chapter_html = urllib2.urlopen(req, timeout=20).read()
			chapter_html = chapter_html.replace('<!--dt id="qw" name="qw">', '')
			chapter_html = chapter_html.replace('</dt--!>', '')
			soup = BeautifulSoup.BeautifulSoup(chapter_html)
			chapter_list = []
			chapters = soup.find('ul', {'class':'chapterlist'}).findAll('a')

			for c in chapters:
				c_url = chapter_url + c['href']
				chapter_list.append({'name':c.text, 'spider_url':c_url})
		except:
			print("作品%s获取章节信息失败" % bk_name)
			return False

		res = {}
		res['name'] = bk_name
		res['author'] = author
		res['category'] = category
		res['desc'] = desc
		res['write_status'] = write_status
		res['img_url'] = img_url
		res['chapter'] = chapter_list

		return res

	# 采集章节内容
	def chapter(self):

		res = {}
		res['name'] = self.name
		cont = self.soup.find('div', id="content")
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

		res['content'] = cont
		res['publish_time'] = time.strftime('%Y-%m-%d %H:%M:%S')

		return res


# www.biquge.la 采集引擎
class biquge(BaseSpider):

	def __init__(self, name, url):
		super(biquge, self).__init__(name, url)

	# 采集作品信息
	def spider(self):
		bk_name = self.soup.find('div', id="info").find('h1').text
		author = self.soup.find('div', id="info").findAll('p')[0].text
		author = author.replace('作&nbsp;&nbsp;&nbsp;&nbsp;者：', '')
		category = self.soup.find('meta', {"property":"og:novel:category"})['content']
		desc = str(self.soup.find('div', id="intro"))
		desc = desc.replace('<div id="intro">', '')
		desc = desc.replace('</div>', '')
		desc = desc.strip()

		img_url = self.soup.find('div', id="fmimg").find('img')['src']
		write_status = self.soup.find('div', id="info").findAll('p')[3].text
		# 没有最新章节，则为完结，否则为连载
		if write_status == -1:
			write_status = 1
		else:
			write_status = 0

		# print(write_status)
		# print(img_url)
		# print(desc)
		# print(bk_name)
		# print(category)
		# print(author)

		chapters = self.soup.find('div', id="list").findAll('dd')

		chapter_list = []
		for c in chapters:
			if not c.find('a'):
				continue

			chapter_url = self.url + c.find('a')['href']
			chapter_list.append({'name':c.text, 'spider_url':chapter_url})

		# print(chapter_list)

		res = {}
		res['name'] = bk_name
		res['author'] = author
		res['category'] = category
		res['desc'] = desc
		res['write_status'] = write_status
		res['img_url'] = img_url
		res['chapter'] = chapter_list

		return res


	# 采集章节内容
	def chapter(self):

		res = {}
		res['name'] = self.name
		cont = self.soup.find('div', id="content")
		cont = str(cont)
		cont = cont.replace('<div id="content">', '')
		cont = cont.replace('</div>', '')
		cont = cont.replace('<script>readx();</script>', '')
		cont = cont.strip()
		cont = Db.escape(cont)

		res['content'] = cont
		res['publish_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
		return res
