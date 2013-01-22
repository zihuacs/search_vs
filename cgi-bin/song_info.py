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

	'''
	results = [{'title':'...','artist':'...','album':'...','high':{'title':[],'artist':[],'album':[]},'link':{'title','artist','album'}},]
	src_type must in ['baidu','xiami','yiting','kugou','kuwo']
	proc_time =time.begin - time.end 
	'''
	def __init__(self,src_type):
		self.results   =[]
		self.src_type  =src_type
		self.all_num   =0
		self.proc_time = 0.0
		self.search_url=''
	

	def get_results(self):
		return self.results
	
	def get_src_type(self):
		return self.src_type

	def get_all_num(self):
		return self.all_num

	def get_proc_time(self):
		return self.proc_time
	
	def get_search_url(self):
		return self.search_url

	def set_all_num(self,all_num):
		self.all_num = all_num
	
	def set_proc_time(self,proc_time):
		self.proc_time = proc_time

	def set_search_url(self,search_url):
		self.search_url = search_url
	'''
	result= {'title':'...','artist':'...','album':'...','high':{'title':[],'artist':[],'album':[]},'link':{'title','artist','album'}}}
	'''
	def append_result(self,result):
		self.results.append(result)
	'''
	clear it but not clear proc_time
	'''
	def clear(self):
		tmp_time = self.proc_time
		self.__init__(self.src_type)
		self.proc_time = tmp_time

	def show(self):
		print "type : %s" % self.src_type
		print "all_num : %d" % self.all_num
		print "proc_time : %f" % self.proc_time 
		count=0
		for item in self.results:
			count = count+1
			print "%2d\t%-40s\t|\t%-30s\t|\t%-20s\t" % (count,item['title'],item['artist'],item['album'])
			#print "%-40s\t\t%-30s\t\t%-20s\t" % (item['high']['title'],item['high']['artist'],item['high']['album'])


