#!/usr/bin/env python
from markdown import markdown
import os, sys, re
import subprocess
from codecs import open

template='''\
<!DOCTYPE html>
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>NaNoWriMo 2010 :: %(title)s</title>
<style type="text/css">
html
{
	background-color: #444;
}
body
{
	width: 800px;
	margin: 0px auto;
	background-color: #F8F8F8;
	padding: 2ex 2em;
}
h1
{
	font-size: 24pt;
	background-color: #888;
	color: #444;
	font-family: serif;
	text-shadow: 0px 1px 1px #BBB, 0px -1px 1px black;
	border-radius: 5px;	
	padding: 5px;
	-webkit-border-radius: 5px;	
	-moz-border-radius: 5px;	
}
p
{
	text-align: justify;
	margin-top: 0px;
	margin-bottom: 0px;
	text-indent: 0.25in;
	font-family: serif;
	font-size: 12pt;
	line-height: 20pt;
}
a.prev,
a.next
{
	color: blue;
	-webkit-transition: text-shadow 0.25s ease-in;
}
a.prev:hover,
a.next:hover
{
	color: blue;
	text-shadow: 0px 0px 10px #4444FF;
}
a.prev:visited, a.next:visited
{
	color: blue;
}
</style>
</head>
<body>
<div>
<a class="prev" href="%(prevlink)s">&lt; %(prevtext)s</a> |
<a class="next" href="%(nextlink)s">%(nexttext)s &gt;</a>
</div>
<div class="body">
%(body)s
</div>
<div>
<a class="prev" href="%(prevlink)s">&lt; %(prevtext)s</a> |
<a class="next" href="%(nextlink)s">%(nexttext)s &gt;</a>
</div>
</body>
</html>
'''

published_dir = os.path.join(os.getcwd(),'published')

if not os.path.exists(published_dir):
	os.mkdir(published_dir)


files = []

for d in sorted(os.listdir(os.getcwd())):
	dpath = os.path.join(os.getcwd(),d)
	if not os.path.isdir(d): continue
	if not re.match('2010-11-\d\d',d): continue
	for f in sorted(os.listdir(dpath)):
		m = re.match('chapter_(\d\d).markdown',f)
		if not m: continue
		pubfilename = os.path.join(published_dir, '%s.%02d.html'%(d,int( m.group(1))) )
		files.append( (os.path.join(dpath, f), pubfilename) )

for i, row in enumerate(files):
	mkfile, htfile = row
	mkstream = open(mkfile,'r', encoding='utf-8')
	htstream = open(htfile,'w', encoding='utf-8')
	if (i-1) >= 0:
		prevmkfile, prevhtfile = files[i-1]
		prev_link = os.path.basename(prevhtfile)
		prev_text = prev_link[:-5]
	else:
		prev_link = "#"
		prev_text = "THE BEGINNING"
	if (i+1) < len(files):
		nextmkfile, nexthtfile = files[i+1]
		next_link = os.path.basename(nexthtfile)
		next_text = next_link[:-5]
	else:
		next_link = "#"
		next_text = "THE END"
	htstream.write(template%{
		'title' : os.path.basename(htfile),
		'body'  : markdown(mkstream.read()),
		'nexttext' : next_text,
		'nextlink' : next_link,
		'prevtext' : prev_text,
		'prevlink' : prev_link
		}
	)
	htstream.close()
	mkstream.close()
	subprocess.Popen('git add %s'%htfile,shell=True,stdin=sys.stdin,stdout=sys.stdout,stderr=sys.stderr).wait()
			
