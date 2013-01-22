#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-15, 20:05:00 
# @file search_360.py
# @author zihuacs(zihuacs@qq.com)
# @brief 抓取360音乐歌曲检索首页结果，非首页忽略之--->1ting,kuwo,kugou,xiami
#--------------------------------------------------------------------- 
import urllib2
import time
from bs4 import BeautifulSoup
from song_info import *
from urllib import quote

# 360各标签map
TAB_NAME_360MAP={
	'酷我音乐' : 'kuwo',
	'一听音乐' : '1ting',
	'酷狗音乐' : 'kugou',
	'虾米音乐' : 'xiami',
	'kuwo'     : '酷我音乐',
	'1ting'    : '一听音乐',
	'kugou'    : '酷狗音乐',
	'xiami'    : '虾米音乐'
}

class Search360:
	'''
	url : http://s.music.so.com/s?q=%s&c=%s
	type: in ['xiami','1ting','kuwo','kugou'] 
	'''
	def __init__(self,url,qtype):
		self.song_info = SongInfo(qtype)
		self.url       = url 
		self.type      = qtype 
		
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
	360的仅需直接返回即可，无需类似b一样拼接
	'''
	def get_link(self,tag):
		_a_link = tag.attrs['href'].encode('utf-8')
		return _a_link


	'''
	tag: soup处理的当前标签，从合适的tag中抽取num、title、artist、album、high
	封装到result里
	result={'title':'...','artist':'...','album':'...','high':{'title':[],'artist':[],'album':[]}}
	'''
	def find_song_info(self,tag):
		# 抓取结果数		
		if tag.name =='a' and tag.has_key('class') and tag.attrs['class'] == ['js-tabs-sel']:
			tab_name = tag.contents[0].encode('utf-8').split('(')[0].strip()
			tab_num  = int(tag.contents[0].encode('utf-8').split('(')[1].split(')')[0])
			if tab_name == TAB_NAME_360MAP[self.type] :
				self.all_num = tab_num
				self.song_info.set_all_num(tab_num)
		# 抓取song信息 但必须保证self.all_num > 0
		if self.all_num >0 and tag.name == 'a' and len(tag.attrs)==3 and tag.has_key('href') and \
		   tag.has_key('target') and tag.has_key('title') and tag['target'] in ['360Play','_blank'] :

			_high_list = self.get_high_list(tag.find_all('em'))
			_a_link    = self.get_link(tag)
			if tag.parent['class'] == ['title'] :
				self.result['title']=tag['title'].encode('utf-8')
				self.result['high']['title'] = _high_list 
				self.result['link']['title'] = _a_link
				return True

			if tag.parent['class'] == ['artist'] :
				self.result['artist']=tag['title'].encode('utf-8')
				self.result['high']['artist'] = _high_list 
				self.result['link']['artist'] = _a_link
				return True

			if tag.parent['class'] == ['album'] :
				self.result['album']=tag['title'].encode('utf-8')
				self.result['high']['album'] = _high_list
				self.result['link']['album'] = _a_link

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
		search_url = self.url % (quote(qword),self.type)
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
def get_search_360_res(url,qword,qtype):
	S3 = Search360(url,qtype)
	S3.start(qword)
	s360_song_info = S3.get_song_info()
	return s360_song_info

def test_360(url,qword,qtype):
	S3 = Search360(url,qtype)
	S3.start(qword)
	S3.show()

#test_360('http://s.music.so.com/s?q=%s&c=%s','因为爱情','kuwo')
#get_search_360_res('http://s.music.so.com/s?q=%s&c=%s','因为爱情','kuwo')