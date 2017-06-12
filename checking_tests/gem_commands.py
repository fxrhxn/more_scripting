import subprocess
import os



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



def install_package(cmd, type):
	print(cmd)

# Gem commands to install.
gem_commands = [
	'listen',
	'sass',
	'rb-fsevent',
]

for cmd in gem_commands:
	if(GemDependency(cmd).ensure()['installed']):
		print('Already installed ' + cmd)
	else:
		print('Installing ' + cmd)
		command = 'sudo gem install ' + cmd
		install_package(command, 'gem')
