'''
创建RunSpider类
	run方法运行爬虫, 作为运行爬虫的入口,获取爬虫列表并运行，检测代理IP，可用,写入数据库并处理爬虫内部异常
	使用协程异步来执行每一个爬虫任务, 以提高抓取代理IP效率
	使用schedule模块, 实现每隔一定的时间, 执行一次爬取任务
'''

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

import importlib
import sys,time
import schedule
sys.path.append('../')
from settings import PROXIES_SPIDERS,SPIDERS_RUN_INTERVAL
from proxy_validate.httpbin_validator import check_proxy
from proxies_db.mongo_pool import MongoPool
from proxies_utils.log import logger

class RunSpider(object):

	def __init__(self):

		self.mongo_pool = MongoPool()
		self.coroutine_pool = Pool()

	def get_spider_from_settings(self):
		'''
		获取配置文件中的具体爬虫列表创建对象
		'''
		for full_class_name in PROXIES_SPIDERS:
			module_name,class_name = full_class_name.rsplit('.',maxsplit =1)
			#动态导入模块
			module = importlib.import_module(module_name)

			cls = getattr(module,class_name)
			spider = cls()
			yield spider

	def run(self):
		'''
		遍历爬虫对象，执行get_proxies方法
		'''
		spiders = self.get_spider_from_settings()
		for spider in spiders:
			self.coroutine_pool.apply_async(self.__run_one_spider,args=(spider,))
		#当前线程等待爬虫执行完毕
		self.coroutine_pool.join()
	

	def __run_one_spider(self,spider):
		try:
			check_ip_count = 0
			for proxy in spider.get_proxies():
				time.sleep(0.1)
				checked_proxy = check_proxy(proxy)
				check_ip_count += 1
				if proxy.speed != -1:
					self.mongo_pool.insert(checked_proxy)
			logger.info('爬虫{}爬取并校验{}个ip完毕'.format(spider,check_ip_count))

		except Exception as er:
			logger.exception(er)
			logger.exception("爬虫{} 出现错误".format(spider))

	@classmethod
	def start(cls):
		'''
		类方法，依据配置文件汇总的时间间隔run爬虫，单位小时
		'''
		rs = RunSpider()
		rs.run()
		schedule.every(SPIDERS_RUN_INTERVAL).hours.do(rs.run)

		while 1:
			schedule.run_pending()
			time.sleep(60)



if __name__ == '__main__':
	#类方法调用
	RunSpider.start()
	#app = RunSpider()
	#app.run()

	#测试schedue
	'''def task():
		print("haha")
	schedule.every(10).seconds.do(task)
	while 1:
		schedule.run_pending()
		time.sleep(1)'''


