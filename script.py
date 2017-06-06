import os
import sys
import subprocess


'''
Dependencies that need to be installed.

1) Node Version 0.12.15

2) npm install -g coffee-script@1.6.3

3) npm install -g node-inspector@0.12.1

4) npm install -g shrinkpack@0.13.1

5) ruby gem rb-fsevent

6) ruby gem sass

7) ruby gem listen

8) pip install selenium==2.35

9) pip install iso8601
'''

## Things needed for the correct node version.
bubble_node_version = 'node@0.12.15'
bubble_node_version_cmd = 'brew install ' + bubble_node_version
bubble_ruby_version = 'ruby gem '

## NPM packages
bubble_coffeescript = 'coffee-script@1.6.3'
bubble_coffeescript_cmd = 'npm install -g ' + bubble_coffeescript

bubble_node_inspector = 'node-inspector@0.12.1'
bubble_node_inspector_cmd = 'npm install -g ' + bubble_node_inspector

bubble_shrkinkpack = 'shrinkpack@0.13.1'
bubble_shrkinkpack_cmd = 'npm install -g ' + bubble_shrkinkpack

## Ruby Gems
bubble_fsevent = 'rb-fsevent'
bubble_fsevent_cmd = 'sudo gem install ' + bubble_fsevent

bubble_sass = 'sass'
bubble_sass_cmd = 'sudo gem install ' + bubble_sass

bubble_listen = 'listen'
bubble_listen_cmd = 'sudo gem install ' + bubble_listen


## Pip commands
bubble_selenium = 'selenium==2.35'
bubble_selenium_cmd = 'sudo -H pip install ' + bubble_selenium

bubble_iso8601 = 'iso8601'
bubble_iso8601_cmd = 'sudo -H pip install ' + bubble_iso8601


debug = True

_failed = False

def fail(msg):
	global _failed
	_failed = True
	print msg


#returns the output, ignores return code (unless ignore_fail is false)
def get_output(cmd, ignore_fail=True, no_verbose=False):
	try:
		if not no_verbose:
			print 'checking ' + cmd
		return subprocess.check_output(cmd, shell=True)
	except subprocess.CalledProcessError, e:
		if ignore_fail:
			return e.output
		else:
			raise e

## Checking the dependency.
class Dependency:
	def name(self): return self._name

	def ensure(self):
		if self.check() == False:
			self.upgrade()
		else:
			print('Correct node version installed.')

	def check(self):
		if debug:
			if hasattr(self, 'remote_only'):
				return True
			return self.check_debug()
		else:
			if hasattr(self, 'local_only'):
				return True
			return self.check_prod()

	def check_debug(self): raise Exception('No check routine defined for ' + self.name())

	def check_prod(self): return self.check_debug()

	def upgrade(self):

		return self.upgrade_debug()




	def upgrade_debug(self):

		#Function that installs the npm file.
		def install_npm(command):
			try:
				print(command)
			except:
				print('NPM installation failed. Trying one more time.')

		#Function that installs ruby dependencies.
		def install_ruby(command):
			try:
				os.system(command)

				## Read the command line, and if there is some error, your will do something.

				# TODO - Find out how to read the command line.

			except:
				print('Some Error')


		#Function that installs node.js
		def install_nodejs(command):
			print(command)

		def install_pip(command):
			os.system(command)

		# fail('Installing dependency: ' + self.name())
		if(self.name() == 'Node version node@0.12.15'):
			install_nodejs('Node version goes here. ')

		elif(self.name() == 'npm install -g coffee-script@1.6.3'):
			install_npm(bubble_coffeescript_cmd)

		elif(self.name() == 'npm install -g node-inspector@0.12.1'):
			install_npm(bubble_node_inspector_cmd)

		elif(self.name() == 'npm install -g shrinkpack@0.13.1'):
			install_npm(bubble_shrkinkpack_cmd)

		elif(self.name() == 'ruby gem rb-fsevent'):
			install_ruby(bubble_fsevent_cmd)

		elif(self.name() == 'ruby gem sass'):
			install_ruby(bubble_sass_cmd)

		elif(self.name() == 'ruby gem listen'):
			install_ruby(bubble_listen_cmd)

		elif(self.name() == 'ruby gem rb-fsevent'):
			print('HAHAHAHA')

		elif(self.name() == 'pip install selenium==2.35'):
			install_pip(bubble_selenium_cmd)

		elif(self.name() == 'pip install iso8601'):
			install_pip(bubble_iso8601_cmd)





	def upgrade_prod(self): raise Exception('No upgrade routine defined')

cached_gem_output = None

