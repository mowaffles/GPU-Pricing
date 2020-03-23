#Adapted from https://blog.datahut.co/scraping-ebay/

#from scipy import stats
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib import style
import csv

item_name = []
prices = []
dates = []

def writeCSV(filename):
	global item_name
	global prices
	global dates
	with open(filename, mode='w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		
		csv_writer.writerow(['Name', 'Price', 'Date'])	#Write header row
		for i in range(0, len(item_name)):
			csv_writer.writerow([item_name[i], prices[i], dates[i] ])

def readCSV(filename):
	global item_name
	global prices
	global dates
	with open(filename) as csv_file:
		print("Reading CSV...")
		csv_reader = csv.reader(csv_file)
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				#print(f'Column names are {", ".join(row)}')
				line_count += 1
			else:
				item_name.append(row[0])
				prices.append(float(row[1]))
				dates.append(row[2])
				#print(f'\t{row[0]} : {row[1]} : {row[2]}.')
				line_count += 1
		print(f'Processed {line_count} lines.')

def scraper(urlObj):
	global item_name
	global prices
	global dates
	for i in range(1,(urlObj[1] + 1)):
		ebayUrl = urlObj[0] + str(i)
		r= requests.get(ebayUrl)
		data=r.text
		soup=BeautifulSoup(data)
	
		listings = soup.find_all('li', attrs={'class': 's-item'})
	
		for listing in listings:
			prod_name=" "
			prod_price = " "
			for name in listing.find_all('h3', attrs={'class':"s-item__title"}):
				if(str(name.find(text=True, recursive=False))!="None"):
					prod_name=str(name.find(text=True, recursive=False))
					item_name.append(prod_name)
	
			if(prod_name!=" "):
				price = listing.find('span', attrs={'class':"s-item__price"})
				prod_price = price.get_text()
				prod_price = prod_price.replace("£","")
				prod_price = prod_price.replace(",","")
				prod_price = float(prod_price)
				prices.append(prod_price)

			if(prod_name!=" "):
				date = listing.find('span', attrs={'class':"s-item__ended-date"})
				prod_date = date.get_text()
				dates.append(prod_date)
		
		print("Current page:",i)

	for i in range(0, len(item_name)): #Raw output
		print("Item: ", i, " | Name: ", item_name[i], " | Price: ", prices[i],  " | Date: ", dates[i])

	#reverse all lists
	item_name = list(reversed(item_name))
	prices = list(reversed(prices))
	dates = list(reversed(dates))

def removeTi():
	global item_name
	global prices
	global dates
	#Remove 1080Ti entries
	toDelete = []
	for i in range(0, len(item_name)):
		if ( ((item_name[i]).find("Ti") != -1) or ((item_name[i]).find("TI ") != -1) ):
			#print(item_name[i])
			toDelete.insert(0,i)
	#toDelete = list(reversed(toDelete))	#Flip to avoid
	for elem in toDelete:
		del item_name[elem]
		del prices[elem]
		del dates[elem]

def removeSuper():
	global item_name
	global prices
	global dates
	#Remove 1080Ti entries
	toDelete = []
	for i in range(0, len(item_name)):
		if ( ((item_name[i]).find("Super") != -1) or ((item_name[i]).find("TI ") != -1) ):
			#print(item_name[i])
			toDelete.insert(0,i)
		elif ( ((item_name[i]).find("SUPER") != -1) or ((item_name[i]).find("TI ") != -1) ):
			#print(item_name[i])
			toDelete.insert(0,i)
	#toDelete = list(reversed(toDelete))	#Flip to avoid
	for elem in toDelete:
		del item_name[elem]
		del prices[elem]
		del dates[elem]

def graphing():
	global item_name
	global prices
	global dates

	#Graphing
	style.use('ggplot')
	
	dateString = str(dates[0] + " -- " + dates[len(dates)-1])

	plt.subplot(211)
	plt.plot(prices)
	plt.xlabel(dateString)
	plt.ylabel("Price (£)")

	plt.subplot(212)
	plt.boxplot(prices, vert=False)
	plt.show()

def printData():
	output = pd.DataFrame({"Name":item_name, "Prices": prices, "Date": dates})
	pd.set_option('display.max_rows', len(item_name))
	print (output)

def main():
	GTX1080 = ["https://www.ebay.co.uk/b/NVIDIA-GeForce-GTX-1080-Computer-Graphics-Video-Cards/27386/bn_100742202?LH_ItemCondition=3000&LH_Sold=1&rt=nc&_sop=13&_pgn=", 4]
	GTX1070 = ["https://www.ebay.co.uk/b/NVIDIA-GeForce-GTX-1070-NVIDIA-Computer-Graphics-Video-Cards/27386/bn_100736487?LH_ItemCondition=3000&LH_Sold=1&rt=nc&_sop=13&_pgn=", 6]
	RTX2060 = ["https://www.ebay.co.uk/b/Industrial-NVIDIA-GeForce-RTX-2060-Computer-Graphics-Video-Cards/27386/bn_7116613730?LH_ItemCondition=3000&LH_Sold=1&rt=nc&_sop=13&_pgn=", 2]
	RTX2070 = ["https://www.ebay.co.uk/b/NVIDIA-GeForce-RTX-2070-NVIDIA-Computer-Graphics-Video-Cards/27386/bn_7116470210?LH_ItemCondition=3000&LH_Sold=1&rt=nc&_sop=13&_pgn=", 1]
	RTX2080 = ["https://www.ebay.co.uk/b/NVIDIA-GeForce-RTX-2080-NVIDIA-Computer-Graphics-Video-Cards/27386/bn_7116471402?LH_ItemCondition=3000&LH_Sold=1&rt=nc&_sop=13&_pgn=", 1]
	RTX2080Ti = ["https://www.ebay.co.uk/b/NVIDIA-GeForce-RTX-2080-Ti-NVIDIA-Computer-Graphics-Video-Cards/27386/bn_7116466367?LH_ItemCondition=3000&LH_Sold=1&rt=nc&_sop=13&_pgn=", 1]

	#scraper(RTX2080Ti)
	readCSV("RTX2080.csv")
	removeTi()
	removeSuper()
	printData()
	#writeCSV("RTX2080Ti.csv")
	graphing()

main()