#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-23, 15:18:00 
# @file pingce.py
# @author zihuacs(zihuacs@qq.com)
# @brief 基于最小编辑距离 + 逆序评价
#---------------------------------------------------------------------
from song_info import *
'''
return min_num
'''
def min_num(a,b):
	if a<b:
		return a
	return b
'''
计算两个字符串的最小编辑距离
dist[i,j] = min(dist[i,j-1] +1 , dist[i-1,j]+1, dist[i-1,j-1] + (s1[i] == s2[j] ? 0:1))
str1,str2 unicode 编码
'''
def minimum_edit_distance(str1,str2):
	# 两个字符串的长度
	len1= len(str1)
	len2= len(str2)
	# 特殊情形
	if len1 == 0 and len2 ==0:
		return 0
	if len1 !=0 and len2 ==0:
		return len1
	if len1 ==0 and len2 !=0:
		return len2
	# 以下处理 len1 && len2 均不为0的情形
	# 初始化分配空间
	dist= []
	dist=[0]*len1 
	for i in range(len1):
		for j in range(len2):
			dist[i] = [0]*len2
	# 设置dist[0][0] = if str1[0] == str2[0] then 0 else 1
	# 左上角
	if str1[0] == str2[0]:
		dist[0][0]=0
	else:
		dist[0][0]=1
	# 第0行
	for j in range(1,len2):
		if str1[0] == str2[j]:
			dist[0][j] = j-1
		else:
			dist[0][j] = dist[0][j-1] + 1
	# 第0列
	for i in range(1,len1):
		if str1[i] == str2[0]:
			dist[i][0] = i-1
		else:
			dist[i][0] = dist[i-1][0] + 1
	# [1,len1) -- [1,len2)
	for i in range(1,len1):
		for j in range(1,len2):
			dist[i][j] = min_num( dist[i-1][j] +1 , dist[i][j-1] +1 )
			if str1[i] == str2[j]:
				dist[i][j] = min_num( dist[i-1][j-1] , dist[i][j])
			else:
				dist[i][j] = min_num( dist[i-1][j-1] +1  , dist[i][j])

	return dist[len1-1][len2-1]

'''
从list中获取百度，无则构造一个无数据对象返回
'''
def get_baidu_song_info(song_info_list):
	for song_info in song_info_list:
		if song_info.get_src_type() == 'baidu':
			return song_info

	return SongInfo('baidu')
'''
规范str, 去除多余字符什么的
'''
def str_proc(string):
	special_en_string ='''~!@#$%^&*()_+-=[{]};:'"\|,<.>/?·'''
	special_word_list =[' ','\n','\t','！','——','【','】','《','》','，','。','、','？','；','：','‘','’','“','”'] 
	special_word_list+=list(special_en_string)

	for sword in special_word_list:
		string = string.replace(sword,'')


	return string
'''
最小编辑距离 得到最佳匹配 
'''
def get_best_match(baidu_song_info,other_str):
	match_list   =[]
	is_hav_match =False

	for i,item in enumerate(baidu_song_info.get_results()):
		baidu_str = ''
		baidu_str = item['title'] + item['artist'] + item['album']
		# 字符串归一化
		try:
			ubaidu_str = str_proc(baidu_str).decode('UTF-8')
			uother_str = str_proc(other_str).decode('UTF-8')
		except UnicodeDecodeError:
			ubaidu_str = baidu_str
			uother_str = other_str

		# 计算字符串编辑距离
		distance  = minimum_edit_distance(ubaidu_str,uother_str)
		match_list.append([i,distance])
		# only distance in [0,1,2]
		if distance < 3:
			is_hav_match = True 

	if is_hav_match == False:
		# 表示无match
		return [-1,-1]

	# here 统一处理match_list
	min_distance = match_list[-1][1]
	min_no       = match_list[-1][0]

	i = len(match_list)-1
	while i>=0:
		if match_list[i][1] < min_distance:
			min_distance = match_list[i][1]
			min_no       = match_list[i][0]
		i-=1

	return [min_no,min_distance]
'''
两两对比之 baidu vs other 
'''
def search_vs(baidu_song_info, other_song_info):
	match_list = []
	for item in other_song_info.get_results():
		other_str = ''
		other_str = item['title'] + item['artist'] + item['album']
		match_list.append(get_best_match(baidu_song_info , other_str))

	# core
	for i in range(len(match_list)):
		i_item = match_list[i]
		if i_item[0] == -1:
			continue
		for j in range(len(match_list)):
			j_item = match_list[j]
			if j==i or j_item[0] == -1:
				continue
			
			if j < i and j_item[0] > i_item[0]:
				if baidu_song_info.results[i_item[0]].has_key('up') == False:
					baidu_song_info.results[i_item[0]]['up'] = 0
				else:
					baidu_song_info.results[i_item[0]]['up'] = baidu_song_info.results[i_item[0]]['up'] + 1

			if j > i and j_item[0] < i_item[0]:
				if baidu_song_info.results[i_item[0]].has_key('down') == False:
					baidu_song_info.results[i_item[0]]['down'] = 0
				else:
					baidu_song_info.results[i_item[0]]['down'] = baidu_song_info.results[i_item[0]]['down'] + 1 

				 

'''
评测入口程序
'''
def pingce_fun(song_info_list):
	baidu_song_info = get_baidu_song_info(song_info_list)
	type_list = ['kuwo','xiami','kugou','1ting']
	for i in range(1,len(song_info_list)):
		search_vs(baidu_song_info,song_info_list[i])

print minimum_edit_distance(" 你是我的眼0 我的歌声里".decode('UTF-8'),"我的歌声里 你是我的眼0".decode('UTF-8'))
print str_proc('我的歌声...')