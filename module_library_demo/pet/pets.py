#!/bin/env python
# encoding:utf8
#
# 采集宠物的全部数据
#
# author songmw<imphp@qq.com>
# date 	 2016.01.09
import os
import sys
import re
import urllib2
import BeautifulSoup
import time

path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(path + '/../')

from Base import *

debug = False

# 单例模式
class Singleton(object):

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

# 创建蜘蛛对象
class Spider(Singleton):

    def __init__(self, url):
        self.url = ''
        self.html = ''
        self.soup = None

        try:
            self.url = url
            header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib2.Request(self.url, headers=header)
            self.html = urllib2.urlopen(req, timeout=20).read()
            re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
            html = re_script.sub('', self.html)
            self.soup = BeautifulSoup.BeautifulSoup(html)

        except :
            print("地址 ： %s 解析失败！" % self.url)

    def getSoupInstance(self):
        return self.soup

# 百度风云榜-宠物采集
def bdTop():
    url = 'http://top.baidu.com/buzz?b=24'
    spi = Spider(url)
    soup = spi.getSoupInstance()

    table = soup.findAll('table', {'class':'list-table'})[0]
    trline = table.findAll('tr')

    sql = 'insert into data_bd_pet(name, detail_url, search_num) values '
    dogs = []
    for item in trline:
        name = item.findAll('a', {'class':'list-title'})
        if not name:
            continue

        dogname = name[0].text
        search_num = item.findAll('td', {'class':'last'})[0].text
        detail_url = item.findAll('a', {'class':'icon-search icon-xiang-imp'})[0]['href']
        detail_url = str(detail_url)
        detail_url = 'http://top.baidu.com' + detail_url[1:len(detail_url)]
        dogs.append(dogname)
        dogs.append(detail_url)
        dogs.append(search_num)
        sql += '("%s", "%s", "%s"),'

    sql = sql[0:-1]
    db.execute(sql % tuple(dogs))

# dog126-狗狗种类采集
def dog126():

    url = 'http://www.dog126.com/ggjs.html'
    spi = Spider(url)
    soup = spi.getSoupInstance()
    dogs_spider = soup.findAll('div', {'id':'showli_75'})
    dogs = []

    sql = 'insert into data_dog126_pet(dog_id, name, avatar) values '
    for item in dogs_spider:
        name = item.findAll('dd', {'class':'jsdd'})[0].text
        avatar = 'http://www.dog126.com/' + str(item.find('img')['src'])
        detail_url = item.findAll('dd', {'class':'jsdd'})[0].find('a')['href']
        detail_url = 'http://www.dog126.com/' + str(detail_url)

        end_num = avatar.rfind('.')
        start_num = avatar.rfind('/')
        dog_id = avatar[start_num+1: end_num]
        dogs.append(dog_id)
        dogs.append(name)
        dogs.append(avatar)
        sql += '("%s", "%s", "%s"),'

    sql = sql[0:-1]
    db.execute(sql % tuple(dogs))

# dog126-狗狗信息数据分析
# param str url
# return dict
def dog126infoparse(url):
    res = {}
    spi = Spider(url)
    soup = spi.getSoupInstance()
    detail_base = soup.findAll('div', {'class':'Details_main'})[0]
    # print(detail_base)

    en_name = detail_base.findAll('li')[1].text
    res['en_name'] = str(en_name).replace('英&nbsp;文名：', '')

    birth_city = detail_base.findAll('li')[2].text
    res['birth_city'] = str(birth_city).replace('产&nbsp; &nbsp;地：', '')

    age = detail_base.findAll('li')[3].text
    res['age'] = str(age).replace('寿&nbsp; &nbsp;命：', '')

    alias = detail_base.findAll('li')[4].text
    res['alias'] = str(alias).replace('别&nbsp; &nbsp;名：', '')

    man_high = detail_base.findAll('li')[5].text
    res['man_high'] = str(man_high).replace('雄性身高：', '')

    woman_high = detail_base.findAll('li')[6].text
    res['woman_high'] = str(woman_high).replace('雄性身高：', '')

    zhpj = detail_base.findAll('li')[7].find('em')['style']
    res['zhpj'] = str(zhpj).replace('width:', '')

    detail_pj = soup.findAll('div', {'class':'pet-feature-dea'})[0].findAll('li')
    # print(detail_pj)

    nianrenchengdu = detail_pj[0].find('em')['style']
    res['nianrenchengdu'] = str(nianrenchengdu).replace('width:', '')

    xjcd = detail_pj[1].find('em')['style']
    res['xjcd'] = str(xjcd).replace('width:', '')

    dmcd = detail_pj[2].find('em')['style']
    res['dmcd'] = str(dmcd).replace('width:', '')

    twcd = detail_pj[3].find('em')['style']
    res['twcd'] = str(twcd).replace('width:', '')

    mrcd = detail_pj[4].find('em')['style']
    res['mrcd'] = str(mrcd).replace('width:', '')

    dxhys = detail_pj[5].find('em')['style']
    res['dxhys'] = str(dxhys).replace('width:', '')

    dsrys = detail_pj[6].find('em')['style']
    res['dsrys'] = str(dsrys).replace('width:', '')

    dwys = detail_pj[7].find('em')['style']
    res['dwys'] = str(dwys).replace('width:', '')

    ydl = detail_pj[8].find('em')['style']
    res['ydl'] = str(ydl).replace('width:', '')

    kxlx = detail_pj[9].find('em')['style']
    res['kxlx'] = str(kxlx).replace('width:', '')

    kscd = detail_pj[10].find('em')['style']
    res['kscd'] = str(kscd).replace('width:', '')

    nhcd = detail_pj[11].find('em')['style']
    res['nhcd'] = str(nhcd).replace('width:', '')

    nrcd = detail_pj[12].find('em')['style']
    res['nrcd'] = str(nrcd).replace('width:', '')

    cssyd = detail_pj[13].find('em')['style']
    res['cssyd'] = str(cssyd).replace('width:', '')

    details = soup.findAll('div', {'class':'option_box'})[0]
    res['details'] = str(details)

    return res

