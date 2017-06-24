# Kavitha Madhavaraj #
#Necessary Variables
host = "localhost"
port = 27017
dataDB = "techstore"
collection = "techdata"


#Links to be used according to category
links_to_scrape = { 
					"http://www.designnews.com":"designnews",\
				    "http://www.sciencealert.com":"sciencealert", \
				    "http://spectrum.ieee.org":"ieeespectrum"\
				  }
links_rss       = {
					"http://phys.org/rss-feed/":"phys_org",\
					"https://www.technologyreview.com/stories.rss":"technologyreview",\
					"http://www.dailymail.co.uk/sciencetech/index.rss":"dailymail"\
				  }
