#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-15, 20:46:00 
# @file test.py
# @author zihuacs(zihuacs@qq.com)
# @brief just for test
#--------------------------------------------------------------------- 
from proc_init import *
proc_init()

from conf import *
from search_baidu import *
from serach_360 import *

def test_search_baidu():
	test_baidu(SEARCH_BAIDU_URL,"我的歌声里")

def test_search_360():
	type_list = ['1ting','xiami','kuwo','kugou']
	for qtype in type_list:
		test_360(SEARCH_360_URL,'我的歌声里',qtype)

def main():
	test_search_baidu()
	test_search_360()

if __name__ =='__main__':
	main()