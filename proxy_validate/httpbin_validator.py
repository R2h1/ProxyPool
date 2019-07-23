'''
代理IP速度检查: 就是发送请求到获取响应的时间间隔
匿名程度检查:
		对 http://httpbin.org/get 或 https://httpbin.org/get 发送请求
		if : origin 中有','分割的两个IP就是透明代理IP
		if : headers 中包含 Proxy-Connection 说明是匿名代理IP
		else : 就是高匿代理IP
检查代理IP协议类型:
	如果 http://httpbin.org/get 发送请求可以成功, 说明支持http协议
	如果 https://httpbin.org/get 发送请求可以成功, 说明支持https协议
'''
import sys
import time
import requests
import json
sys.path.append("..")
from proxies_utils import random_headers
from settings import CHECK_TIMEOUT
from proxies_utils.log import logger
from dbmodle import Proxy


def check_proxy(proxy):
	'''
	分别判断http和https是否请求成功
	'''
	#代理ip
	proxies = {
	'http':'http://{}:{}'.format(proxy.ip,proxy.port),
	'https':'https://{}:{}'.format(proxy.ip,proxy.port),
	}

	http,http_nick_type,http_speed = http_check_proxies(proxies)
	https,https_nick_type,https_speed = http_check_proxies(proxies,False)

	if http and https:
		proxy.protocol = 2  #支持https和http
		proxy.nick_type =http_nick_type
		proxy.speed = http_speed
	elif http:
		proxy.protocol = 0  #只支持http
		proxy.nick_type =http_nick_type
		proxy.speed = http_speed
	elif https:
		proxy.protocol = 1 #只支持https
		proxy.nick_type =https_nick_type
		proxy.speed = https_speed
	else:  
		proxy.protocol = -1
		proxy.nick_type = -1
		proxy.speed = -1
	
	#logger.debug(proxy)

	return proxy

def http_check_proxies(proxies,isHttp = True):
	'''
	代理ip请求校验ip
	'''
	nick_type = -1 #匿名程度变量
	speed = -1  #响应速度变量
	if isHttp:
		test_url = 'http://httpbin.org/get'
	else:
		test_url = 'https://httpbin.org/get'
	#requests库请求test_url
	try:
		#响应时间
		start_time = time.time()
		res = requests.get(test_url,headers = random_headers.get_request_headers(),proxies = proxies,timeout = CHECK_TIMEOUT)
		end_time = time.time()
		cost_time =end_time-start_time

		if res.ok:
			#响应速度
			speed = round(cost_time,2)
			#转换为字典
			res_dict = json.loads(res.text)
			#获取请求来源ip
			origin_ip = res_dict['origin']
			#获取响应请求头中'Proxy-Connection',若有,说明是匿名代理
			proxy_connection = res_dict['headers'].get('Proxy-Conntion',None)

			if "," in origin_ip:
				#如果响应内容中的源ip中有‘,’分割的两个ip的话及时透明代理ip
				nick_type = 2 #透明
			elif proxy_connection:
				#'Proxy-Connection'存在说明是匿名ip
				nick_type = 1 #匿名
			else:
				nick_type =0  #高匿
			return True,nick_type,speed
		else:
			return False,nick_type,speed
	except Exception as e:
		#logger.exception(e)
		return False,nick_type,speed

if __name__ == '__main__':
	proxy = Proxy('180.104.62.199','9000')
	result = check_proxy(proxy)
	print(result)
