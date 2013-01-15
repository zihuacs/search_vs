#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-15, 14:17:00 
# @file song_info.py
# @author zihuacs(zihuacs@qq.com)
# @brief song_info 360&baidu 抓取共用的信息
#--------------------------------------------------------------------- 

class SongInfo:

	# results = [{'title':'...','artist':'...','album':'...','high':{'title':[],'artist':[],'album':[]}},..]
	# src_type must in ['baidu','xiami','yiting','kugou','kuwo']
	def __init__(self,src_type):
		self.results  =[]
		self.src_type =src_type
		self.all_num  =0

	def set_all_num(self,all_num):
		self.all_num = all_num
	
	# result= {'title':'...','artist':'...','album':'...','high':{'title':[],'artist':[],'album':[]}}
	def append_result(self,result):
		self.results.append(result)

	def clear(self):
		self.__init__(self.src_type)

	def show(self):
		print "type : %s" % self.src_type
		print "all_num : %d" % self.all_num
		count=0
		for item in self.results:
			count = count+1
			print "%2d\t%-40s\t|\t%-30s\t|\t%-20s\t" % (count,item['title'],item['artist'],item['album'])
			#print "%-40s\t\t%-30s\t\t%-20s\t" % (item['high']['title'],item['high']['artist'],item['high']['album'])


