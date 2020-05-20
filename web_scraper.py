import requests
from bs4 import BeautifulSoup
import re

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


# main
url = "http://books.toscrape.com/index.html"
# soup = getAndParseURL(url)
categories_list = getcategoriesURLs(url)
# print(categories_list)
for category in categories_list:
	listofbooks = getProductURLs(category)
	print(str(len(listofbooks)))
	print(listofbooks)
