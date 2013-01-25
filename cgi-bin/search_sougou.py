#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-24, 22:13:00 
# @file search_sougou.py
# @author zihuacs(zihuacs@qq.com)
# @brief 抓取搜狗音乐歌曲检索首页结果，非首页忽略之
#--------------------------------------------------------------------- 
import urllib2
import time
from bs4 import BeautifulSoup
from song_info import *
from urllib import quote


class SearchSougou:
	'''
	url : http://mp3.sogou.com/music.so?query=%s
	'''
	def __init__(self,url):
		self.song_info = SongInfo('sougou')
		self.url       = url 
		
		self.temp_init()
		self.all_num=0
		self.next = '' # next in ['artist','album']
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
	em_list = [<font style="color:red;text-decoration:underline;">因为爱情</font>]
	return high_list = [因为爱情] 
	strip+去重
	'''
	def get_high_list(self,em_list):
		high_list = []
		for high_item in em_list:
			high_word = str(high_item).replace('<font style="color:red;text-decoration:underline;">','').replace('</font>','')
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
		if tag.name =='div' and tag.has_key('class') and tag.attrs['class'] == ['rststat']:
			# tag: <div class="rststat">找到约 21,952 <!--resultbarnum:21,952--> 条结果</div>
			tab_num = int(tag.get_text().encode('utf-8').split(' ')[1].replace(',',''))
			self.all_num = tab_num
			self.song_info.set_all_num(tab_num)
			return True

		if self.all_num >0 and tag.name == 'td'  and tag.has_key('class') and \
		   tag['class'] in [['songname'],['singger']]:

			_title     = tag.a['title'].encode('utf-8')
			_high_list = self.get_high_list(tag.find_all('font'))
			_link      = tag.a['href'].encode('utf-8')
			# print _title
			# print _high_list
			# print _link

			if tag['class'] == ['songname']:
				self.result['title']         = _title
				self.result['high']['title'] = _high_list
				self.result['link']['title'] = self.url % quote(_title.decode('utf-8').encode('gbk'))
				self.next = 'artist'
				return True

			if tag['class'] == ['singger']:
				if self.next == '':
					self.next = 'artist'
				tmp_key =self.next 

				self.result[tmp_key]         = _title
				self.result['high'][tmp_key] = _high_list
				self.result['link'][tmp_key] = _link

				if self.next == 'artist':
					self.next = 'album'
				elif self.next == 'album':
					# 加入一条结果
					self.song_info.append_result(self.result)
					# 清空临时变量
					self.temp_init()
					self.next = ''		

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
		# content = content.decode('gbk').encode('utf-8')
		# print content
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
def get_search_sougou_res(url,qword):
	SG = SearchSougou(url)
	SG.start(qword)
	sougou_song_info = SG.get_song_info()
	return sougou_song_info

def test_sougou(url,qword):
	SG = SearchSougou(url)
	SG.start(qword)
	SG.show()

#test_sougou('http://mp3.sogou.com/music.so?query=%s','因为爱情')
#get_search_sougou_res('http://mp3.sogou.com/music.so?query=%s','因为爱情')