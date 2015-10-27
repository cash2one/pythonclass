#/bin/env python
#encoding:utf8
# 
# db 类
#
# author 	songmw
# date 		2015-07-27
import MySQLdb
import MySQLdb.cursors
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Db(object) :

	dbCursor = None
	dbCon = None
	dbConfig = '配置文件地址'

	__host = None
	__dbname = None
	__user = None
	__passwd = None
	__charset = None

	# 取消单例模式
	# def __new__(cls, *args, **kw):

	# 	if not hasattr(cls, '_instance'):
	# 		cls._instance = super(Db, cls).__new__(cls, *args, **kw)
	# 	return cls._instance

	def __init__(self):

		self.__getConfig()
		try :
			self.dbCon = MySQLdb.connect(host=self.__host,user=self.__user,passwd=self.__passwd,db=self.__dbname,charset=self.__charset,cursorclass=MySQLdb.cursors.DictCursor)
			self.dbCursor = self.dbCon.cursor()
		except MySQLdb, e:
			print('error %d : %s' % (e.args[0], e.args[1]))

	# 获取db配置文件
	def __getConfig(self):

		cp = ConfigParser.ConfigParser()
		cp.read(self.dbConfig)
		self.__host = cp.get('db', 'host')
		self.__dbname = cp.get('db', 'dbname')
		self.__user = cp.get('db', 'user')
		self.__passwd = cp.get('db', 'passwd')
		self.__charset = cp.get('db', 'charset')

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

		self.dbCursor.close()
		self.dbCon.close()
