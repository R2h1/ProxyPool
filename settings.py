#默代理IP的默认最高分数
MAX_SCORE =50

import logging

#日志模块默认配置：
# 默认等级
LOG_LEVEL = logging.INFO
#默认日志格式
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
# 默认时间格式
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
# 默认日志文件名称
LOG_FILENAME = 'log.log'

#校验请求超时参数
CHECK_TIMEOUT = 20

#代理ip请求超时参数
TIMEOUT = 30
#mongodb的URL配置
MONGO_URL = 'mongodb://127.0.0.1:27017/'

#具体爬虫的配置列表
PROXIES_SPIDERS = [
"proxy_spider.proxy_spiders.XiciSpider",
"proxy_spider.proxy_spiders.Ip3366Spider",
"proxy_spider.proxy_spiders.kuaiSpider",
"proxy_spider.proxy_spiders.Free89ipSpider",
"proxy_spider.proxy_spiders.IphaiSpider",
"proxy_spider.proxy_spiders.ProxylistplusSpider",
"proxy_spider.proxy_spiders.QiYunSpider",
]

#爬虫间隔自动运行时间
SPIDERS_RUN_INTERVAL = 4

#配置检测代理ip的异步数量
TEST_PROXIES_ASYNC_COUNT = 10

#db中ip间隔自动运行时间
TEST_RUN_INTERVAL = 2

#随机获取代理ip的最大数量
PROXIES_MAX_COUNT = 50