# -*- coding: utf-8 -*-
from parser import *
import urllib2
from urllib2 import URLError
import errno
bbs_index_url = 'http://bbs.whu.edu.cn/wForum/index.php'


class post_obj:
	def __init__(self):
		self.id = ''
		self.poster 

def spider_dfs(url):
    is_legal_url = url.find('http://')
    new_url = ''
    if is_legal_url == -1: #the url is relative path
        if url[0] == '\\':
            new_url = bbs_url + url
        else:
            new_url = bbs_url + '\\' + url
    else:
        new_url = url
    
    if new_url.find('bbs.whu.edu.cn') != -1:
        linkContent = urllib2.urlopen(new_url)
        if linkContent.code == 200:
            parser = bbs_spider()
            parser.feed(linkContent.read())
            for item in parser.url:
                spider_dfs(item)
    return

class BbsSpider:
    def __init__(self ,link):
        self.link = link
        self.board_name_e = []#engine
        self.board_name_c = []#chinese
        self.board_urls = []
    	self.post_id = []
    
    #from index page to get the border name 
    def getIndexPageBoardName(self):
        board_link = urllib2.urlopen(bbs_index_url)
       	if board_link.code == 200:
			board_parser = bbs_index_parser()
			board_parser.feed(board_link.read())
			for item in board_parser.content:
				if item.find('boards[boards.length]') != -1:
					board_name = item.split('\'')
					self.board_name_e.append(board_name[1])
					self.board_name_c.append(board_name[3])
	
	#get all the posts from the url
	def deal(self):
	    pass
	    '''
	    
	    '''
				
    def start(self):
    	#first get the all boardname of index page
       	self.getIndexPageBoardName()
       	#second form new url just like
       	# bbs.whu.edu.cn/wForum/board.php?name=border_name_e[i]
       	for item in self.board_name_e:
			for page_num in range(1,11,1):
				temp_url = 'http://bbs.whu.edu.cn/wForum/board.php?name=' + \
				item + '&page=' + str(page_num)
				self.board_urls.append(temp_url)
       	#third get all t
       	for url_item in self.board_urls:
	        print url_item
	        try:
	            url_link = urllib2.urlopen(url_item)
	        except URLError as e:
	            print e.reason
            if url_link.code == 200:
                id_parser = bbs_id_parser()
				id_parser.feed(url_link.read())
				for item in id_parser.content:
				    if item.find('origin = ') != -1:
					    tmp = item.split('(')[1]
					    tp = tmp.split(',')
					    #self.post_id.append(tp[0])
					    self.deal()
					    f.write(tp[0])
					    f.write('\n')
        '''
#for url in parser.urls:
#    print url
