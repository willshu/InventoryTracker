#!/usr/bin/python3
import time
import datetime
import requests
from bs4 import BeautifulSoup
import logging
import json
import asyncio
import concurrent.futures
import aiohttp
from scraper_settings import urls, api

logging_filename = "scraper" + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
logging.basicConfig(filename=logging_filename, filemode='a', level='INFO', format='%(asctime)-15s - %(message)s')

class Product():
	def __init__(self, name, price, url, stock):
		self.name = name
		self.price = price
		self.url = url
		self.stock = bool(stock)
	def __repr__(self):
		return json.dumps(self.__dict__)
	def __eq__(self, other):
	 	return self.__dict__ == other.__dict__
	def __hash__(self):
		return hash((self.name, self.price, self.url))


async def api_call(product, session):
	headers = api['headers']
	url_get = api['url_get']
	url_put_post = api['url_put_post']
	async with session.get(url_get + product.name, headers=headers) as resp:
		resp.raise_for_status()
		ret = await resp.json()
		if not ret:
			r = await session.post(url_put_post, data=json.dumps(product.__dict__), headers=headers)
			logging.info("Posting new item {} to inventory".format(product.name))
			print(f"{json.dumps(product.__dict__)}")
		else:
			r = await session.put(url_put_post + str(ret[0]['id']) +'/', data=json.dumps(product.__dict__), headers=headers)
			logging.info("Updating {} in inventory".format(product.name))
		return r

async def get_html(url, session):
	try:
		async with session.get(url) as resp:
			resp.raise_for_status()
			html = await resp.text()
			return html
	except aiohttp.client_exceptions.ClientResponseError:
		logging.info(f'404 error {url}')
		return None

def try_get_inventory(func): # wrapper function to retry on failures
	def wrapper(*args, **kwargs):
		while True:
			try:
				result = func(*args, *kwargs)
			except AssertionError:
				logging.info("Returned zero results, retrying")
				time.sleep(10)
			else:
				return result
	return wrapper

@try_get_inventory
async def get_inventory (urls, session, loop: asyncio.AbstractEventLoop): # loop through the URLs, build a list of Products
	tasks = []
	inventory = []
	for url in urls:
		tasks.append(loop.create_task(get_html(url, session)))
	for task in tasks:
		html = await task
		if html is not None:
			soup = BeautifulSoup(html, 'html.parser')
			products = soup.find_all(attrs={"class" : "card"})
			inventory += parse_products(products)
	assert len(inventory) != 0 # get_inventory occasionally returns no results and no exception
	return inventory	

def parse_products(products):
	inventory = []
	for product in products:
		name = product["data-name"]
		link = product.find('a', {'data-event-type': 'product-click'})['href']
		cost = product.find('span', {'class': 'price price--withoutTax price-section--minor'}).string
		stock = None
		try:
			product.find('a', {'class': 'button button--small card-figcaption-button'}).contents
			stock = True
		except AttributeError:
			stock = False
		inventory.append(Product(name,cost,link,stock))	
	return inventory

async def get_inv_and_post(count):
	loop = asyncio.get_event_loop()
	tasks = []
	async with aiohttp.ClientSession() as session:
		inventory = await get_inventory(urls, session, loop)
		for i in inventory:
			task = loop.create_task(api_call(i, session))
			tasks.append(task)
		await asyncio.gather(*tasks, return_exceptions=True)
	logging.info('Checked website {} times, {} items found'.format(str(count), len(inventory)))

if __name__ == '__main__':
	count = 1
	while True:
		asyncio.run(get_inv_and_post(count))
		count += 1		
		time.sleep(15)




