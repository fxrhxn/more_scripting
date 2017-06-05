import subprocess
import os


cmd = 'sudo gem install listen'
def install_ruby(command):
	try:
		##Check ruby version
		#ruby_version =
		os.system(command)

		## Read the command line, and if there is some error, your will do something.

		# TODO - Find out how to read the command line.

	except:
		print('Some Error')



# def run_command(cmd):
# 	p = subprocess.Popen(cmd,
# 						 stdout=subprocess.PIPE,
# 						 stderr=subprocess.STDOUT)
# 	return iter(p.stdout.readline, b'')
#
#
# command = 'npm install express'.split()
#
#
# ruby_error = 'ERROR:'
#
# try:
# 	for line in run_command(command):
#
# 		# Split the error array.
# 		# error_array = line.split()
# 		#
# 		#
# 		# if(error_array[0] == ruby_error):
# 		# 	print('Error')
# 		print('Installed Ruby Gem')
#
# except:
# 	print('Error!')

## Function that installs homebrew.
def install_brew():
	os.system('ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')

# Make sure home brew is installed.
def check_brew():
	brew_read = os.popen('brew -v').read()

	brew_version = brew_read.split()[1].split('.')

	brew_major = brew_version[0]

	if(brew_major.isdigit()):
		return
	else:
		install_brew()

# Function that updates ruby.
def update_ruby():
	os.system('brew install ruby')

## Function that checks version of ruby.
def check_ruby():

	## Get the current version of Ruby.
	reading = os.popen('ruby -v').read()
	version = reading.split()[1][:5]

	version_splitting = version.split('.');

	major_version = int(version_splitting[0]);
	minor_version = int(version_splitting[1]);

	if(major_version < 2):
		update_ruby()
	else:
		if(minor_version < 5):
			update_ruby()


def check_pip():
	reading = os.popen('pip -V').read()
	version = reading.split()[1].split('.')

	if(len(version) != 3):
		return False
	else:
		return True


def check_gem():
	reading = os.popen('gem -v').read()
	version = reading.split('.')

	if(len(version) != 3):
		return False
	else:
		return True

## 1) Install ruby's latest version.

## 2) Link the file to the computer.
print check_gem()

'''
Current Goals


	Ruby Plans
	----------
1) Install latest version of Ruby.

2) Integrate that function into your current script.

3) Run the script, and see what can be built.


	Brew Plans
	----------

1) Install homebrew if it doesen't exist.

'''
