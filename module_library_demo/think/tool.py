#!/bin/env python
# encoding:utf8
#
# 快捷创建gkp项目 
#
# author songmw<imphp@qq.com>
# date 	 2015.11.19
import os
import sys
import commands
import re
import time

path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(path + '/../')

from Base import *

debug = True
	
# 核心类库 api的模板
def ApiTemplate(tem):

	# 创建时间
	now = time.strftime('%Y-%m-%d %H:%M:%S')
	# 命名空间
	namespace = 'Zcore\\Api' + tem['namespace']
	# 类名
	classname = tem['classname']
	# 作者
	author = tem['author']
	# 联系方式
	email = tem['email']
	# 类描述
	classdesc = tem['classdesc']

	template_var = (classdesc, author, email, now, namespace, classname)

	template = """
<?php
/**
 * %s
 *
 * @author 	%s<%s>
 * @date 	%s
 */
namespace %s;
use Zcore\Tool\Log;

class %s {
	
	static protected $key = '缓存key';
	static protected $expire = 10800 ;	// 3小时	
	
	/** 
	 * 初始化方法
	 */
	public function __construct()
	{

	
	}

	private function _loadFromCache()
	{


	}

	private function _loadFromDb()
	{


	}
	
	/**
	 * 获取信息
	 */
	public function getInfo()
	{


	}
	
	/**
	 * 清除缓存
	 */
	static public function clear()
	{


	}
}
""" 
	return template % template_var

if __name__ == '__main__' :

	try:
		# 获取www信息
		user_info = commands.getoutput('id www')
		com = re.compile(r"\=(.*?)\(")
		val = com.findall(user_info)
		uid = int(val[0])
		gid = int(val[1])
	except:
		print('未发现www用户')
		sys.exit(0)

	try:
		config = CONF_PATH + '/tool.ini'
		confIns = loadConf(config)
		
		print( '*' * 22 + '  快速创建项目工具  ' + '*' * 22)		
		print( '* 类库核心文件需要选择核心类库')		
		print( '* 项目文件，选择项目和分组后，输入控制器全名或者service全名即可')		
		print( '* 多文件，用 逗号 分割；目录用 / 分割，只允许一个层级目录')
		print( '* -- 暂时只支持创建core/api/下的类文件')
		print( '*' * 20 + '************************' + '*' * 20)		
		create_type = int(raw_input('[1创建核心类库文件|2创建项目文件]请输入：'));


		if create_type == 1:
			dir_path = confIns.get('think', 'core')
			sec_type = int(raw_input('[1Api|2Behavior|3Model|4Tool]请输入：'))
			file_name = str(raw_input('请输入文件的名称，含有目录的用 / 分割，注意大小写：'))
			class_desc = str(raw_input('请输入类描述，允许后期再填写：'))

		if sec_type == 1:
			dir_path = dir_path + '/Api'
		elif sec_type == 2:
			dir_path = dir_path + '/Behavior'
		elif sec_type == 3:
			dir_path = dir_path + '/Model'
		elif sec_type == 4:
			dir_path = dir_path + '/Tool'
		else:
			print('必须要选择创建的核心类库类型！')
			sys.exit(0)

		if not file_name:
			print('必须要填写创建的文件名称！')

		elif create_type == 2:
			print('太麻烦，暂时只支持类库的文件创建')
			sys.exit(0)
			dir_path = confIns.get('think', 'project')
			project_name = str(raw_input('请输入项目名称：'))
			group_name = str(raw_input('请输入分组名称：'))
			file_name = str(raw_input('请输入文件全名（需要保护Controller/Service）：'))

		# 分析文件
		tmp = file_name
		file_path = ''
		if tmp.find('/') > 0:
			tmp = tmp.split('/')
			file_path = tmp[0] + '/'
			file_name = tmp[1]
		else:
			file_name = tmp

		realpath_dir = dir_path + '/' + file_path

		# 创建目录，改权限为www
		if not os.path.exists(realpath_dir):
			os.mkdir(realpath_dir)
			os.chown(realpath_dir, uid, gid)

		realpath_file = dir_path + '/' + file_path + file_name

		if os.path.exists(realpath_file):
			print("%s 已经存在！" % realpath_file)
			sys.exit(0)

		# 获取传递模板的参数
		tem = {}
		tem['author'] = confIns.get('copyright', 'author')
		tem['email'] = confIns.get('copyright', 'email')
		file_name = file_name.split('.')
		file_name = file_name[0]
		tem['namespace'] = ''
		tem['classdesc'] = class_desc

		if file_path:
			tem['namespace'] = '\\' + file_path[0:-1]

		tem['classname'] = file_name.replace('Controller', '')
		template = ApiTemplate(tem)

		# print template
		# sys.exit(0)

		# 写入文件
		fp = open(realpath_file, 'a')
		fp.write(template)
		fp.close()

		# 修改权限
		os.chown(realpath_file, uid, gid)
		os.chmod(realpath_file, 755)

		print('已经创建完毕！')

	except Exception, e:
		print(e.args[0])