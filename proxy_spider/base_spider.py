'''
通用爬虫:通过指定URL列表, 分组XPATH和组内XPATH, 来提取不同网站的代理IP
定义一个BaseSpider类, 继承object
  - 提供三个类成员变量:urls, group_xpath, detail_xpath: ip, port, area
  - 提供初始方法, 传入爬虫URL列表, 分组XPATH, 详情(组内)XPATH
  - 对外提供一个获取代理IP的方法
'''

import requests
import sys
import time,random
from lxml import etree
sys.path.append('..')
from proxies_utils.random_headers import get_request_headers
from dbmodle import Proxy
from settings import TIMEOUT

class BaseSpider(object):
	#类成员变量
	#代理IP网址的URL的列表
	urls =[]
	#分组XPATH, 获取包含代理IP信息标签列表的XPATH
	group_xpath = ''
	#组内XPATH, 获取代理IP详情的信息XPATH, 格式为: {'ip':'xx', 'port':'xx', 'area':'xx'}
	detail_xpath ={}
	def __init__(self,urls =[],group_xpath='',detail_xpath={}):
		#提供初始方法, 传入爬虫URL列表, 分组XPATH, 详情(组内)XPATH
		if urls:
			self.urls =urls
		if group_xpath:
			self.group_xpath =group_xpath
		if detail_xpath:
			self.detail_xpath=detail_xpath


	def get_proxies(self):
		#获取页面数据
		for url in self.urls:
			page_html = self.get_page(url)

			proxies =self.get_html_proxies(page_html)
			#yeild from 返回的是proxies内的数据
			yield from proxies


	def get_page(self,url):
		#请求页面数据
		try:
			res =requests.get(url,headers = get_request_headers(),timeout=TIMEOUT)
			#每次请求url休眠1秒
			time.sleep(random.uniform(3,6))
			return res.content
		except requests.exceptions.ReadTimeout:
			for i in range(1, 10):
				print('请求超时，第%s次重复请求' % i)
				res = requests.get(url, headers=get_request_headers(),timeout=TIMEOUT)
				if res.status_code == 200:
					return res.content
				else:
					continue
		

	def get_html_proxies(self,page_html):
		element = etree.HTML(page_html)
		trs = element.xpath(self.group_xpath)
		for tr in trs:
			ip = self.get_list_first(tr.xpath(self.detail_xpath['ip']))
			port = self.get_list_first(tr.xpath(self.detail_xpath['port']))
			area = self.get_list_first(tr.xpath(self.detail_xpath['area']))
			proxy = Proxy(ip,port,area=area)
			yield proxy

	def get_list_first(self,lst):
		#返回列表的第一个元素
		return lst[0] if len(lst) !=0 else ''

if __name__ == '__main__':
	config = {
	'urls':['http://www.ip3366.net/free/?stype=1&page={}'.format(i) for i in range(1,8)],
	'group_xpath':'//*[@id="list"]/table/tbody/tr',
	'detail_xpath':{
	'ip':'./td[1]/text()',
	'port':'./td[2]/text()',
	'area':'./td[5]/text()',
	}
	}
	spider = BaseSpider(**config)
	for proxy in spider.get_proxies():
		print(proxy)
