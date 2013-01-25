#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-25, 11:58:00 
# @file search_sina.py
# @author zihuacs(zihuacs@qq.com)
# @brief 抓取新浪音乐歌曲检索首页结果，非首页忽略之
#--------------------------------------------------------------------- 
import urllib2
import time
from bs4 import BeautifulSoup
from song_info import *
from urllib import quote

class SearchSina:
	'''
	url : http://music.sina.com.cn/yueku/search_new.php?type=song&key=%s
	'''
	def __init__(self,url):
		self.song_info = SongInfo('sina')
		self.url       = url

		self.temp_init()
		self.all_num = 0
	'''
	临时变量初始化 --- 在查找song_info 中使用
	'''
	def temp_init(self):
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
		if tag.name =='div' and tag.has_key('class') and tag['class'] == ['search_A','pt10mlr30']:
			tab_num = int(tag.span.i.get_text())
			self.all_num = tab_num
			self.song_info.set_all_num(tab_num)
			return True

		if self.all_num>0 and tag.name == 'em' and tag.has_key('class') and tag['class'] in [['w190'],['w170']]:
			
			_title = tag.a['title'].encode('utf-8')
			_high_list = self.get_high_list(tag.find_all('span'))
			_link = tag.a['href'].encode('utf-8')

			if tag['class'] == ['w190']:
				self.result['title']         = _title
				self.result['high']['title'] = _high_list
				self.result['link']['title'] = _link
				return True
			if tag['class'] == ['w170']:
				self.result['artist']         = _title
				self.result['high']['artist'] = _high_list
				self.result['link']['artist'] = _link
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
def get_search_sina_res(url,word):
	SA = SearchSina(url)
	SA.start(word)
	sina_song_info = SA.get_song_info()
	return sina_song_info

def test_sina(url,word):
	SA = SearchSina(url)
	SA.start(word)
	SA.show()


#test_sina('http://music.sina.com.cn/yueku/search_new.php?type=song&key=%s','因为爱情')
#get_search_sina_res('http://music.sina.com.cn/yueku/search_new.php?type=song&key=%s','即刻出发')
