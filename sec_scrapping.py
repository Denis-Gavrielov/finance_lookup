from urllib.request import urlopen
from bs4 import BeautifulSoup

class SECScraper:
	''' gets the right SEC files '''

	def __init__(self):
		self.get_10K()


	def get_10Q(self, ticker='AAPL'):
		''' takes in a ticker and gets the latest 10-Q url ''' 
		url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK='+ticker+'&Find=Search&owner=exclude&action=getcompany'
		html = urlopen(url)
		soup = BeautifulSoup(html, 'html.parser')

		n = 0
		while n < 5: 
			# here I am trying to get the 10-Q from the current page 
			# if the 10-Q is not in the first 40 filings, I will try
			# getting the next 40 filings. In total I am looking at 800
			# filings before giving up on finding a 10-K
			n += 1
			try:
				ten_Q = soup.find('td', text='10-Q').next_siblings
				if ten_Q != None:
					break
			except AttributeError: 
				next_page = soup.find('input', {'value' : 'Next 40'})
				new_url = 'https://www.sec.gov' + next_page['onclick'].replace('parent.location=', '').strip("'")
				html = urlopen(new_url)
				soup = BeautifulSoup(html, 'html.parser')

		try:
			if ten_Q == None:
				return ('')
		except:
			return ('')


		i = 0
		for sibling in ten_Q:
			if i == 2:
				break
			i += 1
			ten_Q2 = sibling.find('a')

		new_link = ten_Q2['href']

		html = urlopen('https://www.sec.gov' + new_link)
		soup2 = BeautifulSoup(html, 'html.parser')

		ten_Q = soup2.find('td', text='10-Q').next_siblings
		i = 0
		for sibling in ten_Q:
			if i == 2:
				break
			i += 1
			ten_Q2 = sibling.find('a')

		new_link = ten_Q2['href']
		final_url = 'https://www.sec.gov' + new_link


		return (final_url)

	def get_10K(self, ticker='AMZN'):
		''' takes in a ticker and get the latest 10-K url '''
		url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK='+ticker+'&Find=Search&owner=exclude&action=getcompany'
		html = urlopen(url)
		soup = BeautifulSoup(html, 'html.parser')

		n = 0
		while n < 5: 
			# here I am trying to get the 10-K from the current page 
			# if the 10-K is not in the first 40 filings, I will try
			# getting the next 40 filings. In total I am looking at 800
			# filings before giving up on finding a 10-K
			n += 1
			try:
				ten_K = soup.find('td', text='10-K').next_siblings

				if ten_K != None:
					break
			except AttributeError: 
				next_page = soup.find('input', {'value' : 'Next 40'})
				new_url = 'https://www.sec.gov' + next_page['onclick'].replace('parent.location=', '').strip("'")
				html = urlopen(new_url)
				soup = BeautifulSoup(html, 'html.parser')


		try:
			if ten_K == None:
				return ('')
		except:
			return ('')


		i = 0
		for sibling in ten_K:
			if i == 2:
				break
			i += 1
			ten_K2 = sibling.find('a')

		new_link = ten_K2['href']

		html = urlopen('https://www.sec.gov' + new_link)
		soup2 = BeautifulSoup(html, 'html.parser')


		ten_K = soup2.find('td', text='10-K').next_siblings

		i = 0
		for sibling in ten_K:
			if i == 2:
				break
			i += 1
			ten_K2 = sibling.find('a')
			if ten_K2 == None:
				ten_K2 = sibling.parent.find('a')

		new_link = ten_K2['href']

		final_url = 'https://www.sec.gov' + new_link
		
		return (final_url)


SECScraper()