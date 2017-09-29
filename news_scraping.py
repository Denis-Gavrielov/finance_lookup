from urllib.request import urlopen
from bs4 import BeautifulSoup

class NewsScraper:
	''' gets news headlines and links '''

	def __init__(self):
		''' start '''
		#self.get_yahoo_news()
		pass

	def get_yahoo_news(self, ticker='AAPL'):
		''' goes on the yahoo website and returns a list of tuples with news 
		headlines and their links ''' 

		n = 0
		while n < 10:
			n += 1
			url = 'https://finance.yahoo.com/quote/' + ticker + '/news?p=' + ticker
			html = urlopen(url)
			soup = BeautifulSoup(html, 'lxml')

			articles = []
			children = soup.find('ul', {'class' : 'Mb(0) Ov(h) P(0) Wow(bw)'})
			for child in children:
				x = child.find('h3', {'class' : 'Mb(5px)'})
				if x != None:
					
					sublink = x.find('a')['href']
					link = 'http://finance.yahoo.com' + sublink
					title = x.find('a').get_text()
					articles.append((title, link))
			print(articles)
			if articles != []:
				break

		return articles


	def get_yahoo_press_releases(self, ticker='AAPL'):
		''' goes on the yahoo website and returns a list of tuples with news
		headlines and their links ''' 
		
		n = 0
		while n < 10:
			n += 1

			url = 'http://finance.yahoo.com/quote/' + ticker + '/press-releases?p=' + ticker
			html = urlopen(url)
			soup = BeautifulSoup(html, 'lxml')

			articles = []
			children = soup.find('ul', {'class' : 'Mb(0) Ov(h) P(0) Wow(bw)'})
			for child in children:
				x = child.find('h3', {'class' : 'Mb(5px)'})
				if x != None:
					link = 'https://finance.yahoo.com' + x.find('a')['href']
					title = x.find('a').get_text()
					articles.append((title, link))
			print(articles)
			if articles != []:
				break
		return articles


NewsScraper()


