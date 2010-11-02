commit: .DOITANYWAY
	git commit -a 
	git push origin master

new: .DOITANYWAY
	python scripts/newchapter.py

count: .DOITANYWAY
	python scripts/countwords.py

.DOITANYWAY:
