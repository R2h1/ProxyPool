'''
为爬虫提供稳定可用的代理ip的接口
	根据协议类型和域名，提供随机的稳定可用ip的服务
	根据协议类型和域名，提供获取多个高可用代理ip的服务
	给指定ip上追加不可用域名的服务
'''
from flask import Flask
from flask import request
import json

from proxies_db.mongo_pool import MongoPool

from settings import PROXIES_MAX_COUNT


class ProxyApi(object):

	def __init__(self):

		self.app = Flask(__name__)

		#操作数据库的对象
		self.mongo_pool =  MongoPool()

		#获取接口url中参数
		@self.app.route('/random')
		def random():
			protocol = request.args.get('protocol')
			domain = request.args.get('domain')
			proxy = self.mongo_pool.random_proxy(protocol,domain,count = PROXIES_MAX_COUNT)

			if protocol:
				return '{}://{}:{}'.format(protocol,proxy.ip,proxy.port)
			else:
				return '{}:{}'.format(proxy.ip,proxy.port)

		@self.app.route('/proxies')
		def proxies():
			protocol = request.args.get('protocol')
			domain = request.args.get('domain')
			proxies =self.mongo_pool.get_proxies(protocol,domain,count =PROXIES_MAX_COUNT)
			#proxies是proxy对象构成的列表，需要转换为字典的列表

			proxies_dict_list =[proxy.__dict__ for proxy in proxies]
			return json.dumps(proxies_dict_list)
		
		@self.app.route('/disabl_domain')
		def disable_domain():
			ip = request.args.get('ip')
			domain = request.args.get('domain')

			if ip is None:
				return '请提供ip参数'
			if domain is None:
				return '请提供域名domain参数'
			self.mongo_pool.add_disable_domain(ip,domain)
			return '{} 禁用域名 {} 成功'.format(ip,domain)

	def run(self,debug):
		self.app.run('0.0.0.0',port = 7474,debug = debug)

	@classmethod
	def start(cls,debug = None):
		proxy_api = cls()
		proxy_api.run(debug = debug)

if __name__ == '__main__':
	ProxyApi.start(debug = True)
	#proxy_api = ProxyApi()
	#proxy_api.run(debug = True)