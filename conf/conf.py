#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-15, 20:42:00 
# @file conf.py
# @author zihuacs(zihuacs@qq.com)
# @brief 配置文件
#--------------------------------------------------------------------- 
import os
import datetime, time, math
import mylogger

#路径配置
#------------目录级别的--------------#
ROOT_DIR = os.path.abspath('D:\GitHub\search_vs')
# 配置
CONF_DIR = ROOT_DIR + os.path.sep + 'conf'
if not os.path.isdir(CONF_DIR):
    os.mkdir(CONF_DIR)
# 数据
DATA_DIR = ROOT_DIR + os.path.sep + 'data'
if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)
# 文档
DOC_DIR = ROOT_DIR + os.path.sep + 'doc'
if not os.path.isdir(DOC_DIR):
    os.mkdir(DOC_DIR)
# 脚本
SHELL_DIR = ROOT_DIR + os.path.sep + 'shell'
if not os.path.isdir(SHELL_DIR):
    os.mkdir(SHELL_DIR)
# 样式CSS
CSS_DIR = ROOT_DIR + os.path.sep + 'css'
if not os.path.isdir(SHELL_DIR):
    os.mkdir(SHELL_DIR)

# 日志
LOG_DIR = ROOT_DIR + os.path.sep + 'log'
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

#-----------下载相关----------------#
SEARCH_BAIDU_URL = "http://music.baidu.com/search/song?key=%s"
SEARCH_360_URL   = "http://s.music.so.com/s?q=%s&c=%s"
#-----------变量相关----------------#
TYPE_LIST = ['baidu','kuwo','xiami','kugou','1ting']
#-----------文件相关----------------#
#index.css
INDEX_CSS = CSS_DIR + os.path.sep + 'index.css'

#Log
LOG_PATH = LOG_DIR + os.path.sep + 'search_vs'
#Log级别
#FATAL = 60
#ERROR = 50
#WARNING = 40
#NOTICE = 30
#TRACE = 20
#DEBUG = 10
#级别设置
LOG_LEVEL_DEF = 10
#格式
LOG_FORMATTER_DEF = mylogger.Formatter('[%(levelname)s] [%(asctime)s] [%(message)s] [%(module)s %(filename)s %(lineno)d]')
LOG_CONFIG_MAP = {'main': {'name':'main','level': LOG_LEVEL_DEF, 'filepath': LOG_PATH, 'formatter': LOG_FORMATTER_DEF}}
#全局logger
LOGGER = mylogger.getLongTimeLogger(LOG_CONFIG_MAP['main']['filepath'], LOG_CONFIG_MAP['main']['formatter'], LOG_CONFIG_MAP['main']['name'], LOG_CONFIG_MAP['main']['level'])
