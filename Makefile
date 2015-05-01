

clean:
	rm -f */*.pyc */*.log */*~

dist:	clean
	tar -C ../ --exclude=".svn" -cvzf ../openEcslent.tgz openEcslent/