class GemDependency(Dependency):
	def __init__(self, gem):
		self.gem = gem
		self._name = 'ruby gem ' + self.gem

	def check_debug(self):
		global cached_gem_output
		if cached_gem_output is None:
			cached_gem_output = get_output('gem list --local')
		return cached_gem_output.find(self.gem) != -1

	def upgrade_prod(self): run('gem install ' + self.gem)


cached_pip_output = None

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

## Next 4 functions are checking functions.
def ruby_check():

	## Get the current version of Ruby.
	reading = os.popen('ruby -v').read()
	version = reading.split()[1][:5]

	version_splitting = version.split('.');

	major_version = int(version_splitting[0]);
	minor_version = int(version_splitting[1]);

	if(major_version < 2):
		return False
	else:
		if(minor_version < 4):
			return False


def brew_check():
	brew_read = os.popen('brew -v').read()

	brew_version = brew_read.split()[1].split('.')

	brew_major = brew_version[0]

	if(brew_major.isdigit()):
		return True
	else:
		return False

def pip_check():
	reading = os.popen('pip -V').read()
	version = reading.split()[1].split('.')

	if(len(version) != 3):
		return False
	else:
		return True



def gem_check():
	reading = os.popen('gem -v').read()
	version = reading.split('.')

	if(len(version) != 3):
		return False
	else:
		return True


## Next 4 functions are installing functions.

## Ruby is usually installed.
def install_ruby():
	print('Ruby installed.')

## Install pip.
def install_pip():
	try:
		os.system('brew install python')
	except:
		os.system('brew install python')


## Gem is usually installed.
def install_gem():
	print('Gem installed.')

## Command to install homebrew.
def install_brew():
	try:
		os.system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
	except:
		os.system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')




## Class to check the node version.
class NodeVersion(Dependency):
	def __init__(self, version):
		self.version = version
		self._name = 'Node version ' + version

	def check_debug(self):
		return get_output('node --version').find(self.version) != -1

	def upgrade_prod(self):
		CmdExists('n --help', 'npm install -g n').ensure()
		run('n ' + self.version)
		#Make sure we have a clean build of all our npm files
		run('npm prune')
		run('npm install')
		run('npm rebuild')

class YumDependency(Dependency):
	def __init__(self, package):
		self.package = package
		self._name = 'yum package ' + self.package

	def check_debug(self): return True

	def check_prod(self):
		return no_error('yum list installed ' + self.package)

	def upgrade_prod(self):
		run('yum -y install ' + self.package)


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

	def upgrade_prod(self): run(self.install)


class GlobalNPM(CmdExists):
	def __init__(self, package, version):
		CmdExists.__init__(self, 'npm list -g --depth 1 ' + package, 'npm install -g ' + package + '@' + version, version)




if __name__ == "__main__":

## Just set debug to True. Don't worry why.
	debug = True

# Check the correct version of Node / Ruby
	print('Script has started.')
	check_ruby = ruby_check()
	check_brew = brew_check()
	check_pip = pip_check()
	check_gem = gem_check()

	## Check ruby and see correct version.
	if(check_ruby == False):
		install_ruby()


	## Check brew and find the correct version.
	if(check_brew == False):
		install_brew()

	## Check pip and install the same version.
	if(check_pip == False):
		install_pip()

	## Check gem and install the correct version.
	if(check_gem == False):
		install_gem()


	NodeVersion(bubble_node_version).ensure()
# Check correct NPM packages.
	GlobalNPM('coffee-script', '1.6.3').ensure()
	GlobalNPM('node-inspector', '0.12.1').ensure()
	GlobalNPM('shrinkpack', '0.13.1').ensure()
	GemDependency('rb-fsevent').ensure()
	GemDependency('sass').ensure()
	GemDependency('listen').ensure()

# #Dependencies for our testing framework:
	PipDependency('selenium', '2.35').ensure()
	PipDependency('iso8601').ensure()

	YumDependency('ImageMagick').ensure()

'''
Part 2 -  Create Bubble project, and Bubble test
'''






# checking node --version
# Please install dependency: Node version 0.12.15
# checking npm list -g --depth 1 coffee-script
# Please install dependency: npm install -g coffee-script@1.6.3
# checking npm list -g --depth 1 node-inspector
# npm ERR! code 1
# Please install dependency: npm install -g node-inspector@0.12.1
# checking npm list -g --depth 1 shrinkpack
# npm ERR! code 1
# Please install dependency: npm install -g shrinkpack@0.13.1
# checking gem list --local
# Please install dependency: ruby gem rb-fsevent
# Please install dependency: ruby gem sass
# Please install dependency: ruby gem listen
# starting sass --update sass:public/static/css
# checking pip freeze
# Please install dependency: pip install selenium==2.35
# Please install dependency: pip install iso8601
