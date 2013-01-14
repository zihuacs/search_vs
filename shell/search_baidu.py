#coding=utf-8
import urllib2
import re
from bs4 import BeautifulSoup

_baidu_url ="http://music.baidu.com/search/song?key=我的歌声里"

content  = urllib2.urlopen(_baidu_url).read()
soup = BeautifulSoup(content)
print soup.originalEncoding


class SongInfo:

	# results = [{'title':'...','artist':'...','album':'...','high':{'title':'...','artist':'...','album':'...'}},..]
	# src_type must in ['baidu','xiami','yiting','kugou','kuwo']
	def __init__(self,src_type):
		self.results  =[]
		self.src_type =src_type
		self.all_num  =0

	def set_all_num(self,all_num):
		self.all_num = all_num
	
	# result= {'title':'...','artist':'...','album':'...','high':{'title':'...','artist':'...','album':'...'}}
	def append_result(self,result):
		self.results.append(result)

	def show(self):
		print "type : %s" % self.src_type
		print "all_num : %d" % self.all_num
		count=0
		for item in self.results:
			count = count+1
			print "%2d\t%-40s\t|\t%-30s\t|\t%-20s\t" % (count,item['title'],item['artist'],item['album'])
			#print "%-40s\t\t%-30s\t\t%-20s\t" % (item['high']['title'],item['high']['artist'],item['high']['album'])

song_info = SongInfo('baidu') 
result={}
result['high']={}

all_num=0

'''
em_list = [<em><em>因为爱情</em></em>, <em> 因为爱情  </em>]
return high_list = [因为爱情] 
'''
def get_high_list(em_list):
	high_list = []
	for high_item in em_list:
		high_word = str(high_item).replace('<em>','').replace('</em>','')
		if not high_word.strip() in high_list:
			high_list.append(high_word.strip())
	return high_list

def tab_baidu(tag):
	global song_info
	global all_num
	global result

	if tag.name == 'li' and tag.has_key('class') and tag['class'][0] == 'ui-tab-active' :
		tab_name = tag.a.string.encode('utf-8').split('(')[0]
		tab_num  = int(tag.a.string.encode('utf-8').split('(')[1].split(')')[0])
		if tab_name in ['歌曲']:
			all_num = tab_num
			song_info.set_all_num(tab_num)
			return True

	if tag.name == 'span' and tag.has_key('class') and tag.has_key('style') and \
	   tag['class'] in [['song-title'],['singer'],['album-title']]:
		
		_string    = tag.get_text().encode('utf-8').strip().replace('\n',' ')
		_high_list = get_high_list(tag.find_all('em'))

		if tag['class'] == ['song-title']:
			result['title']          = _string.strip().split(' ')[0]
			result['high']['title']  = _high_list

		if tag['class'] == ['singer']:
			result['artist']         = _string.replace('/',',').replace('\t',' ').replace(' ','')
			result['high']['artist'] = _high_list

		if tag['class'] == ['album-title']:
			result['album']          = _string.replace("《",' ').replace("》",' ').strip()
			result['high']['album']  = _high_list	
			
			song_info.append_result(result)
			result={}
			result['high']={}
	return False


print soup.find_all(tab_baidu)


song_info.show()