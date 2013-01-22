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
import time
from bs4 import BeautifulSoup
from song_info import *
from urllib import quote

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
		self.all_num        =0
		self.result         ={'title':'','artist':'','album':'','high':{},'link':{}}
		self.result['high'] ={'title':[],'artist':[],'album':[]}
		self.result['link'] ={'title':'','artist':'','album':''}
		self.a_link         = ''

	'''
	return self.song_info
	'''
	def get_song_info(self):
		return self.song_info

	'''
	just for test 
	'''
	def find_a(self,tag):
		if tag.name == 'a' and tag.has_key('href'):

			if self.a_link == '':
				self.a_link = tag.attrs['href'].encode('utf-8')
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
	get a link
	'''
	def get_link(self,tag):
		tag.find(self.find_a)
		_a_link     = self.a_link
		self.a_link = ''
		return "http://music.baidu.com"+_a_link.strip('')
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
			_a_link    = self.get_link(tag)
			if tag['class'] == ['song-title']:
				if tag.a != None:
					_string = tag.a.get_text().encode('utf-8').strip().replace('\n',' ')
				self.result['title']          = _string.strip()
				self.result['high']['title']  = _high_list
				self.result['link']['title']  = _a_link
				return True
			if tag['class'] == ['singer']:
				self.result['artist']         = _string.replace('/',',').replace('\t',' ').replace(' ','')
				self.result['high']['artist'] = _high_list
				self.result['link']['artist']  = _a_link

				return True
			if tag['class'] == ['album-title']:
				self.result['album']          = _string.replace("《",' ').replace("》",' ').strip()
				self.result['high']['album']  = _high_list	
				self.result['link']['album']  = _a_link
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
		search_url = self.url % quote(qword)
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
		self.song_info.set_search_url( search_url )
		soup.find_all(self.find_song_info)

'''
根据url and word return song_info
'''
def get_search_baidu_res(url,word):
	SB = SearchBadiu(url)
	SB.start(word)
	badiu_song_info = SB.get_song_info()
	return badiu_song_info

def test_baidu(url,word):
	SB = SearchBadiu(url)
	SB.start(word)
	SB.show()


#test_baidu('http://music.baidu.com/search/song?key=%s','我的歌声里')
#get_search_baidu_res('http://music.baidu.com/search/song?key=%s','即刻出发')
