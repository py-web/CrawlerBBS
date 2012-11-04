
# -*- coding: utf-8 -*-
import urllib2
import re
import sys
from sgmllib import SGMLParser
        
# spider engine to get all the link of a target link
Dic = {}

#the spider engine for sina blog
class parser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.url = []
        self.is_td = False
        self.is_just = False
        
    def start_td(self,attrs):
        href = [v for k,v in attrs if k == 'class' or k == 'width']
        if len(href) == 2 and href[0].find('TableBody') != -1 and href[1] == '*':
            self.is_td = True
        elif len(href) == 2 and href[0].find('TableBody') != -1 and href[1] == "175":
            self.is_td = False
            
            
    def handle_data(self,attrs):
        if self.is_td and attrs != " ":
            self.url.append(attrs)
            self.is_just = True
            
    def start_br(self,attrs):
        if self.is_just:
            self.url.append('\n')
            self.is_just = False
            
link = urllib2.urlopen("http://bbs.whu.edu.cn/wForum/disparticle.php?boardName=Electronics&ID=1105510034&pos=20")
html = link.read()
st = parser()
html = html.decode('gbk','ignore').encode('utf-8')

f = open("2.txt","w")
typ = sys.getfilesystemencoding()
#st.feed(html.decode("GB2312").encode('utf-8'))
st.feed(html)
#tar = u"发信人"
#print st.url[12].find(tar)
page = 1
is_lou = 0
is_end = False
poster_e = ""
poster_c = ""
poster_title = ""
poster_time = ""
poster_content = []
final = []
is_start = False
sts = ""
fn = [] 
for item in st.url:
    if page == 1:
        if item != '\n':
            sts = sts + item
        else:
            final.append(sts)
            sts = ""

for item in final:
    ans = ""
    tp = item.split("\r\n")
    for st in tp:
        if st:
           ans = st
    fn.append(ans)
tf = open("3.txt","w")
is_post_end = False
for item in fn:
    tf.write(item)
    tf.write('\n')
    if item.find("发信人") == 0 and not is_start:
        name = item.split(":")[1].split("(")
        poster_e = name[0]
        is_start = False
        is_end = False
        poster_c = name[1].split(")")[0]
    elif item.find(' 标 题:') == 0 and not is_start:
        poster_title = item.split("标 题:")[1]
        if poster_title.find(' Re:') == 0:
            is_re = 1
        else:
            is_lou = 1
    elif item.find(' 发信站: 珞珈山水') == 0:
        poster_time = item.split('(')[1].split(')')[0]
        is_start = True
    elif item.find(' --') == 0:
        is_end = True
        is_start = False
    else:
        if item.find("※ 来源") == -1  and not is_end and is_start:
            poster_content.append(item)
        elif item.find("※ 来源") != -1:
            is_end = False
            is_start = False
            f.write('ID:\r')
            f.write(poster_e)
            f.write('\n')
            f.write('name\r')
            f.write(poster_c)
            f.write('\nTitle:\r')
            f.write(poster_title)
            f.write(str(is_lou))
            f.write('\nContent:\r')
            for each in poster_content:
                f.write(each)
                f.write('\n\r')
            f.write('time:\r')
            f.write(poster_time)
            f.write('\n\n')
            is_lou = 0
            poster_c = ""
            poster_e = ""
            poster_title = ""
            poster_content = []
            poster_time = ""