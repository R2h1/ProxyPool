'''
定期检测数据库中的代理ip的可用性,分数评级，更新数据库
'''
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
import schedule
import sys
sys.path.append('../')
from proxy_validate.httpbin_validator import check_proxy
from proxies_db.mongo_pool import MongoPool
from settings import TEST_PROXIES_ASYNC_COUNT,MAX_SCORE,TEST_RUN_INTERVAL


class DbProxiesCheck(object):

	def __init__(self):
		#创建操作数据库对象
		self.mongo_pool = MongoPool()
		#待检测ip队列
		self.queue = Queue()
		#协程池
		self.coroutine_pool = Pool()

	#异步回调函数
	def __check_callback(self,temp):
		self.coroutine_pool.apply_async(self.__check_one,callback = self.__check_one())


	def run(self):
		#处理检测代理ip核心逻辑
		proxies = self.mongo_pool.find_all()

		for proxy in proxies:
			self.queue.put(proxy)

		#开启多异步任务
		for i in range(TEST_PROXIES_ASYNC_COUNT):
			#异步回调，死循环执行该方法
			self.coroutine_pool.apply_async(self.__check_one,callback =self.__check_one())
		#当前线程等待队列任务完成
		self.queue.join()



	def __check_one(self):
		#检查一个代理ip可用性
		#从队列中获取一个proxy
		proxy = self.queue.get()

		checked_proxy = check_proxy(proxy)

		if checked_proxy.speed == -1:
			checked_proxy.score -= 1
			if checked_proxy.score == 0:
				self.mongo_pool.delete(checked_proxy)
			else:
				self.mongo_pool.update(checked_proxy)
		else:
			checked_proxy.score = MAX_SCORE
			self.mongo_pool.updata(checked_proxy)
		#调度队列的task_done方法(一个任务完成)
		self.queue.task_done()


	@classmethod
	def start(cls):
		'''
		类方法，依据配置文件的时间间隔运行检测数据库中的ip可用性，单位小时
		'''
		test = DbProxiesCheck()
		test.run()
		schedule.every(TEST_RUN_INTERVAL).hours.do(test.run)

		while 1:
			schedule.run_pending()
			time.sleep(60)


if __name__ == '__main__':
	DbProxiesCheck.start()
	#test = DbProxiesCheck()
	#test.run()
