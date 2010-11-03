#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup as Soup
import sys, os
from markdown import markdown
import re
from datetime import datetime, date, timedelta
import subprocess
from codecs import open

def td_total_seconds(td):
	return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
def td_set_total_seconds(secs):
	ms = secs * 10**6
	secs = int(secs)
	days = int(secs/24*3600)
	secs = secs % (24*3600)
	return timedelta(days, secs, ms)

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
		with open(fpath,'r',encoding="utf-8") as ff:
			md = ff.read()
		ht = markdown(md)
		s = Soup(ht)
		numwords = len([i for i in findwords(s) if re.search('\w',i)])
		print "%s\t%s\t%s"%(os.path.basename(path) , f , numwords)
		sum += numwords
print "total\t\t%d"%sum
percent = (100.0 * (float(sum)/target))
print "You are %02.2f%% of where you need to be."%percent
#if sum > target:
#	dt = sum / rate
#	writeby= dstart + dt
#	print "You will be behind if you don't write by %s"%(writeby.isoformat())


with open('README.markdown','r') as md:
	lines = md.readlines()

found=False
for i in range(0,len(lines)):
	if "Latest wordcount:" in lines[i]:
		found = i
wcline = "Latest wordcount: %s (%02.2f%% @ %s)"%(sum, percent, datetime.now().isoformat())
if i:
	lines[i] = wcline
else:
	lines.append("")
	lines.append(wcline)
with open('README.markdown','w') as md:
	md.write("".join(lines))

subprocess.Popen('git add README.markdown',shell=True,stdin=sys.stdin,stdout=sys.stdout,stderr=sys.stderr).wait()
