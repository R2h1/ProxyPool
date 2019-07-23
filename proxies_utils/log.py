'''
记录日志的模块
'''

import sys,os
#Python的标准日志模块：logging
import logging
#将上级目录添加到搜索路径中
sys.path.append("../")

from settings import LOG_LEVEL,LOG_FMT ,LOG_DATEFMT,LOG_FILENAME 

class Logger(object):

    def __init__(self):
        #获取一个logger对象
        self._logger = logging.getLogger()
        #设置format对象
        self.formatter = logging.Formatter(fmt=LOG_FMT,datefmt=LOG_DATEFMT)
        #设置日志输出——文件日志模式
        self._logger.addHandler(self._get_file_handler(LOG_FILENAME))
        #设置日志输出——终端日志模式
        self._logger.addHandler(self._get_console_handler())
        # 4. 设置日志等级
        self._logger.setLevel(LOG_LEVEL)

    def _get_file_handler(self, filename):
        '''
        返回一个文件日志handler
        '''
        # 获取一个输出为文件日志的handler
        filehandler = logging.FileHandler(filename=filename,encoding="utf-8")
        # 设置日志格式
        filehandler.setFormatter(self.formatter)
        # 返回
        return filehandler

    def _get_console_handler(self):
        '''
        返回一个输出到终端日志handler
        '''
        #获取一个输出到终端的日志handler
        console_handler = logging.StreamHandler(sys.stdout)
        #设置日志格式
        console_handler.setFormatter(self.formatter)
        # 返回handler
        return console_handler

    #属性装饰器，返回一个logger对象
    @property
    def logger(self):
        return self._logger

# 初始化并配一个logger对象，达到单例
# 使用时，直接导入logger就可以使用
logger = Logger().logger

if __name__ == '__main__':
    print(logger)
    logger.debug("调试信息")
    logger.info("状态信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重错误信息")