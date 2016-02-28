import requests
import json
import csv
import os.path
import schedule
import time
import xml.etree.ElementTree as ET



def air_parser(URL, city_name, saved_number):

	#base_URL = "http://www.stateair.net/web/rss/1/1.xml"
	#URL = base_URL ##+ "count=" + counting + "&offset=" + offset
	result = requests.get(URL)

	#print result.text

	root = ET.fromstring(result.text)

	#city_name = "Beijing"

	temp = []

	for item in root[0]:

		if(item.tag == "item"):
			time = item.find("title").text
			PM25 = item.find("Conc").text
			AQI = item.find("AQI").text
			entry = {"city":city_name ,"time":time, "PM2.5":PM25, "AQI":AQI}
			temp.append(entry)
		else:
			print "this is not an record"

		#print (item.tag == "item")

	if(os.path.isfile(city_name + ".csv")):
		print city_name + "file already exists"
		filename_output = city_name + ".csv"
		with open(filename_output, 'a') as outfile:
			# init the writer #
			samplewriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
			# saved number should be less than 10 #
			for i in reversed(range(0, saved_number)):
				samplewriter.writerow([temp[i]['time'], temp[i]['city'], temp[i]['PM2.5'], temp[i]['AQI']])
	else: ## file already exists ##
		filename_output = city_name + ".csv"
		with open(filename_output, 'a') as outfile:
			# init the writer #
			samplewriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
			# write first line #
			samplewriter.writerow(['time', 'city', 'PM2.5', 'AQI'])
			# saved number should be less than 10 #
			for i in reversed(range(0, saved_number)):
				samplewriter.writerow([temp[i]['time'], temp[i]['city'], temp[i]['PM2.5'], temp[i]['AQI']])

	print city_name + "job is done."
	#print temp


#########################
##### Main Function #####
#########################

air_parser('http://www.stateair.net/web/rss/1/1.xml', 'Beijing', 24)
air_parser('http://www.stateair.net/web/rss/1/2.xml', 'Chengdu', 24)
air_parser('http://www.stateair.net/web/rss/1/3.xml', 'Guangzhou', 24)
air_parser('http://www.stateair.net/web/rss/1/4.xml', 'Shanghai', 24)
air_parser('http://www.stateair.net/web/rss/1/5.xml', 'Shenyang', 24)

def job1():
	air_parser('http://www.stateair.net/web/rss/1/1.xml', 'Beijing', 1)
	print "Beijing job is on schedule"
def job2():
	air_parser('http://www.stateair.net/web/rss/1/2.xml', 'Chengdu', 1)
	print "Chengdu job is on schedule"
def job3():
	air_parser('http://www.stateair.net/web/rss/1/3.xml', 'Guangzhou', 1)
	print "Guangzhou job is on schedule"
def job4():
	air_parser('http://www.stateair.net/web/rss/1/4.xml', 'Shanghai', 1)
	print "Shanghai job is on schedule"
def job5():
	air_parser('http://www.stateair.net/web/rss/1/5.xml', 'Shenyang', 1)
	print "Shenyang job is on schedule"

schedule.every(1).minutes.do(job1)
schedule.every(1).minutes.do(job2)
schedule.every(1).minutes.do(job3)
schedule.every(1).minutes.do(job4)
schedule.every(1).minutes.do(job5)

while True:
	schedule.run_pending()
	time.sleep(60)

#########################
