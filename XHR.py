


import requests
import re
import json
from lxml import html

#有些网站的内容不是静态的，而是动态生成的，这样用lxml直接去扒就没用了。下面是一种处理这种网站的办法。

#先使用chrome的开发者工具（网页上右键：审查代码），然后点击Network，点击XHR (XMLHttpRequest)，通过它可以查看，当你进入某个网页（或者网页中的某个子标题）时，
#是否有ajax请求，如果有的话，它会列出具体的请求网址(如下面这个硬code。找到这个网址，就可以进行抓取。 
#用JsonViewer之类的工具打开它，观察它的结构，然后写下面代码
jsContent = requests.get('http://36kr.com/api/post?column_id=67&b_id=&per_page=20&_=1509701373197')
jsDict = json.loads(jsContent.content)

#注意： 这个结构可能是因网站而异的，不是都一样的
jsData = jsDict['data']
jsItems = jsData['items']

for item in jsItems:
    contentUrl = "http://36kr.com/p/"+str(item['id'])+".html"
    print(contentUrl)

    