# dog126-狗狗基础信息采集
def dog126info():

    if debug:
        sql = 'select id,dog_id from data_dog126_pet order by dog_id asc limit 1'
    else:
        sql = 'select id,dog_id from data_dog126_pet order by dog_id asc'

    dogs = db.query(sql).fetchall()
    info_url = 'http://www.dog126.com/doginfo_%s.html'

    for item in dogs:
        dog_id = int(item['dog_id'])
        url = info_url % dog_id
        print('正在采集 : %s' % url)
        info = {}
        info = dog126infoparse(url)

        sql = '''update data_dog126_pet set
        details = "%s",
        en_name = "%s",
        birth_city = "%s",
        age="%s",
        alias="%s",
        man_high="%s",
        woman_high="%s",
        zhpj="%s",
        nianrenchengdu="%s",
        xjcd="%s",
        dmcd="%s",
        twcd="%s",
        mrcd="%s",
        dxhys="%s",
        dsrys="%s",
        dwys="%s",
        ydl="%s",
        kxlx="%s",
        kscd="%s",
        nhcd="%s",
        nrcd="%s",
        cssyd="%s" where id = "%d"'''

        db.execute(sql %
        (db.escape(info['details']),
        db.escape(info['en_name']),
        db.escape(info['birth_city']),
        db.escape(info['age']),
        db.escape(info['alias']),
        db.escape(info['man_high']),
        db.escape(info['woman_high']),
        db.escape(info['zhpj']),
        db.escape(info['nianrenchengdu']),
        db.escape(info['xjcd']),
        db.escape(info['dmcd']),
        db.escape(info['twcd']),
        db.escape(info['mrcd']),
        db.escape(info['dxhys']),
        db.escape(info['dsrys']),
        db.escape(info['dwys']),
        db.escape(info['ydl']),
        db.escape(info['kxlx']),
        db.escape(info['kscd']),
        db.escape(info['nhcd']),
        db.escape(info['nrcd']),
        db.escape(info['cssyd']),
        int(item['id'])))

def dog126artparse(url):

    res = {}
    spi = Spider(url)
    soup = spi.getSoupInstance()

    cont = soup.findAll('div', {'class':'artCon'})[0]
    title = cont.find('h1').text

    if title == '':
        return False

    res['time'] = cont.findAll('p', {'class':'artInfo'})[0].find('span').text
    res['title'] = title

    content = cont.findAll('div', {'class':'artCon_content'})[0]
    del_tag = content.findAll('div', {'style':'margin-left:40px'})[0]
    del_tag.extract()
    res['content'] = str(content)

    category = soup.findAll('div', {'class':'Article_nav'})[0].findAll('a')[1].text
    res['category'] = category

    return res

# 采集资讯文章
def dog126art():

    url_template = 'http://www.dog126.com/news_%d.html'

    for i in xrange(35000):
        url = url_template % i
        info = {}

        try:
            info = dog126artparse(url)

            if not info:
                print('%s 地址采集失败' % url)
                continue

            sql = '''insert into data_dog126_message(title,category,content,time)
            values("%s", "%s", "%s", "%s")'''

            db.execute(sql % (db.escape(info['title']), db.escape(info['category']),
            db.escape(info['content']), db.escape(info['time'])))


            time.sleep(1)
        except:
            print('%s 地址采集失败' % url)

if __name__ == '__main__':

    db = getDbInstance()

    dog126art()
