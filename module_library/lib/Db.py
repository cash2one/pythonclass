#/bin/env python
#encoding:utf8
# db类 mysql驱动
# author 	songmw
# date 		2015-11-19
import MySQLdb
import MySQLdb.cursors
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Mysql(object) :

	dbCursor = None
	dbCon = None

	# 传递参数为 数据库配置字典
	def __init__(self, db_config):

		try :
			self.dbCon = MySQLdb.connect(host=db_config['host'],user=db_config['user'],passwd=db_config['passwd'],db=db_config['db'],charset=db_config['charset'],cursorclass=MySQLdb.cursors.DictCursor)
			self.dbCursor = self.dbCon.cursor()

		except MySQLdb, e:
			print('error %d : %s' % (e.args[0], e.args[1]))
		except:
			print('db error')

	@staticmethod
	def escape(var):
		return MySQLdb.escape_string(var)

	# 执行sql
	def execute(self, sql):
		res = self.dbCursor.execute(sql)
		self.dbCon.commit()
		return res

	# 预处理 prepare
	def prepare(self, sql):
		res = self.dbCursor.execute(sql)
		return self

	# 提交
	def commit(self):
		self.dbCon.commit()
		return self

	# 获取插入sql的最后一条id
	def getLastId(self):
		return int(self.dbCursor.lastrowid)

	# 查询sql
	def query(self, sql):
		self.dbCursor.execute(sql)
		return self

	# 获取一条数据
	def findone(self):
		return self.dbCursor.fetchone()

	def fetchone(self):
		return self.findone()

	# 获取全部数据
	def findall(self):
		return self.dbCursor.fetchall()

	def fetchall(self):
		return self.findall()

	# 主动销毁
	def close(self):
		self.dbCursor.close()
		self.dbCon.close()

	# 析构方法
	def __del__(self):

		if self.dbCursor and self.dbCon:
			self.dbCursor.close()
			self.dbCon.close()
