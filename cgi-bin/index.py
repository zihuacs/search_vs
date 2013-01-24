#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-17, 16:30:00 
# @file index.py
# @author zihuacs(zihuacs@qq.com)
# @brief web前端首页展示
#--------------------------------------------------------------------- 


import cgi
from proc_init import *
proc_init()

from conf import *
from search_baidu import *
from serach_360 import *
from common import *
from song_info import *
from pingce import pingce_fun

import threading

'''
获取baidu、360单个检索返回的结果并加入 song_info_list
'''
def get_song_info(song_info_list,qword,qtype):
	if qtype == 'baidu':
		song_info_list.append(get_search_baidu_res(SEARCH_BAIDU_URL,qword))
	else:
		song_info_list.append(get_search_360_res(SEARCH_360_URL,qword,qtype))


'''
以多线程的方式获取结果,并以type_list 进行重排序
'''
def mult_get_song_info_list(song_info_list,qword):
	threads=[]
	type_list = ['baidu','kuwo','xiami','kugou','1ting']
	for qtype in type_list:
		t = threading.Thread(target=get_song_info, args=(song_info_list,qword,qtype))
		threads.append(t)

	for i in range(len(type_list)):
		threads[i].start()
	for i in range(len(type_list)):
		threads[i].join()
	# 重排序之
	for qtype in type_list:
		for song_info in song_info_list:
			if song_info.get_src_type() == qtype:
				song_info_list.remove(song_info)
				song_info_list.append(song_info)

'''
从baidu、360汇聚结果
'''
def show_search_res(qword):
	song_info_list=[]
	# 无query，show box 之
	if qword=='':
		# 伪造 空 结果
		song_info_list.append(SongInfo('baidu'))
		song_info_list.append(SongInfo('1ting'))
		song_info_list.append(SongInfo('xiami'))
		song_info_list.append(SongInfo('kuwo'))
		song_info_list.append(SongInfo('kugou'))

		show_song_info_list_html(INDEX_CSS,song_info_list,qword)
		return True
	# 向 3B 发起检索
	# B 检索
	# song_info_list.append(get_search_baidu_res(SEARCH_BAIDU_URL,qword))
	# # 3 检索
	# type_list = ['1ting','xiami','kuwo','kugou']
	# for qtype in type_list:
	# 	s360_song_info = get_search_360_res(SEARCH_360_URL,qword,qtype)
	# 	song_info_list.append(s360_song_info)
	
	# 多线程抽取结果
	mult_get_song_info_list(song_info_list,qword)
	# 评测之
	pingce_fun(song_info_list)

	# # show 3B 结果
	show_song_info_list_html(INDEX_CSS,song_info_list,qword)
	return True
'''
从搜索框提取query
'''
def get_query_word():
	form=cgi.FieldStorage()
	if form.has_key('qword'):
		qword = form['qword'].value
	else:
		qword = '因为爱情'
	return qword.strip()

'''
主函数入口
'''
def main():
	# 此语句不可少之
	print "Content-type: text/html; charset='UTF-8'\n\n"

	qword = get_query_word()
	show_search_res(qword)


if __name__ =='__main__':
	main()

	