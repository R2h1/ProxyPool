'''
代理ip数据模型模块

定义一个类, 继承object
实现init方法, 负责初始化, 包含如下字段:
	ip: 代理的IP地址
	port: 代理IP的端口号
	protocol: 代理IP支持的协议类型,http是0, https是1, https和http都支持是2
	nick_type: 代理IP的匿名程度, 高匿:0, 匿名: 1, 透明:2
	speed: 代理IP的响应速度, 单位s
	area: 代理IP所在地区
	score: 代理IP的评分, 默认分值可以通过配置文件进行配置. 在进行代理可用性检查的时候, 每遇到一次请求失败就减1份, 减到0的时候从池中删除. 如果检查代理可用, 就恢复默认分值
	disable_domains: 不可用域名列表, 有些代理IP在某些域名下不可用, 但是在其他域名下可用
创建配置文件: settings.py; 定义MAX_SCORE = 50, 
'''
from settings import MAX_SCORE

class Proxy(object):

	def __init__(self,ip,port,protocol=-1,nick_type=-1,speed=-1,area=None,score=MAX_SCORE,disuseble_dommains=[]):
		#代理ip的地址
		self.ip = ip
		#代理ip的端口号
		self.port = port
		#代理ip支持协议类型：支持http为0，支持https为1，都支持为2
		self.protocol = protocol
		#代理ip的匿名程度：高匿为0，匿名为1，透明为2
		self.nick_type =nick_type
		#代理ip的响应速度
		self.speed = speed
		#代理ip所在地区
		self.area = area
		#代理ip的评分，衡量代理ip的可用性
		self.score =score
		#代理ip的不可用域名列表
		self.disuseble_dommains =disuseble_dommains

	def __str__(self):
		#返回数据字符串
		return str(self.__dict__)

