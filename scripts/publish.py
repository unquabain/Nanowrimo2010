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

prev_title = "BEGINNING"
prev_link = "#"
last_title = ""
last_content = ""
last_file = None
last_filename = ""
for path, dirs, files in os.walk(os.getcwd()):
	files.sort()
	
	for fname in files:
		m = re.match('chapter_(\d\d).markdown',fname)
		if not m: continue
		chapnum = int(m.group(1))
		chapname = "%s - %02d"%(os.path.basename(path), chapnum)
		chapfname = "%s.%02d.html"%(os.path.basename(path),chapnum)
		if last_file:
			last_file.write(template%{
				'title' : last_title,
				'body'  : last_content,
				'nexttext' : chapname,
				'nextlink' : chapfname,
				'prevtext' : prev_title,
				'prevlink' : prev_link
				}
			)
			last_file.close()
			subprocess.Popen('git add %s'%last_filename,shell=True,stdin=sys.stdin,stdout=sys.stdout,stderr=sys.stderr).wait()

		prev_title = last_title
		prev_link = os.path.basename(last_filename)
		last_title = chapname
		last_filename = os.path.join(published_dir,chapfname)
		last_file = open(last_filename,'w',encoding='utf-8')
		with open(os.path.join(path,fname),'r',encoding='utf-8') as mdfile:
			mdcontent = mdfile.read()
			if mdcontent[0] == u'\uFEFF': mdcontent = mdcontent[1:]
			last_content = markdown(mdcontent)

				
			
last_file.write(template%{
	'title' : last_title,
	'body'  : last_content,
	'nexttext' : "END",
	'nextlink' : "#",
	'prevtext' : prev_title,
	'prevlink' : prev_link
	}
)
last_file.close()
subprocess.Popen('git add %s'%last_filename,shell=True,stdin=sys.stdin,stdout=sys.stdout,stderr=sys.stderr).wait()
			
