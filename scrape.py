# Kavitha Madhavaraj #

from bs4 import BeautifulSoup
import json
import requests
from requests import Session
import time
import string
import unirest
import httplib

links = []
unirest.timeout(20)

def extractKeywords(data):
	words = data.split(",") 
	return words

def find_metadata(url):
	try:
		r  = requests.get(url)
	except requests.exceptions.ConnectionError as e:
		yield null
		yield null
	data = r.text
	soup = BeautifulSoup(data, "html.parser")
	if soup.find(attrs={"name":"author"}):
		yield unicode(soup.find(attrs={"name":"author"})['content']).replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "").encode('ascii','ignore').strip()
	else:
		yield "null"	
	if soup.find(attrs={"name":"keywords"}):
		yield unicode(soup.find(attrs={"name":"keywords"})['content']).replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "").encode('ascii','ignore').strip()
	else:
		yield "null"

def get_links(url,temp,link):
	global links
	data = {}
	data['url'] = url + temp
	#data['summary'], keywords1 = summary(url+temp);
	data['author'], keywords2 = find_metadata(data['url'])
	data['keywords']= extractKeywords(keywords2)
	if(data['author'] == "null"):
		del data['author']
	#if(data['summary'] == ""):
	#	del data['author']
	if(data['keywords'] == "null"):
		del data['keywords']
	data['date'] = time.strftime("%d/%m/%Y")
	data['score'] = -1;
	data['title'] = unicode(''.join(link.findAll(text=True))).replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "").encode('ascii','ignore').strip()
	#print data
	if((data['url'] != "") and (data['title'] != "") and (len(data['title'])> 8)):
		links.append(data)

def getAdditionalData(url):
	print url
	if(url.startswith('http://www.designnews.com/')):
		url ="http://www.designnews.com/author.asp?"+ (url.split('&'))[1]
	try:
		response1 = unirest.get("https://joanfihu-article-analysis-v1.p.mashape.com/link?entity_description=False&link="+url,	headers={ "X-Mashape-Key": "ZoMXvZg49BmshFBZmBeqnvQgFQm3p1Fp8ZIjsnofdHTsYLLKn7","Accept": "application/json"   })
		if((response1 != None) & (response1.body != None)):
			yield ''.join(str(statement.encode('utf-8')) for statement in response1.body['summary'])
			yield response1.body['entities']
			#print ''.join(str(statement.encode('utf-8')) for statement in response1.body['summary'])
		else:
			print response1
			raise response1
	except httplib.BadStatusLine:
		yield None
		yield []
	except Exception as e:
		if("502" in str(e)):
			yield None
			yield []
		else:
			print e
			yield None
			yield []


def do_scrape(url,filename):
	global links
	del links[:]
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, "html.parser")
	for link in soup.find_all('a'):
		temp = link.get('href')
		if temp:
			# Hack ! To remove nicenews default links
			if filename == "nicenews" and (temp.startswith("http://www.nice.org.uk/news/article/") or temp.startswith("http://www.nice.org.uk/news/feature/")):
					get_links("",temp,link)
			# Hack ! To remove ieeespectrum default links like tech, health etc
			if filename == "ieeespectrum" and temp.startswith("/") and len(temp)>15:
				if not temp.startswith("/static"):
					get_links(url,temp,link)
			# Hack ! To remove sciencealert's default links like tech, health etc
			if filename == "sciencealert" and temp.startswith("/") and len(temp)>21:
				get_links(url,temp,link)
			# Hack ! To remove designnews unnecessary old post and site-specific posts
			if filename == "designnews" and temp[0]!= '.' and temp[0]!= '#' and not temp.startswith("http"):
				if (not temp.startswith('/author') and not temp.startswith('/content')):
					get_links(url,temp,link)
				if temp.startswith('/author.asp?section_id') and not temp.endswith('analysis_element'):
					get_links(url,temp,link)	
				elif (temp.startswith('/document') and not (temp.endswith('yes'))):
					get_links(url,temp,link)	
		else:
			continue

	uniqueData= []
	finalData = []

	for item in links:
		if item['url'] not in uniqueData:
			uniqueData.append(item['url'])
			item['summary'], temp = getAdditionalData(item['url'])
			if(item['summary'] is None):
				del item['summary']
			if len(temp) > 0:
				item['keywords'] = temp + item['keywords'] 
				if("null" in item['keywords']):
					item['keywords'].remove("null")
				if("" in item['keywords']):
					item['keywords'].remove("")
			if(item['keywords'] is None):
				del item['keywords']
			
			finalData.append(item)

	result = { url: finalData }
	del uniqueData
	del finalData
	return result
	#with open(eval('filename')+'.json', 'w') as outfile:
	#		json.dump(result, outfile, indent = 4 , sort_keys = False)
	
	
