#!/usr/bin/env python

import os, sys
from datetime import datetime
import subprocess
import git

def shell_exec(command):
	return subprocess.Popen(command,shell=True,stdin=sys.stdin,stdout=sys.stdout,stderr=sys.stderr)

todayfolder = datetime.now().date().isoformat()

if not os.path.exists(todayfolder):
	os.mkdir(todayfolder, 0700)

files = os.listdir(todayfolder)
filenum = len(files) + 1
filename = os.path.join(os.getcwd(), todayfolder, "chapter_%02d.markdown"%filenum)

f = open(filename,"w")
f.write("# Chapter %s - %s\n"%(todayfolder, filenum))
f.close()

editor = os.environ.get('VISUAL', os.environ.get('EDITOR', None))
if editor:
	shell_exec("%s %s"%(editor, filename)).wait()
else:
	shell_exec('/usr/bin/env vi %s'%filename).wait()

shell_exec("git add %s"%filename)
shell_exec("make commit").wait()
