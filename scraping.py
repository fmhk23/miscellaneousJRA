#For scraping race pages
import urllib.request
import re

#For scraping horse pages
import pandas as pd
import numpy as np
import html5lib as lib5
import bs4 as bs
import sys

#------------------#
#Get Horse URL List#
#------------------#
RaceURL = sys.argv
html = urllib.request.urlopen(RaceURL[1]).read()
htmlST = str(html)

horseRE= re.compile('/horse/')
URLnum = []*18
URLlist = []*18
URLbase = 'http://db.netkeiba.com/horse/result/'

#http://bi.biopapyrus.net/python/syntax/string.html
i = 0
rank = 1
while i >= 0:
    m = horseRE.search(htmlST, i)
    if m:
        URLnum.insert(rank,m.end())
        URLlist.insert(rank,htmlST[URLnum[rank - 1]:URLnum[rank - 1]+11])
        URLlist[rank - 1] = URLbase + URLlist[rank - 1]
        rank += 1
        i = m.start() + 1
    else:
        break
#Loop END

#-------------------------------#
#Get race results from Horse URL#
#-------------------------------#
i = 0
LoopTimes = rank - 1
for i in range(LoopTimes):
	URL = URLlist[i]

	#Get Table Data
	try:
		base = pd.read_html(URL, flavor='bs4')
	except Exception as e:
		print(e)
		continue

	#convert to DataFrame
	base_df = pd.DataFrame(base[0])

	#Writedown
	FN =  URL[-11:-1] + '.csv'
	base_df.to_csv(FN)
#Loop END