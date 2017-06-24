# Kavitha Madhavaraj #
import feedparser
import time

def aggregate(link, filename):
	finalData = []
	response = feedparser.parse(link)

	for i  in range(0, len(response.entries)):
		feed = response.entries[i]
		data = {}
		if 'author' in feed:
			data['author'] = feed['author']
		if 'link' in feed:
			data['url'] = feed['link']
		if 'title' in feed:
			data['title'] = feed['title']
		if 'tags' in feed:
			data['keywords'] = [feed['category']]
		if 'summary' in feed:
			data['summary'] = feed['summary']
		data['date'] = time.strftime("%d/%m/%Y")
		data['score'] = -1;
		finalData.append(data)
	result = {link : finalData}    
	return result

