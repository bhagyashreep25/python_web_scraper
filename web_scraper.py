import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def getAndParseURL(url):
	result = requests.get(url)
	soup = BeautifulSoup(result.text, 'html.parser')
	return soup

def getcategoriesURLs(url):
	soup = getAndParseURL(url)
	categories_urls = ["/".join(url.split("/")[:-1]) + "/" + x.get('href') for x in soup.find_all("a", 
		href=re.compile("catalogue/category/books"))]
	categories_urls = categories_urls[1:]
	return categories_urls

def getProductURLs(url):
	soup = getAndParseURL(url)
	booksURLs = []
	booksURLs.extend(getBooksURLs(url, soup))
	return booksURLs

def getBooksURLs(url, soup):
	product_urls = ["/".join(url.split("/")[:-4]) + "/" + x.div.a.get('href')[9:] for x in soup.findAll("article", class_ = "product_pod")]
	return product_urls

def getProductDetails(booksURLs):
	names = []
	prices = []
	nb_in_stock = []
	img_urls = []
	categories = []
	ratings = []

	# scrape data for every book URL
	for url in booksURLs:
		print(url)
		s = getAndParseURL(url)
		# product name
		names.append(s.find("div", class_ = re.compile("product_main")).h1.text)
		# product price
		prices.append(s.find("p", class_ = "price_color").text[2:]) # get rid of the pound sign
		# number of available products
		nb_in_stock.append(re.sub("[^0-9]", "", s.find("p", class_ = "instock availability").text)) # get rid of non numerical characters
		# image url
		img_urls.append(url.replace("index.html", "") + s.find("img").get("src"))
		# product category
		cat = s.find("a", href = re.compile("../category/books/")).get("href").split("/")[3].split('_')[0]
		categories.append(s.find("a", href = re.compile("../category/books/")).get("href").split("/")[3].split('_')[0])
		# ratings
		ratings.append(s.find("p", class_ = re.compile("star-rating")).get("class")[1])

	scraped_data = pd.DataFrame({'name': names, 'price': prices, 'nb_in_stock': nb_in_stock, "url_img": img_urls, "product_category": categories, "rating": ratings})
	scraped_data.head()
	scraped_data.to_excel("outputs/"+cat+".xlsx")


# main
url = "http://books.toscrape.com/index.html"
# soup = getAndParseURL(url)
categories_list = getcategoriesURLs(url)
# print(categories_list)
for category in categories_list:
	listofbooks = getProductURLs(category)
	print(str(len(listofbooks)))
	print(listofbooks)
	getProductDetails(listofbooks)