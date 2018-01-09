from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest

class FrequencySummarizer:
	def __init__(self,min_cut=0.1,max_cut=0.9):
		self._min_cut=min_cut
		self._max_cut=max_cut
		self._stopwords=set(stopwords.words('english')+list(punctuation))
	
	def _compute_frequencies(self,word_sent):
		freq=defaultdict(int)
		for s in word_sent:
			for word in s:
				if word not in self._stopwords:
					freq[word]+=1
		m=float(max(freq.values()))
		for w in freq.keys():
			freq[w]=freq[w]/m
			if freq[w]>=self._max_cut or freq[w]<=self._min_cut:
				del freq[w]
		return freq
	def summarize(self,text,n):
		sents=sent_tokenize(text)
		assert n<=len(sents)
		word_sent=[word_tokenize(s.lower()) for s in sents]
		self._freq=self._compute_frequencies(word_sent)
		ranking=defaultdict(int)
		for i,sent in enumerate(word_sent):
			for w in sent:
				if w in self._freq:
					ranking[i]+=self._freq[w]
		sents_idx=nlargest(n,ranking,key=ranking.get)
		return [sents[j] for j in sents_idx]
import urllib2
from bs4 import BeautifulSoup

def get_only_text(url):
	page=urllib2.urlopen(url).read().decode('utf8')
	soup=BeautifulSoup(page,"lxml")
	text=''.join(map(lambda p:p.text,soup.find_all('article')))
	soup2=BeautifulSoup(text,"lxml")
	if soup2.find_all('p')!=[]:
		text=''.join(map(lambda p:p.text,soup2.find_all('p')))
	return soup.title.text,text

someurl="https://www.washingtonpost.com/news/the-switch/wp/2015/08/06/why-kids-are-meeting-more-strangers-online-than-ever-before/"
textofurl=get_only_text(someurl)
fs=FrequencySummarizer()
summary=fs.summarize(textofurl[1],3)

print summary
			
