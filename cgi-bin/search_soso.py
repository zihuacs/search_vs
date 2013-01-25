#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-25, 10:49:00 
# @file search_soso.py
# @author zihuacs(zihuacs@qq.com)
# @brief 抓取搜搜音乐歌曲检索首页结果，非首页忽略之
#--------------------------------------------------------------------- 
import urllib2
import time
from bs4 import BeautifulSoup
from song_info import *
from urllib import quote


class SearchSoso:
	'''
	url : http://cgi.music.soso.com/fcgi-bin/m.q?w=%s
	'''
	def __init__(self,url):
		self.song_info = SongInfo('soso')
		self.url       = url 

		self.temp_init()
		self.all_num=0

	'''
	临时变量初始化 --- 在查找song_info 中使用
	'''
	def temp_init(self):
		self.result         ={'title':'','artist':'','album':'','high':{},'link':{}}
		self.result['high'] ={'title':[],'artist':[],'album':[]}
		self.result['link'] ={'title':'','artist':'','album':''}

	'''
	return self.song_info
	'''
	def get_song_info(self):
		return self.song_info

	'''
	just for test 
	'''
	def find_a(self,tag):
		if tag.name == 'a':
			return True
		return False

	'''
	em_list = [[<strong>因为爱情</strong>, <strong>爱情</strong>]]
	return high_list = [因为爱情,爱情] 
	strip+去重
	'''
	def get_high_list(self,em_list):
		high_list = []
		for high_item in em_list:
			high_word = str(high_item).replace('<strong>','').replace('</strong>','')
			if not high_word.strip() in high_list:
				high_list.append(high_word.strip())
		return high_list

	'''
	tag: soup处理的当前标签，从合适的tag中抽取num、title、artist、album、high
	封装到result里
	result={'title':'...','artist':'...','album':'...','high':{'title':[],'artist':[],'album':[]}}
	'''
	def find_song_info(self,tag):
		# 抓取结果数
		if tag.name =='p' and tag.has_key('class') and tag['class'] == ['s_head_info']:
			# <p class="s_head_info">SOSO音乐搜索 "<strong>因为爱情</strong>" 约<em>2630</em>项结果</p>
			tab_num = int(tag.em.get_text())
			self.all_num = tab_num
			self.song_info.set_all_num(tab_num)
			return True	

		if self.all_num >0 and tag.name == 'td'  and tag.has_key('class') and \
		   tag['class'] in [['song'],['singer'],['ablum']]:

			if tag.a != None:
				_title     = tag.a.get_text().encode('utf-8')
				_high_list = self.get_high_list(tag.find_all('strong'))
				_link      = tag.a['href'].encode('utf-8')
			else:
				_title , _high_list , _link = '',[],''

			# print _title
			# print _high_list
			# print _link

			if tag['class'] == ['song']:
				self.result['title']         = _title
				self.result['high']['title'] = _high_list
				self.result['link']['title'] = self.song_info.get_search_url()
				return True

			if tag['class'] == ['singer']:
				self.result['artist']         = _title
				self.result['high']['artist'] = _high_list
				self.result['link']['artist'] = _link
				return True

			if tag['class'] == ['ablum']:
				self.result['album']         = _title
				self.result['high']['album'] = _high_list
				self.result['link']['album'] = _link
				# 加入一条结果
				self.song_info.append_result(self.result)
				# 清空临时变量
				self.temp_init()	
				return True	

		return False
	'''
	just call self.song_info.show()
	'''
	def show(self):
		self.song_info.show()
	'''
	qword: 因为爱情、我的歌声里、...
	1. 拼接url，下载之，soup解析之，而后勇find_song_info寻址之
	'''
	def start(self,qword):
		# 拼接url
		search_url = self.url % quote(qword.decode('utf-8').encode('gbk'))
		
		# 下载之 
		begin_time = time.time()
		content = urllib2.urlopen(search_url).read()
		end_time = time.time()
		# 时间之
		self.song_info.set_proc_time(float(end_time - begin_time))
		# soup对象
		soup = BeautifulSoup(content)
		# 清空song_info
		self.song_info.clear()
		# 寻址之
		self.song_info.set_search_url(search_url)
		soup.find_all(self.find_song_info)

'''
根据url and word return song_info
'''
def get_search_soso_res(url,qword):
	SS = SearchSoso(url)
	SS.start(qword)
	soso_song_info = SS.get_song_info()
	return soso_song_info

def test_soso(url,qword):
	SS = SearchSoso(url)
	SS.start(qword)
	SS.show()

#test_soso('http://cgi.music.soso.com/fcgi-bin/m.q?w=%s','因为爱情')
#get_search_soso_res('http://cgi.music.soso.com/fcgi-bin/m.q?w=%s','因为爱情')