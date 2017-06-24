# Kavitha Madhavaraj #
from config import links_to_scrape,links_rss
import readandwrite

if __name__ == '__main__':
	print "Started the proces...."
	readandwrite.readAndWrite(links_rss,True)
	readandwrite.readAndWrite(links_to_scrape,False)
