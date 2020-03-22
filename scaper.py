#Adapted from https://blog.datahut.co/scraping-ebay/

#from scipy import stats
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib import style

item_name = []
prices = []
dates = []


for i in range(1,7):
	GTX1080url = "https://www.ebay.co.uk/b/NVIDIA-GeForce-GTX-1080-Computer-Graphics-Video-Cards/27386/bn_100742202?LH_ItemCondition=3000&LH_Sold=1&rt=nc&_pgn="+str(i)+"&_sop=13&_udlo=100"
	GTX1070url = "https://www.ebay.co.uk/b/NVIDIA-GeForce-GTX-1070-NVIDIA-Computer-Graphics-Video-Cards/27386/bn_100736487?LH_ItemCondition=3000&LH_Sold=1&rt=nc&_pgn="+str(i)+"&_sop=13"

	ebayUrl = GTX1070url
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
			prod_price = float(prod_price)
			prices.append(prod_price)

		if(prod_name!=" "):
			date = listing.find('span', attrs={'class':"s-item__ended-date"})
			prod_date = date.get_text()
			dates.append(prod_date)
	
	print("Current page:",i)

for i in range(0, len(item_name)): #Raw output
	print("Item: ", i, " | Name: ", item_name[i], " | Price: ", prices[i],  " | Date: ", dates[i])



def removeTi():
	#Remove 1080Ti entries
	toDelete = []
	for i in range(0, len(item_name)):
		if ( (item_name[i]).find("Ti") != -1):
			#print(item_name[i])
			toDelete.insert(0,i)
	#toDelete = list(reversed(toDelete))	#Flip to avoid
	for elem in toDelete:
		del item_name[elem]
		del prices[elem]
		del dates[elem]

removeTi()

output = pd.DataFrame({"Name":item_name, "Prices": prices, "Date": dates})
print (output)

#reverse all lists
item_name = list(reversed(item_name))
prices = list(reversed(prices))
dates = list(reversed(dates))

#Graphing
style.use('ggplot')

plt.plot(prices)
plt.show()