'''
针对proxies集合进行数据库的增删改查的操作，并提供代理api使用
'''
import random
import pymongo
import sys

sys.path.append("..")
from settings import MONGO_URL
from proxies_utils.log import logger
from dbmodle import Proxy

class MongoPool(object):

	def __init__(self):
		#连接数据库
		self.client = pymongo.MongoClient(MONGO_URL)
		#获取操作字典集
		self.proxies = self.client['proxies_pool']['proxies']

	def __del__(self):
		#关闭数据库连接
		self.client.close()

	def insert(self,proxy):
		'''
		代理ip插入方法
		'''
		count = self.proxies.count_documents({'_id':proxy.ip})
		if count == 0:
			#Proxy对象转换为字典
			proxy_dict = proxy.__dict__
			#主键
			proxy_dict['_id'] = proxy.ip
			#向proxies字典集中插入代理ip
			self.proxies.insert_one(proxy_dict)
			logger.info('插入新的代理：{}'.format(proxy))
		else:
			logger.warning('已经存在的代理{}'.format(proxy))

	def update(self,proxy):
		'''
		修改更新数据库中代理ip
		'''
		self.proxies.update_one({'_id':proxy.ip},{'$set':proxy.__dict__})
		logger.info('更新代理ip：{}'.format(proxy))

	def delete(self,proxy):
		'''
		删除数据库中代理ip
		'''
		self.proxies.delete_one({'_id':proxy.ip})
		logger.info('删除代理ip:{}'.format(proxy))

	def find_all(self):
		'''
		查询数据库中所有的代理ip
		'''
		cursor = self.proxies.find()

		for item in cursor:
			#删除_id键值对
			item.pop('_id')
			proxy = Proxy(**item)
			#生成器yield
			yield proxy

	def limit_find(self,conditions = {},count = 0):
		'''根据条件进行查询, 
		可以指定查询数量, 先分数降序, 速度升序排, 
		保证优质的代理IP在上面'''
		cursor = self.proxies.find(conditions,limit = count).sort([
			('score',pymongo.DESCENDING),('speed',pymongo.ASCENDING)])
		#接受查询所得代理IP
		proxy_list = []

		for item in cursor:
			itme.pop('_id')
			proxy = Proxy(**item)
			proxy_list.append(proxy)
		return proxy_list

	def get_proxies(self,protocol =None,domain = None,nick_type =0,count = 0):
		'''
		实现根据协议类型和要访问网站的域名, 获取代理IP列表
		'''
		conditions = {'nike_type':nick_type}
		if protocol is None:
			conditions['protocol'] = 2
		elif protocol.lower() == 'http':
			conditions['protocol'] ={'$in':[0,2]}
		else:
			conditons['protocol'] ={'$in':[1,2]}

		if domain:
			conditons['disable_domains'] = {'$nin':[domain]}

		return self.limit_find(conditions,count = count)

	def random_proxy(self,protocol = None,domain =None,count = 0,nick_type =0):
		'''
		根据协议类型 和 要访问网站的域名, 随机获取一个代理IP
		'''
		proxy_list = self.get_proxies(protocol =protocol,domain = domain ,count = count ,nick_type =nick_type)

		return random.choice(proxy_list)

	def add_disable_domain(self,ip,domain):
		'''
		把指定域名添加到指定IP的disable_domain列表中,没有才添加
		'''
		count = self.proxies.count_documents({'_id':ip,'disable_domains':domain})
		if count == 0:
			self.proxies.update_one({'_id':ip},{'$push':{'disable_domains':domain}})



if __name__ == '__main__':
	mongo = MongoPool()
	#插入测试
	proxy = Proxy('202.104.113.32','53281')
	mongo.insert(proxy)

	#更新测试
	#proxy = Proxy('202.104.113.32','8888')
	#mongo.update(proxy)

	#删除测试
	#proxy = Proxy('202.104.113.32','8888')
	#mongo.delete(proxy)

	#查询所有测试
	#for proxy in mongo.find_all():
		#print(proxy)





	
