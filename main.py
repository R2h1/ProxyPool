'''
代理池统一入口：
   开启多个进程，分别启动，爬虫，检测代理ip，WEB服务
'''

from multiprocessing import Process
from proxy_spider.run_spider import RunSpider
from proxy_test import DbProxiesCheck
from proxy_api import ProxyApi

def run():
	process_list = []
	#启动爬虫
	process_list.append(Process(target = RunSpider.start))
	#启动检测
	process_list.append(Process(target = DbProxiesCheck.start))
	#启动web服务
	process_list.append(Process(target = ProxyApi.start))

	for process in process_list:
		#设置守护进程
		process.daemon = True
		process.start()
	#主进程等待子进程的完成
	for process in process_list:
		process.join()


if __name__ == '__main__':
	run()
