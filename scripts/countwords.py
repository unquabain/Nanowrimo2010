#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup as Soup
import sys, os
from markdown import markdown
import re
from datetime import datetime, date, timedelta

def td_total_seconds(td):
	return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

dstart = datetime(2010,11,1)
dend   = datetime(2010,12,1)
dnow   = datetime.now()

numwords = 50000.0

Dtotal = dend - dstart
Dtonow = dnow - dstart

rate = numwords/td_total_seconds(Dtotal)
target = rate * td_total_seconds(Dtonow)



def findwords(soup):
	for e in soup:
		if e.string:
			for w in e.string.split(): yield w
		else:
			for w in findwords(e): yield w

sum = 0

for path, dirs, files in os.walk(os.getcwd()):
	if not re.search('/2010-11-\d\d$',path): continue
	for f in files:
		fpath = os.path.join(path,f)
		with open(fpath,'r') as ff:
			md = ff.read()
		ht = markdown(md)
		s = Soup(ht)
		numwords = len([i for i in findwords(s) if re.search('\w',i)])
		print "%s\t%s\t%s"%(os.path.basename(path) , f , numwords)
		sum += numwords
print "total\t\t%d"%sum
print "You are %02.2f%% of where you need to be."%(100.0 * (float(sum)/target))
