import requests
import json
import csv
import os
import schedule
import time
import xml.etree.ElementTree as ET

from pymongo import MongoClient

client = MongoClient("141.142.209.153",27017)
air_db = client['air_quality_data']
air_quality = air_db['simple_cities']

def uploadDataToServer(dataSet):

	air_quality.insert(dataSet)

	print "upload finished"


def air_parser(URL, URL2, city_name):

	#base_URL = "http://www.stateair.net/web/rss/1/1.xml"
	#URL = base_URL ##+ "count=" + counting + "&offset=" + offset
	result = requests.get(URL)
	result2 = requests.get(URL2)

	#print result.text

	root = ET.fromstring(result.text)
	#root2 = ET.fromstring(result2.text)

	#city_name = "Beijing"

	temp = []

	for item in root[0]:

		if(item.tag == "item"):
			time = item.find("title").text
			PM25 = item.find("Conc").text
			AQI = item.find("AQI").text

			## from URL2
			xml_data = result2.text.split('\n')[1:]

			data1 = xml_data[10]
			data2 = xml_data[12]

			weather = data1.split(': ')[1].split(', ')[0]
			windSpeed = data2.split('Wind Speed: ')[1].split('mph')[0] #unit mph
			windDirection = data2.split('Wind Direction: ')[1].split(', ')[0]
			## end of URL2

			entry = {"city":city_name ,"time":time, "Concentration":PM25, "AQI":AQI, 
					"weather":weather, "windSpeed":windSpeed, "windDirection":windDirection}
			temp.append(entry)

			break
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
			for i in reversed(range(0, 1)):
				samplewriter.writerow([temp[i]['time'], temp[i]['city'], temp[i]['Concentration'], 
									temp[i]['AQI'], temp[i]['weather'], temp[i]['windSpeed'], 
									temp[i]['windDirection']])
	else: ## file already exists ##
		filename_output = city_name + ".csv"
		with open(filename_output, 'a') as outfile:
			# init the writer #
			samplewriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
			# write first line #
			samplewriter.writerow(['Time', 'City', 'Concentration', 'AQI', 
									'Weather', 'Wind_Speed', 'Wind_Direction'])
			# saved number should be less than 10 #
			for i in reversed(range(0, 1)):
				samplewriter.writerow([temp[i]['time'], temp[i]['city'], temp[i]['Concentration'], 
									temp[i]['AQI'], temp[i]['weather'], temp[i]['windSpeed'], 
									temp[i]['windDirection']])

	print city_name + "job is done."

	uploadDataToServer(temp)

	#print temp


#########################
##### Main Function #####
#########################

air_parser('http://www.stateair.net/web/rss/1/1.xml', 
			'http://open.live.bbc.co.uk/weather/feeds/en/1816670/observations.rss', 
			'Beijing')
air_parser('http://www.stateair.net/web/rss/1/2.xml', 
			'http://open.live.bbc.co.uk/weather/feeds/en/1815286/observations.rss',
			'Chengdu')
air_parser('http://www.stateair.net/web/rss/1/3.xml',
			'http://open.live.bbc.co.uk/weather/feeds/en/1809858/observations.rss',
			'Guangzhou')
air_parser('http://www.stateair.net/web/rss/1/4.xml',
			'http://open.live.bbc.co.uk/weather/feeds/en/1796236/observations.rss',
			'Shanghai')
air_parser('http://www.stateair.net/web/rss/1/5.xml',
			'http://open.live.bbc.co.uk/weather/feeds/en/2034937/observations.rss', 
			'Shenyang')

def job1():
	air_parser('http://www.stateair.net/web/rss/1/1.xml', 
			'http://open.live.bbc.co.uk/weather/feeds/en/1816670/observations.rss', 
			'Beijing')
	print "Beijing job is on schedule"
def job2():
	air_parser('http://www.stateair.net/web/rss/1/2.xml', 
			'http://open.live.bbc.co.uk/weather/feeds/en/1815286/observations.rss',
			'Chengdu')
	print "Chengdu job is on schedule"
def job3():
	air_parser('http://www.stateair.net/web/rss/1/3.xml',
			'http://open.live.bbc.co.uk/weather/feeds/en/1809858/observations.rss',
			'Guangzhou')
	print "Guangzhou job is on schedule"
def job4():
	air_parser('http://www.stateair.net/web/rss/1/4.xml',
			'http://open.live.bbc.co.uk/weather/feeds/en/1796236/observations.rss',
			'Shanghai')
	print "Shanghai job is on schedule"
def job5():
	air_parser('http://www.stateair.net/web/rss/1/5.xml',
			'http://open.live.bbc.co.uk/weather/feeds/en/2034937/observations.rss', 
			'Shenyang')
	print "Shenyang job is on schedule"

schedule.every(60).minutes.do(job1)
schedule.every(60).minutes.do(job2)
schedule.every(60).minutes.do(job3)
schedule.every(60).minutes.do(job4)
schedule.every(60).minutes.do(job5)

while True:
	schedule.run_pending()
	time.sleep(60)

#########################
