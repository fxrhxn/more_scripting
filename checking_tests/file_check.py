import os
import subprocess



## This function checks if ruby is installed.
def ruby_check():

	## Get the current version of Ruby.
	reading = os.popen('a -v').read()
	print(reading.split())

	if(len(reading.split()) == 0):
		return False
	else:
		return True


ruby_check()
