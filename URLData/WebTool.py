"""
*------------------------------------------------------------ 
* Model : WebTool 
* Version : 1.2
* Designer : XSky123
*
* About URL,Page...
* 伦家会努力让你喜欢的～喵～～
*------------------------------------------------------------
"""
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error,http.cookiejar,gzip
import re
# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1  

def Replace_Char(x):
	# 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
	BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")

	# 用非 贪婪模式 匹配 任意<>标签
	EndCharToNoneRex = re.compile("<.*?>")

	# 用非 贪婪模式 匹配 任意<p>标签
	BgnPartRex = re.compile("<p.*?>")
	CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
	CharToNextTabRex = re.compile("<td>")

	# 将一些html的符号实体转变为原始符号
	replaceTab = [("<","<"),(">",">"),("&","&"),("&","\""),(" "," ")]
	x = BgnCharToNoneRex.sub("",x)
	x = BgnPartRex.sub("\n    ",x)
	x = CharToNewLineRex.sub("\n",x)
	x = CharToNextTabRex.sub("\t",x)
	x = EndCharToNoneRex.sub("",x)

	for t in replaceTab:  
		x = x.replace(t[0],t[1])  
	return x 

def Opener(cookie=""):
	head = {
	'Connection': 'Keep-Alive',
	'Accept': 'text/html, application/xhtml+xml, */*',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
	}
	if(cookie!=""):
		head['Cookie']=cookie
		# cj = http.cookiejar.CookieJar()
	opener = urllib.request.build_opener()
	header = []
	for key, value in head.items():
		elem = (key, value)
		header.append(elem)
	opener.addheaders = header
	return opener
def OpenURL(URL,charset="utf-8"):
	if(URL.startswith("http://")==0):
		URL="http://"+URL
	opener=Opener()
	htmlOriginal =opener.open(URL, timeout = 1000).read()
	# print("Access"+URL+"Finished")
	htmlSource=""
	# socket=urllib.request.urlopen(URL)
	if(htmlOriginal.startswith(b'\x1f\x8b')):
		htmlOriginal=gzip.decompress(htmlOriginal).decode(charset)
		htmlSource=htmlOriginal
	else:
		if(charset != "utf-8"):
			htmlSource=htmlOriginal.decode(charset)
		else:
			htmlSource=htmlOriginal

	return htmlSource
def OpenURL_BS(URL,charset="utf-8"):
	soup=BeautifulSoup(OpenURL(URL,charset))
	# print("BeautifulSoup"+URL+"Finished")
	return soup