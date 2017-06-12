import os
import subprocess


'''
Todo

1) Find out how Pip commands are checked. -


2) Do the loop of all of the pip commands.

'''

class Dependency:
	def name(self):
		return self._name

	def ensure(self):
		if self.check() == False:
			# self.upgrade()
			return { 'installed' : False, 'message' : self.name() + ' is not installed'}
		else:
			# print(self.name() + ' already installed.')
			return { 'installed' : True, 'message' : self.name() + ' is already installed'}

	def check(self):
		if hasattr(self, 'local_only'):
			return True
		return self.check_prod()

	def check_debug(self): raise Exception('No check routine defined for ' + self.name())

	def check_prod(self): return self.check_debug()

	def upgrade(self):
		return self.upgrade_debug()

	def upgrade_debug(self):
		print(self.name())
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


# Variable that is needed in the PipDependency class
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


## Pip commands to install.
pip_commands = [
	{'package' : 'selenium', 'v' : '2.35'},
	{'package' : 'iso8601', 'v' : None}
]


## Loop through all of the pip commands.
for cmd in pip_commands:
	# No version specified.
	if(cmd['v'] == None):

		#Check to see if dependency is installed.
		if(PipDependency(cmd['package']).ensure()['installed']):
			print(cmd['package'] + ' already installed.')
		else:
			print('Installing ' + cmd['package'])

	# Version is given.
	else:

		#Check to see if dependency is installed.
		if(PipDependency(cmd['package'], cmd['v']).ensure()['installed']):
			print(cmd['package'] + ' already installed.')
		else:
			print('Installing ' + cmd['package'])










####
