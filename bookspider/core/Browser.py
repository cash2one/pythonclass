#!/bin/env python
#encoding:utf8
#
# 模拟浏览器行为类
#
# author 	eric
import mechanize
import cookielib

# 模拟浏览器行为
class Browser:
	def __init__(self, url):
		self.url = url
	# 获取一个打开的对象
	def getReadInstance(self):
		# 设置浏览器
		br = mechanize.Browser()
		cj = cookielib.LWPCookieJar()
		br.set_cookiejar(cj)
		br.set_handle_equiv(True)
		# br.set_handle_gzip(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 60)
		br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0')]
		
		try :
			r = br.open(self.url)
			return r
		except:
			return False