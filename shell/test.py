#coding=utf-8
import urllib2
from bs4 import BeautifulSoup

_360_url ="http://s.music.so.com/s?q=因为爱情&c=kuwo"

content  = urllib2.urlopen(_360_url).read()
soup = BeautifulSoup(content)
print soup.originalEncoding

print content
_360_tab_arr=['虾米音乐','一听音乐','酷狗音乐','酷我音乐']
_360_tab_map={
	'虾米音乐' : 'xiami' ,
	'一听音乐' : 'yiting',
	'酷狗音乐' : 'kugou' ,
	'酷我音乐' : 'kuwo'  ,
}
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
			print "%2d\t%-40s\t|\t%-30s\t|\t%-20s\t" % (count,item['title']+"--"+item['high']['title'],item['artist']+"--"+item['high']['artist'],item['album']+"--"+item['high']['album'])
			#print "%-40s\t\t%-30s\t\t%-20s\t" % (item['high']['title'],item['high']['artist'],item['high']['album'])

song_info = SongInfo('kuwo') 
result={}
result['high']={}

all_num=0


def tab_360(tag):
	global song_info
	global all_num
	global result

	if tag.name =='a' and tag.has_key('class') and tag.attrs['class'] == ['js-tabs-sel']:
		tab_name = tag.contents[0].encode('utf-8').split('(')[0]
		tab_num  = int(tag.contents[0].encode('utf-8').split('(')[1].split(')')[0])
		if tab_name in _360_tab_arr :
			print _360_tab_map[tab_name]
			print tab_num
			all_num = tab_num
			song_info.set_all_num(tab_num)

	if tag.name == 'a' and len(tag.attrs)==3 and tag.has_key('href') and \
	   tag.has_key('target') and tag.has_key('title') and \
	   tag['target'] in ['360Play','_blank']  :

		high_text = ''
		if tag.parent.a.em != None :
			high_text = tag.parent.a.em.string.encode('utf-8')
		
		if tag.parent['class'] == ['title'] :
			# print tag['title'].encode('utf-8')
			result['title']=tag['title'].encode('utf-8')
			result['high']['title'] = high_text 

		if tag.parent['class'] == ['artist'] :
			# print tag['title'].encode('utf-8')
			result['artist']=tag['title'].encode('utf-8')
			result['high']['artist'] = high_text 

		if tag.parent['class'] == ['album'] :
			# print tag['title'].encode('utf-8')
			result['album']=tag['title'].encode('utf-8')
			result['high']['album'] = high_text 

			# insert it 
			song_info.append_result(result)
			result={}
			result['high'] = {}

	return False


soup.find_all(tab_360)


song_info.show()