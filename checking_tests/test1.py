import os
import subprocess




## Find a way to check if the version exists.

#returns the output, ignores return code (unless ignore_fail is false)
def get_output(cmd, ignore_fail=True, no_verbose=False):
	try:
		if not no_verbose:
			print 'Checking ' + cmd
		return subprocess.check_output(cmd, shell=True)
	except subprocess.CalledProcessError, e:
		if ignore_fail:
			return e.output
		else:
			raise e

## Dependency class that does most of the heavy lifting. Currently we are only using the ensure function to make sure that we have the dependencies that are necessary.
class Dependency:
	def name(self):
		return self._name

	## MAIN FUNCTION USED - Checks if package is installed or not.
	def ensure(self):
		if self.check() == False:
			return { 'installed' : False, 'message' : self.name() + ' is not installed'}
		else:
			return { 'installed' : True, 'message' : self.name() + ' is already installed'}

	def check(self):
		return self.check_prod()

	def check_debug(self):
		raise Exception('No check routine defined for ' + self.name())

	def check_prod(self):
		return self.check_debug()

	def upgrade(self):
		return self.upgrade_debug()

	def upgrade_debug(self):
		print('')
		# fail('Installing dependency: ' + self.name())
		#print(self.name() + 'hahahaahhaha')


	def upgrade_prod(self): raise Exception('No upgrade routine defined')


## Make this None.
cached_pip_output = None

# Use this class to check for pip dependencies.
class PipDependency(Dependency):
	def __init__(self, package, version=None):
		self.package = package
		if version is not None:
			self.package += '==' + version
		self._name = 'pip install ' + self.package

	def check_debug(self):
		global cached_pip_output
		if cached_pip_output is None:
			cached_pip_output = get_output('pip freeze')

		return cached_pip_output.find(self.package) != -1

	def upgrade_prod(self): run(self._name)

## Class to check if a command exists.
class CmdExists(Dependency):
	def __init__(self, cmd, install, in_output = None):
		self._name = install
		self.cmd = cmd
		self.install = install
		self.in_output = in_output

	def check_debug(self):


		if self.in_output is not None:
			return get_output(self.cmd).find(self.in_output) != -1
		else:
			return no_error(self.cmd)

	def upgrade_prod(self):
		run(self.install)


## Use this class to check for NPM packages.
class GlobalNPM(CmdExists):
	def __init__(self, package, version):
		CmdExists.__init__(self, 'npm list -g --depth 1 ' + package, 'npm install -g ' + package + '@' + version, version)



# The main class that installs all of the Gems.
class GemDependency(Dependency):
	def __init__(self, gem):
		self.gem = gem
		self._name = 'ruby gem ' + self.gem

	def check_debug(self):
		cached_gem_output = get_output('gem list --local')
		return cached_gem_output.find(self.gem) != -1

	def upgrade_prod(self): run('gem install ' + self.gem)





## NPM commands we have to call.
npm_commands = [
	{'cmd' : 'sudo npm install -g coffee-script', 'v' : '1.6.3'},
	{'cmd' : 'sudo npm install -g node-inspector', 'v' : '0.12.1'},
	{'cmd' : 'sudo npm install -g shrinkpack', 'v' : '0.13.1'},
]

## Pip commands to install.
pip_commands = [
	{'package' : 'selenium', 'v' : '2.35'},
	{'package' : 'iso8601', 'v' : None}
]


# Gem commands to install.
gem_commands = [
	'listen',
	'sass',
	'rb-fsevent',
]

# Function that installs the packages.
def install_package(cmd, type):

	## Python packages.
	if(type == 'pip'):
		os.system(cmd)

	# NPM packages
	elif(type == 'npm'):
		os.system(cmd)

	# GEM packages.
	elif(type == 'gem'):
		os.system(cmd)

## This function checks if ruby is installed.
def ruby_check():

	## Get the current version of Ruby.
	reading = os.popen('ruby -v').read()

	# If the array count is 0, ruby does not exist.
	if(len(reading.split()) == 0):
		return False
	else:
		return True

