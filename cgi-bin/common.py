#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-17, 16:37:00 
# @file common.py
# @author zihuacs(zihuacs@qq.com)
# @brief 共享之
#--------------------------------------------------------------------- 
from song_info import *
from conf import *
'''
搜索框功能框 post请求
'''
def show_search_box(qword='',type_list=[],select_type_list=[],func_list=[],func_open_item=''):
	print '''
	<br>
	<br>
	<form action=index.py method=post>
	<table id="mytable" cellspacing="0" align="center"> 
	<caption>
	search_vs_box
	<br>
	'''
	
	print "<input type=text name=qword size=50 value=\"%s\" >" % qword 
	print '<br>'

	for qtype in type_list:
		print qtype
		if qtype in select_type_list:
			print "<input type=\"checkbox\" checked=\"checked\" name=%s>" % qtype
		else:
			print "<input type=\"checkbox\"  name=%s>" % qtype

	print '<br>'

	for qfunc in func_list:
		print qfunc
		if qfunc == func_open_item:
			print "<input type=\"radio\" checked=\"checked\" name=\"func\" value=%s>" % qfunc
		else:
			print "<input type=\"radio\" name=\"func\" value=%s>" % qfunc
	print '<br>'
	print '''
	<input type=submit value="music">
	</caption>
	</table>
	</form>
	'''

'''
prit src_file_path.content
'''
def print_file_content(src_file_path):
	try:
		src_file = open(src_file_path,'r')
	except IOError:
		return False
	# print it
	print src_file.read()
	src_file.close()
	return True
'''
<style type="text/css"> 
css.file.content
</style>
'''
def print_index_style(index_css_path):
	print '<style type="text/css">'
	# print css_scr_file_content
	print_file_content(index_css_path)
	print '</style>'

'''
对 show_str  ... 代之，否则 丑
飘红词 em 之
'''
def high_and_link_str(show_str,high_list,a_link):
	show_str=show_str.strip()
	if show_str.strip()=='':
		show_str='...'
	# highlight it
	for high_word in high_list:
		show_str = show_str.replace(high_word,("<em>%s</em>" % high_word))
	
	return "<a href=\"%s\" target=\"view_window\"> %s </a>" % (a_link ,show_str)
'''
show one song_info_table
'''
def show_song_info_table(song_info,qword,post_info):

	print '''<table id="mytable" cellspacing="0" align="center" width="700px">'''
	# mao tag
	print "<a name=\"%s\"></a>" % song_info.get_src_type() 
	for qtype in post_info['select_type_list']:
		print "<a href=\"#%s\">%s </a>" % (qtype,qtype)

	print '<caption>'
	print "<a href=\"%s\" target=\"view_window\"> %s_music</a> num:%d time:%f" % (song_info.get_search_url() ,song_info.get_src_type(),song_info.get_all_num(),song_info.get_proc_time())
	print '</caption>'

	print '''
	<tr> 
	<th scope="col" >歌曲</th> 
	<th scope="col" >歌手</th> 
	<th scope="col" >专辑</th> 
	<th scope="col" >建议</th>
	</tr>'''
	for item in song_info.get_results():
		print '<tr>' + \
		'<td class="row" width="250px">' + high_and_link_str( item['title'],item['high']['title'],item['link']['title'] )  + '</td>' + \
		'<td class="row" width="150px">' + high_and_link_str( item['artist'],item['high']['artist'],item['link']['artist'] ) + '</td>' + \
		'<td class="row" width="200px">' + high_and_link_str( item['album'],item['high']['album'],item['link']['album'] )  + '</td>'

		up,down = 0,0
		if item.has_key('up'):
			up = item['up']
		if item.has_key('down'):
			down = item['down']

		if up == down:
			sug_str ='→'
		if up > down:
			sug_str = '↑'
		if up < down:
			sug_str = '↓'

		print '<td class="row" >' + sug_str           + '</td>' + '</tr>'
	print '</table>'

'''
body.print
'''
def show_song_info_list_body(song_info_list,post_info):
	print '<body>'
	print '<div class="main_content">'
	# 搜索框
	qword=post_info['qword']
	show_search_box(qword,TYPE_LIST,post_info['select_type_list'],["sug_close","sug_open"],post_info['select_func'])

	for song_info in song_info_list:
		show_song_info_table(song_info,qword,post_info)

	print '</div>'
	print '</body>'

'''
index_css_path : css 样式
song_info_list : [baidu_res,360_res] 
'''
def show_song_info_list_html(index_css_path,song_info_list,post_info):
	print '''<html><head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>music_search better than rd!</title>'''
	print_index_style(index_css_path)
	print '''</head>'''

	show_song_info_list_body(song_info_list,post_info)
	
	print '</html>'
