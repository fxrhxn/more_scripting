import subprocess
import os

#try:

# proc = subprocess.check_output(['brew', 'install', 'python'], stderr=subprocess.STDOUT)
#
# print proc
# # except subprocess.CalledProcessError:
# # 	print('HA')
#

try:
	x = os.system('brew install python')
except:
	os.system('brew link gdbm')
	x = os.system('brew install python')
