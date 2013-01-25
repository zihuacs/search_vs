#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-25, 00:00:00 
# @file search_qq.py
# @author zihuacs(zihuacs@qq.com)
# @brief 抓取QQ音乐歌曲检索首页结果，非首页忽略之
#--------------------------------------------------------------------- 
import urllib2
import time
from bs4 import BeautifulSoup
from song_info import *
from urllib import quote


class SearchQq:
	'''
	url : http://soso.music.qq.com/fcgi-bin/multiple_music_search.fcg?p=1&catZhida=1&lossless=0&t=100&utf8=1&w=%s#tab=music|%s
	'''
	def __init__(self,url):
		self.song_info = SongInfo('qq')
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
	em_list = [<strong class="keyword">我的歌声里</strong>]
	return high_list = [因为爱情] 
	strip+去重
	'''
	def get_high_list(self,em_list):
		high_list = []
		for high_item in em_list:
			high_word = str(high_item).replace('<strong class="keyword">','').replace('</strong>','')
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

		if tag.name =='div' and tag.has_key('class') and tag['class'] == ['search_time'] :
			#<p>找到相关结果约<strong>682</strong>条，用时<strong>0.011</strong>秒</p>
			try:
				tab_num = int(tag.p.strong.get_text())
			except AttributeError:
				# 无结果标志
				self.all_num = 0
				return
			self.all_num = tab_num
			self.song_info.set_all_num(tab_num)
			return True
		# 提取内容
		if tag.name == 'div'  and tag.has_key('class') and \
		   tag['class'] in [['music_name'],['singer_name'],['album_name']]:
			if tag.a.has_key('title'):
				_title = tag.a['title'].encode('utf-8')
			else:
				_title = tag.a.get_text().encode('utf-8')

			_high_list = self.get_high_list(tag.find_all('strong'))
			_link      = tag.a['href'].encode('utf-8')

			if tag['class'] == ['music_name']:
				self.result['title']         = _title
				self.result['high']['title'] = _high_list
				self.result['link']['title'] = self.url % (_title,_title)
				return True

			if tag['class'] == ['singer_name']:
				self.result['artist']         = _title
				self.result['high']['artist'] = _high_list
				self.result['link']['artist'] = _link
				return True

			if tag['class'] == ['album_name']:
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
		search_url = self.url % (qword,qword)

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
def get_search_qq_res(url,qword):
	SQ = SearchQq(url)
	SQ.start(qword)
	qq_song_info = SQ.get_song_info()
	return qq_song_info

def test_qq(url,qword):
	SQ = SearchQq(url)
	SQ.start(qword)
	SQ.show()

#test_qq('http://soso.music.qq.com/fcgi-bin/multiple_music_search.fcg?p=1&catZhida=1&lossless=0&t=100&utf8=1&w=%s#tab=music|%s','叫床')
#get_search_qq_res('http://soso.music.qq.com/fcgi-bin/multiple_music_search.fcg?p=1&catZhida=1&lossless=0&t=100&utf8=1&w=%s#tab=music|%s','因为爱情')