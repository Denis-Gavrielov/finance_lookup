'''
27/09/2017

This programme is designed to help me speed up my US stock trading research by 
automating web searches through web scraping methods. 
It asks for a US stock ticker and returns the stock's chart (in different time 
frames), key financials, recent SEC quarterly/yearly reports and  
the three most recent news stories and press releases found on finance.yahoo.

It prints the progress on scraping finance.yahoo in the text editor. After 10 attempts 
to request the news stories or press releases it will skip this task. 

Note that the programme is done for my productivity and not to look fancy. 

If you want to reach out or are testing this programme and have any recommendations 
then please let me know via email (d.gavrielov@icloud.com). 
I am always happy to improve myself. :)
'''

from tkinter import * 
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import codecs
import csv
from sec_scrapping import SECScraper as sec #my own class that gets SEC data
from news_scraping import NewsScraper as ns #own class that gets yahoo data
import webbrowser #for hyperlinks

class TickerInfo:

	def __init__(self, root):
		self.root = root
		self.create_top_frame()
		root.title('Ticker Info')
		self.count = 0
	
		#self.create_ticker_display_frame()

	def create_top_frame(self):
		''' creates the top frame that will ask for the ticker '''
		Label(self.root, text='Enter ticker (e.g. "AAPL", "MSFT", "TSLA"):').grid(row=0, column=0, sticky=W)
		self.ticker = StringVar()
		Entry(self.root, width=6, textvariable=self.ticker).grid(row=0, column=1, sticky=W)
		Button(self.root, text='get info', command=self.get_info).grid(row=0, column=2, sticky=W)
		self.chart_type = 'yearly'

	def get_info(self):
		''' gets the ball rolling after a ticker was put in '''
		if not self.ticker.get():
			return
		self.get_chart()
		self.ask_for_specific_chart()
		self.display_yahoo()
		self.filings()
		self.articles()


	#chart: 
	def get_chart(self): #, chart_type='yearly'):
		''' gets the chart: currently: daily chart from bigcharts
		to do: specify which chart we want '''
		ticker = str(self.ticker.get()).upper()
		urls = {'yearly': 'http://bigcharts.marketwatch.com/quickchart/quickchart.asp?symb=' + ticker + '&insttype=&freq=&show=', 
		'1 Month': 'http://bigcharts.marketwatch.com/quickchart/quickchart.asp?symb=' + ticker + '&insttype=&freq=1&show=&time=4',
		'5 Days': 'http://bigcharts.marketwatch.com/quickchart/quickchart.asp?symb=' + ticker + '&insttype=&freq=7&show=&time=3',
		'Intraday': 'http://bigcharts.marketwatch.com/quickchart/quickchart.asp?symb=' + ticker + '&insttype=&freq=9&show=&time=1'}
		url = urls[self.chart_type]
		html = urlopen(url)
		soup = BeautifulSoup(html, 'html.parser')
		try:
			image = soup.find('td', {'class' : 'padded vatop'}).contents[1]['src']


			image2 = urlretrieve(image, 'image.gif')

			self.photo = PhotoImage(file='image.gif')
			self.label = Label(self.root, image=self.photo)
			self.label.grid(row=2, column=0, sticky=W)
		except:

			self.label = Label(self.root, text='No chart available\nCheck for typos!')
			self.label.grid(row=2, column=0)


	def ask_for_specific_chart(self):
		''' puts buttons that if clicked will updated the chart to yearly, 1 month,
		5 days or intrady ''' 

		self.chart_time = Listbox(self.root)
		self.chart_time.insert(0, 'yearly (default)')
		self.chart_time.insert(0, '1 Month')
		self.chart_time.insert(0, '5 Days')
		self.chart_time.insert(0, 'Intraday')
		self.chart_time.grid(row=2, column=1, sticky=W)

		Button(self.root, text='update chart', command=self.update_chart).grid(row=2, column=1, sticky=SW)

	def update_chart(self):
		''' takes a chart time and then refreshes the chart '''
		curser = self.chart_time.curselection()[-1]
		types = {0: 'Intraday', 1: '5 Days', 2: '1 Month', 3: 'yearly'}
		self.chart_type = types[curser]
		self.get_chart()


	#yahoo: 
	def int_to_millions(self, number):
		''' takes an int and turns it into a millions format '''
		
		try:
			if int(number) > 100000:
				n = ('{:.1f}M'.format(int(number)/1000000))
			else:
				n = ('{:.1f}K'.format(int(number)/1000))
		except ValueError:
			n = 'N/A'

		return n

	def two_decimals(self, number):
		''' takes a float and formats it to only two decimals '''
		return ('{:.2f}'.format(float(number)))


	def display_yahoo(self):
		''' opens the yahoo information, also closes the old information if
		there is any '''
		self.get_yahoo()
		if self.count > 0:
			self.label_1.grid_forget()
			self.label_2.grid_forget()
			self.label_3.grid_forget()
			self.label_4.grid_forget()

			self.label_6.grid_forget()
			self.label_7.grid_forget()
		self.count += 1 

		self.label_1 = Label(self.root, text=self.ticker_name)
		self.label_1.grid(row=1	, column=0, sticky = W)
		self.label_2 =Label(self.root, text=self.change)
		self.label_2.grid(row=3, column=0, sticky = W)
		self.label_3 = Label(self.root, text=self.volume)
		self.label_3.grid(row=4, column=0, sticky = W)
		self.label_4 = Label(self.root, text=self.high_52)
		self.label_4.grid(row=5, column=0, sticky = W)
		self.label_6 = Label(self.root, text=self.low_52)
		self.label_6.grid(row=6, column=0, sticky = W)
		self.label_7 = Label(self.root, text=self.float)
		self.label_7.grid(row=7, column=0, sticky = W)

	def get_yahoo(self):
		''' gets the ticker data from the API ''' 
		ticker = str(self.ticker.get()).upper()
		url = 'http://finance.yahoo.com/d/quotes.csv?s=' + ticker +'&f=nf6cvkj'
		req = urlopen(url)
		f = codecs.getreader('utf8')(req)
		for row in csv.reader(f):
			self.ticker_name = row[0]
			self.float = str('Public Float: ') + self.int_to_millions(row[1])
			change = row[2].split()
			self.change = '$ Change: ' + change[0] + '\n% Change: ' + change[2]
			self.volume = 'Volume: ' + self.int_to_millions(row[3])
			self.high_52 = '52 Week High: ' + self.two_decimals(row[4])
			self.low_52 = '52 Week Low: ' + self.two_decimals(row[5]) 

	# SEC: 
	def filings(self):
		''' prints the links for latest 10-Q and 10-K filings '''
		ticker = str(self.ticker.get()).upper()

		self.count2 = 0
		if self.count2 > 0:
			self.link1.grid_forget()
			self.link2.grid_forget()
		self.count2 += 1 

		if sec.get_10Q(self, ticker) == '':
			self.link1 = Label(self.root, text='Quarterly report not available', fg='black')
			self.link1.grid(row=3, column=1, sticky = W)
		else:
			self.link1 = Label(self.root, text='Most recent quarterly report', fg='blue', cursor='hand2')
			self.link1.grid(row=3, column=1, sticky = W)
			self.link1.bind('<Button-1>', self.callback1)

		if sec.get_10K(self, ticker) == '':
			self.link2 = Label(self.root, text='Yearly report not available\nNote: Yearly/Quarterly reports not available for foreign companies', fg='black')
			self.link2.grid(row=4, column=1, sticky = W)			

		else:
			self.link2 = Label(self.root, text='Most recent yearly report', fg='blue', cursor='hand2')
			self.link2.grid(row=4, column=1, sticky = W)
			self.link2.bind('<Button-1>', self.callback2)


	def callback1(self, x):
		''' creates hyperlink for 10-Q '''
		ticker = str(self.ticker.get()).upper()
		webbrowser.open_new(sec.get_10Q(self, ticker))

	def callback2(self, x):
		''' creates hyperlink for 10-K '''
		ticker = str(self.ticker.get()).upper()
		webbrowser.open_new(sec.get_10K(self, ticker))


	# News Articles:
	def articles(self):
		''' prints the links for latest articles ''' 
		ticker = str(self.ticker.get()).upper()
		self.news = ns.get_yahoo_news(self, ticker)
		self.press = ns.get_yahoo_press_releases(self, ticker)

		if self.count > 1:
			try:
				self.news1.grid_forget()
				self.news2.grid_forget()
				self.news3.grid_forget()
			except AttributeError:
				pass

			try:
				self.error1.grid_forget()
			except AttributeError:
				pass

			try:
				self.press1.grid_forget()
				self.press2.grid_forget()
				self.press3.grid_forget()

			except AttributeError:
				pass

			try:
				self.error2.grid_forget()
			except AttributeError:
				pass

		#news 
		news_headline = Label(self.root, text='Recent news articles')
		news_headline.grid(row=6, column=1, sticky = NW)

		try:
			self.news1 = Label(self.root, text=self.news[0][0], fg='blue', cursor='hand2')
			self.news1.grid(row=7, column=1, sticky = NW)
			self.news1.bind('<Button-1>', self.callback3)

			self.news2 = Label(self.root, text=self.news[1][0], fg='blue', cursor='hand2')
			self.news2.grid(row=8, column=1, sticky = NW)
			self.news2.bind('<Button-1>', self.callback3_1)

			self.news3 = Label(self.root, text=self.news[2][0], fg='blue', cursor='hand2')
			self.news3.grid(row=9, column=1, sticky = NW)
			self.news3.bind('<Button-1>', self.callback3_2)
		except:
			self.error1 = Label(self.root, text='News not available :(', fg='black')
			self.error1.grid(row=7, column=1, sticky = NW)
		
		try:
			if self.news1:
				try:
					self.error1.grid_forget()
				except AttributeError:
					pass
		except:
			pass
		# press releases
		press_headline = Label(self.root, text='\nRecent press releases')
		press_headline.grid(row=10, column=1, sticky = NW)

		try:
			self.press1 = Label(self.root, text=self.press[0][0], fg='blue', cursor='hand2')
			self.press1.grid(row=11, column=1, sticky = NW)
			self.press1.bind('<Button-1>', self.callback4)

			self.press2 = Label(self.root, text=self.press[1][0], fg='blue', cursor='hand2')
			self.press2.grid(row=12, column=1, sticky = NW)
			self.press2.bind('<Button-1>', self.callback4_1)

			self.press3 = Label(self.root, text=self.press[2][0], fg='blue', cursor='hand2')
			self.press3.grid(row=13, column=1, sticky = NW)
			self.press3.bind('<Button-1>', self.callback4_2)
		except:
			self.error1 = Label(self.root, text='Press releases not available :(', fg='black')
			self.error1.grid(row=11, column=1, sticky = NW)

		try:
			if self.press1:
				try:
					self.error2.grid_forget()
				except AttributeError:
					pass
		except:
			pass

	def callback3(self, x):
		''' creates hyperlink for news'''
		ticker = str(self.ticker.get()).upper()
		webbrowser.open_new(self.news[0][1])

	def callback3_1(self, x):
		ticker = str(self.ticker.get()).upper()
		webbrowser.open_new(self.news[1][1])

	def callback3_2(self, x):
		ticker = str(self.ticker.get()).upper()
		webbrowser.open_new(self.news[2][1])

	def callback4(self, x):
		''' creates hyperlink for press releases '''
		ticker = str(self.ticker.get()).upper()
		webbrowser.open_new(self.press[0][1])

	def callback4_1(self, x):
		''' creates hyperlink for press releases '''
		ticker = str(self.ticker.get()).upper()
		webbrowser.open_new(self.press[1][1])

	def callback4_2(self, x):
		''' creates hyperlink for press releases '''
		ticker = str(self.ticker.get()).upper()
		webbrowser.open_new(self.press[2][1])


def main():
	root = Tk()
	TickerInfo(root)
	root.mainloop()

main()