import requests as r
import random
from bs4 import BeautifulSoup as bs


class ProxyScraper:
		
	def __init__(self):
		self.proxies = []
		self.headers = self.makeHeader("https://google.com")
		self.testTimeout = 3

	def makeHeader(self, ref):
		return {
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Referer': ref,
			'DNT': '1'
		}
	
	def filterProxy(self, filters, proxy):
		for key in filters:
			if key == 'anonymity' and filters[key] != "*":
				if filters[key] == "*":
					continue
				if filters[key] != proxy[key]:
					return False
			elif key == 'https' and filters[key] != "*":
				if filters[key] != proxy[key]:
					return False
			elif key == 'country' and filters[key] != "*":
				if proxy[key] not in filters[key]:
					return False
		return True

	def loadProxies(self, filters={'anonymity': 'anonymous', 'https': True, 'country': '*'}):

		self.proxies = []

		resp = r.get("https://free-proxy-list.net/", headers=self.headers)
		
		if resp.status_code == 200:
			dom = bs(resp.text, 'html.parser')
			rows = dom.findAll("tr")

			for row in rows:
				try:
					host = row.findAll("td")[0].text
					port = row.findAll("td")[1].text
					proxy = host + ":" + port
					if "." not in proxy:
						break
					anonymity = row.findAll("td")[4].text.strip()
					country = row.findAll("td")[3].text.strip()
					isHTTPS = True if row.findAll("td")[6].text == "yes" else False
					proxyObj = {
							'proxy': proxy,
							'host': host,
							'port': port,
							'anonymity': anonymity,
							'country': country,
							'https': isHTTPS
						}
					if self.filterProxy(filters, proxyObj):
						self.proxies.append(proxyObj)
				except IndexError:
					continue
	
	def testProxy(self, proxyObj):
		proxy = {'http':'http://'+proxyObj['proxy'], 'https':'https://'+proxyObj['proxy']}
		try:
			resp = r.get('http://google.com', proxies=proxy, timeout=self.testTimeout)
			if resp.status_code == 200:
				return True
		except IOError:
			return False


	def getRandomAliveProxy(self):
		for proxy in self.proxies:
			if self.testProxy(proxy) and random.random() > 0.5:
				return proxy
		return None


	def getAliveProxies(self):
		aliveProxies = []
		for proxy in self.proxies:
			if self.testProxy(proxy):
				aliveProxies.append(proxy)
		return aliveProxies


	def getProxies(self):
		return self.proxies

if __name__ == "__main__":
	pm = ProxyScraper()
	pm.loadProxies()
	print(pm.getRandomAliveProxy())
