#This python file gather the data from race page.
#(EX)http://race.netkeiba.com/?pid=race_old&id=c201605021110&mode=top
#
#Target data: Frame num, Horse num, Horse name, Odds, Horse ID
#
#Output:a csv file

#----------------#
#Import Libraries#
#----------------#
#For scraping race pages
import urllib.request
import re

import pandas as pd
import numpy as np
import html5lib as lib5
import bs4 as bs
import sys

#-----------------#
#Get Horse ID List#
#-----------------#
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
        URLlist.insert(rank,htmlST[URLnum[rank - 1]:URLnum[rank - 1]+10])
        rank += 1
        i = m.start() + 1
    else:
        break
#Loop END

#-----------------------------#
#Get Basic Info from the Table#
#-----------------------------#
base = pd.read_html(RaceURL[1], flavor='bs4')
base_df = pd.DataFrame(base[0])

L = len(URLlist)

numlist = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
base_df_subset = base_df.ix[3:(3+L),{0,1,3,5,8,9}]
base_df_subset.index = numlist[0:L]

#----------------------------#
#Join 2 pd.DFs and write .csv#
#----------------------------#
URLlist_df = pd.DataFrame(URLlist)
Writedown_df = pd.concat([base_df_subset,URLlist_df],axis =1)
Writedown_df.to_csv("Horsedata_today.csv")