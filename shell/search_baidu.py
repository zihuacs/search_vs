#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-15, 19:52:00 
# @file search_baidu.py
# @author zihuacs(zihuacs@qq.com)
# @brief 抓取百度音乐歌曲检索首页结果，非首页忽略之
#--------------------------------------------------------------------- 
import urllib2
from bs4 import BeautifulSoup
from song_info import *

class SearchBadiu:
	'''
	url : http://music.baidu.com/search/song?key=%s
	'''
	def __init__(self,url):
		self.song_info = SongInfo('baidu')
		self.url       = url

		self.temp_init()
	'''
	临时变量初始化 --- 在查找song_info 中使用
	'''
	def temp_init(self):
		self.all_num=0
		self.result={}
		self.result['high']={}

	'''
	just for test 
	'''
	def find_a(self,tag):
		if tag.name == 'a':
			return True
		return False

	'''
	em_list = [<em><em>因为爱情</em></em>, <em> 因为爱情  </em>]
	return high_list = [因为爱情] 
	strip+去重
	'''
	def get_high_list(self,em_list):
		high_list = []
		for high_item in em_list:
			high_word = str(high_item).replace('<em>','').replace('</em>','')
			if not high_word.strip() in high_list:
				high_list.append(high_word.strip())
		return high_list
	'''
	tag: soup处理的当前标签，从合适的tag中抽取num、title、artist、album、high
	封装到result里
	result={'title':'...','artist':'...','album':'...','high':{'title':[],'artist':[],'album':[]}}
	'''
	def find_song_info(self,tag):
		
		if tag.name == 'li' and tag.has_key('class') and tag['class'][0] == 'ui-tab-active' :
			tab_name = tag.a.string.encode('utf-8').split('(')[0]
			tab_num  = int(tag.a.string.encode('utf-8').split('(')[1].split(')')[0].replace('+',''))
			if tab_name in ['歌曲']:
				self.all_num = tab_num
				self.song_info.set_all_num(tab_num)
				return True

		if tag.name == 'span' and tag.has_key('class') and tag.has_key('style') and \
		   tag['class'] in [['song-title'],['singer'],['album-title']]:
			
			_string    = tag.get_text().encode('utf-8').strip().replace('\n',' ')
			_high_list = self.get_high_list(tag.find_all('em'))

			if tag['class'] == ['song-title']:
				self.result['title']          = _string.strip().split(' ')[0]
				self.result['high']['title']  = _high_list
				return True
			if tag['class'] == ['singer']:
				self.result['artist']         = _string.replace('/',',').replace('\t',' ').replace(' ','')
				self.result['high']['artist'] = _high_list
				return True
			if tag['class'] == ['album-title']:
				self.result['album']          = _string.replace("《",' ').replace("》",' ').strip()
				self.result['high']['album']  = _high_list	
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
		search_url = self.url % qword
		# 下载之
		content = urllib2.urlopen(search_url).read()
		# soup对象
		soup = BeautifulSoup(content)
		# 清空song_info
		self.song_info.clear()
		# 寻址之
		soup.find_all(self.find_song_info)
		# 显示之
		self.show()

def test_baidu(url,word):
	SB = SearchBadiu(url)
	SB.start(word)

#test_baidu('http://music.baidu.com/search/song?key=%s','我的歌声')