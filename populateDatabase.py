import time
import pymongo
from bs4 import BeautifulSoup
from urllib2 import urlopen

start_time= time.time()

url = "https://storesserver.ece.illinois.edu/4dcgi/catalog"
raw_html = urlopen(url).read()
soup = BeautifulSoup(raw_html)

client = pymongo.MongoClient()
db=client.ecestore
collection = db.catalog





def getCategoryPages():
	ret = []
	searchString = "https://storesserver.ece.illinois.edu/4dcgi/catalog/fromcatalog"
	for link in soup.find_all("a"):
		href = link.get("href")
		title= link.string
		if searchString in href:
			ret.append((title,href))
	return ret


def analyzePage(cat,url):
	raw_html = urlopen(url).read()
#	print raw_html
	soup = BeautifulSoup(raw_html)
	print cat

	table=soup.form.table
	print "table: \n"

	#print soup.get_text()
	rows = table.find_all("tr")

	startAnalyzing=0
#	for row in rows:
#		print row
#		print "-------------------------------------------------------------------\n\n\n\n\n\n\n\n"
	for i in range(1,len(rows)):
	#	print str(rows[i])
	#	print "qwerty" + str(startAnalyzing)
	#	print type(rows[i])
	#	print rows[i].attrs
		if "valign" in rows[i].attrs:
			if rows[i]["valign"] == "middle":
				analyzeEntry(cat,rows[i])
	

def analyzeEntry(cat,row):

	fields = row.find_all("td")
	cat          = cat                       .encode("utf-8")
	barcode      = fields[0].p.string.strip().encode("utf-8")
	part_number  = fields[1].p.string.strip().encode("utf-8")
	description  = fields[2].p.string.strip().encode("utf-8")
	manufacturer = fields[3].p.string.strip().encode("utf-8")
	pricestr     = fields[4].p.string.strip().encode("utf-8").strip("$")
	price        = float(pricestr)
	price        = int(price*100)/100.0
	obj = {
		"category"	: cat,
		"barcode" 	: barcode,
		"part_number"	: part_number,
		"description"	: description,
		"manufacturer"	: manufacturer,
		"price"		: price
	      }

	collection.insert(obj)

	print cat + "\t" + description + "\t" + str(price)


for entry in getCategoryPages():
	analyzePage(entry[0],entry[1])


end_time = time.time()

print str(start_time-end_time) + "s"