# This function checks that brew is installed.
def brew_check():

	brew_read = os.popen('brew -v').read()

	# If the array count is 0, brew does not exist.
	if(len(brew_read.split()) == 0):
		return False
	else:
		return True


# Function checks that pip is installed.
def pip_check():
	reading = os.popen('pip -V').read()

	# If the array count is 0, pip does not exist.
	if(len(reading.split()) == 0):
		return False
	else:
		return True



# Function that checks if gem is installed.
def gem_check():
	reading = os.popen('gem -v').read()

	# If the array count is 0, gem does not exist.
	if(len(reading.split()) == 0):
		return False
	else:
		return True


## Next 4 functions are installing functions.

## Ruby is usually installed, here is the function anyways if it needs to be installed.
def install_ruby():
	## Install Ruby using homebrew.
	os.system('brew install ruby')

## Install pip.
def install_pip():
	## Link GBDM to use python with homebrew.
	os.system('brew link gbdm')
	## Install python using homebrew.
	os.system('brew install python')

## Gem is usually installed, but here is the function to install that shit.
def install_gem():
	print('Gem should be installed on all Macs.')

## Command to install homebrew, the legendary package manager.
def install_brew():
	os.system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')


# Get the current line of directories.
cwd = os.getcwd()

# Split the directories up.
directories_split = cwd.split('/');

# Get the name of the current directory.
current_directory = directories_split[len(directories_split) - 1]




#------------------------------
print('Setup Script STARTED')
#---------------------------------
################################################################################
'''

	First Step - Check for prerequisites(Gem / Ruby / Brew / Pip ) + See if user is in desktop.

'''
if(current_directory != 'Desktop'):
	print('ERROR - Please make sure you are in the "Desktop" directory.')
else:

	# Check ruby and see correct version.
	if(ruby_check() == False):
		install_ruby()
	else:
		print('ruby already installed.')

	## Check brew and find the correct version.
	if(brew_check() == False):
		install_brew()
	else:
		print('brew already installed.')

	## Check pip and install the same version.
	if(pip_check() == False):
		install_pip()
	else:
		print('pip already installed.')

	## Check gem and install the correct version.
	if(gem_check() == False):
		install_gem()
	else:
		print('gem already installed.')


################################################################################
	'''

		Second Step - Install Node, then NPM packages.

	'''
	# Loop through all of the commands and check them.
	for cmd in npm_commands:

		## Full command to install, and version.
		full_command = cmd['cmd'] + '@' + cmd['v']
		command = cmd['cmd']
		version = cmd['v']

		if(GlobalNPM(command, version).ensure()['installed']):
			print(command + ' already installed.')
		else:
			print('INSTALLING ' + command)
			install_package(full_command, 'npm')

################################################################################
	'''

		Third Step - Install Pip Commands

	'''

	## Loop through all of the pip commands.
	for cmd in pip_commands:

		# No version specified.
		if(cmd['v'] == None):

			#Check to see if dependency is installed.
			if(PipDependency(cmd['package']).ensure()['installed']):
				print(cmd['package'] + ' already installed.')
			else:
				install_package('pip install ' + cmd['package'], 'pip')

		# Version is given.
		else:

			#Check to see if dependency is installed.
			if(PipDependency(cmd['package'], cmd['v']).ensure()['installed']):
				print(cmd['package'] + ' already installed.')
			else:
				install_package('pip install ' + cmd['package'] + '==' + cmd['v'], 'pip')


################################################################################
	'''

		Fourth Step - Install Gem Packages

	'''

	# Loop through all of the gem commands in the array.
	for cmd in gem_commands:

		# Check if GemDependency is installed.
		if(GemDependency(cmd).ensure()['installed']):
			print('Already installed ' + cmd)
		else:
			print('Installing ' + cmd)

			# Command to install the gem dependency.
			command = 'sudo gem install ' + cmd

			# Function that actually does the installing.
			install_package(command, 'gem')


#------------------------------
	print('DEPENDENCIES INSTALLED - Now Downloading Bubble / Bubble Private')
#---------------------------------
################################################################################
	'''

		Fifth Step  - Download Bubble, and Bubble Private.

	'''




#------------------------------
	print('Setup Script ENDED')
#---------------------------------











#
