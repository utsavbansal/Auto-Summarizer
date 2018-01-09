import requests
import urllib2
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
from math import log
from sklearn.feature_extraction.text import TfidfVectiorizer
from sklearn.cluster import KMeans

def getwashposturl(url,token):
	try:
		page=urllib2.urlopen(url).read().decode('utf8')
	except:
		return None,None
	soup=BeautifulSoup(page)
	if soup is None:
		return None,None
	text=""
	if soup.find_all(token) is not None:
		text=''.join(map(lambda p: p.text,soup.find_all(token)))
		soup2=BeautifulSoup(text)
		if soup2.find_all('p')!=[]:
			text=''.join(map(lambda p: p.text,soup2.find_all('p')))
	return text,soup.title.text

def getnytext(url,token):
	response=requests.get(url)
	soup=BeautifulSoup(response.content)
	page=str(soup)
	title=soup.find('title').text
	mydivs=soup.findAll("p",{"class":"story-body-text story-content"})
	text=''.join(map(lambda p:p.text,mydivs))
	return text,title

def scrapesource(url,magicfrag='2015',scraperfunction=getnytext,token='None'):
	urlbodies={}
	request=urllib2.Request(url)
	response=urllib2.urlopen(request)
	soup=BeautifulSoup(response)
	numerrors=0
	for a in soup.findAll('a'):
		try:
			url=a['href']
			if url not in urlbodies and magicfrag is not None and magicfrag in url or magicfrag is None:
				body=scraperfunction(url,token)
				if body and len(body)>0:
					urlbodies[url]=body
				print url
		except:
			numerrors+=1
	return urlbodies


class FrequencySummarizer:
	def __init__(self,min_cut=0.1,max_cut=0.9):
		self._min_cut=min_cut
		self._max_cut=max_cut
		self._stopwords=set(stopwords.words('english')+list(punctuation)+[u"'s",'"'])
	
	def _compute_frequencies(self,word_sent,customstopwords=None):
		freq=defaultdict(int)
		if customstopwords is None:
			stopwords=set(self._stopwords)
		else:
			stopwords=set(customStopWords).union(self._stopwords)
		for s in word_sent:
			for word in s:
				if word not in stopwords:
					freq[word]+=1
		m=float(max(freq.values()))
		for w in freq.keys():
			freq[w]=freq[w]/m
			if freq[w]>=self._max_cut or freq[w]<=self._min_cut:
				del freq[w]
		return freq

	def extractfeatures(self,article,n,customStopWords=None):
		text=article[0]
		title=article[1]
		sentences=sent_tokenize(text)
		word_sent=[word_tokenize(s.lower()) for s in sentences]
		self._freq=self._compute_frequencies(word_sent,customStopWords)
		if n<0:
			return nlargest(len(self._freq_keys()),self._freq,key=self._freq.get)
		else:
			return nlargest(n,self._freq,key=self._freq.get)
	def extractrawfrequencies(self,article):
		text=article[0]
		title=article[1]
		sentences=sent_tokenize(text)
		word_sent=[word_tokenize(s.lower()) for s in sentences]
		freq=defaultdict(int)
		for s in word_sent:
			for word in s:
				if word not in self._stopwords:
					freq[word]+=1
		return freq
	def summarize(self,article,n):
		text=article[0]
		title=article[1]
		sentences=sent_tokenize(text)
		word_sent=[word_tokenize(s.lower()) for s in sentences]
		self._freq=self._compute_frequencies(word_sent)
		ranking= defaultdict(int)
		for i,sentence in enumerate(word_sent):
			for word in sentence:
				if word in self._freq:
					ranking[i]+=self._freq[word]
		sentences_index=nlargest(n,ranking,key=ranking.get)
		return [sentences[j] for j in sentences_index]



