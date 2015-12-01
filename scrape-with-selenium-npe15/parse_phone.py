import json
import re

fh = open("results.json", "r")
scrape_list = fh.readlines()
fh.close()

for each_scrape in scrape_list:
	scrape_data = json.loads(each_scrape)
	try:
		print(re.findall(r"P: [0-9( )-+-.]+", scrape_data["info"])[0])
	except:
		pass