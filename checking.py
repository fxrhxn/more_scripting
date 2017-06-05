#Makes sure we have the current versions of everything that we need to run

import subprocess
import sys
import os.path


#Not running this automatically right now, but on OS X, the first time, you may need to do this
#and then restart to raise the max file descriptors:
#echo 'kern.maxfiles=20480' | sudo tee -a /etc/sysctl.conf
#echo -e 'limit maxfiles 8192 20480\nlimit maxproc 1000 2000' | sudo tee -a /etc/launchd.conf
#echo 'ulimit -n 4096' | sudo tee -a /etc/profile


#backport of checkprocess to python 2.6
def check_output(*popenargs, **kwargs):
	r"""Run command with arguments and return its output as a byte string.

	Backported from Python 2.7 as it's implemented as pure python on stdlib.

	>>> check_output(['/usr/bin/python', '--version'])
	Python 2.6.2
	"""
	process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
	output, unused_err = process.communicate()
	retcode = process.poll()
	if retcode:
		cmd = kwargs.get("args")
		if cmd is None:
			cmd = popenargs[0]
		error = subprocess.CalledProcessError(retcode, cmd)
		error.output = output
		raise error
	return output
if not hasattr(subprocess, 'check_output'):
	subprocess.check_output = check_output




debug = True
if len(sys.argv) > 1:
	debug = sys.argv[1] == 'debug'

print(sys)

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

#ignores output, raises exception on return code
def run(cmd, fail_okay = False):
	print 'running ' + cmd
	try:
		subprocess.check_output(cmd, shell=True)
		return True
	except subprocess.CalledProcessError, e:
		print 'call failed.  output:'
		print e.output
		if fail_okay:
			return False
		else:
			raise e

#true if returns with a 0 exit code, false otherwise
def no_error(cmd):
	try:
		print 'checking ' + cmd
		subprocess.check_output(cmd, shell=True)
		return True
	except subprocess.CalledProcessError, e:
		return False

def sys_call(args,cwd=None, failokay=False, async=False, hide_output=False):
	print 'running ' + args
	process = subprocess.Popen(args, cwd=cwd, shell=True, stdout=(subprocess.PIPE if hide_output else None), stderr=subprocess.STDOUT)
	ret = process.poll() if async else process.wait()
	if ret is not None and ret != 0:
		if hide_output:
			print process.stdout.read()
		if failokay:
			print ('warning, call failed: ' + args)
		else:
			raise Exception('call failed: ' + args)
	return process

#Calls the given process and sends the given data to its stdin
def input_call(args, data):
	print 'running ' + args
	print 'sending data:\n' + data
	process = subprocess.Popen(args, cwd=None, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
	(stdoutdata, stderrdata) = process.communicate(data)
	print stdoutdata

#Runs the call async, and returns a function that blocks until it completes
def async_call(args):
	print 'starting ' + args
	process = subprocess.Popen(args, cwd=None, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	def wait():
		print 'waiting for ' + args + ' to complete'
		ret = process.wait()
		print process.stdout.read()
		if ret != 0:
			raise Exception('call failed: ' + args)
	return wait

_failed = False
#indicates a dependency was not met and could not be automatically satisfied
def fail(msg):
	global _failed
	_failed = True
	print msg


class Dependency:
	def name(self): return self._name

	def ensure(self):
		if not self.check():
			self.upgrade()

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
		if debug:
			return self.upgrade_debug()
		else:
			return self.upgrade_prod()

	def upgrade_debug(self): fail('Please install dependency: ' + self.name())

	def upgrade_prod(self): raise Exception('No upgrade routine defined')




class YumDependency(Dependency):
	def __init__(self, package):
		self.package = package
		self._name = 'yum package ' + self.package

	def check_debug(self): return True

	def check_prod(self):
		return no_error('yum list installed ' + self.package)

	def upgrade_prod(self):
		run('yum -y install ' + self.package)


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




#This is the list of dependencies we need.  We assume, in prod mode, that we are running on an AMI with:

#pip
#ruby 2.0
#a version of nodejs and npm (we auto-upgrade to the version we want if not installed)
#supervisord
#
#...and configured to pull the bubble code from git


if __name__ == '__main__':

	#
	#
	#Make sure we are on the correct node version
	NodeVersion('0.12.15').ensure()
	#
	# #need this to use native postgres bindings
	YumDependency('postgresql-devel').ensure()
	#
	# #Global node packages
	# GlobalNPM('coffee-script', '1.6.3').ensure()
	# GlobalNPM('node-inspector', '0.12.1').ensure()
	# GlobalNPM('shrinkpack', '0.13.1').ensure()
	#
	# #Install sass
	# GemDependency('rb-fsevent').ensure()
	# GemDependency('sass').ensure()

	#GemDependency('listen').ensure()

	# #Papertrail logging
	# remote = GemDependency('remote_syslog')
	# remote.remote_only = True
	# remote.ensure()

	# if not debug:
	#     #Configure papertrail
	#     papertrail_config = """
	# files:
	#   - /tmp/bubble-stderr*.log
	#   - /tmp/bubble-stdout*.log
	#   - /tmp/supervisord.log
	# destination:
	#   host: logs.papertrailapp.com
	#   port: 45539
	#     """
	#     input_call('cat > /home/ec2-user/papertrail_config.yml', papertrail_config)
	#
	#     sys_call('remote_syslog -c /home/ec2-user/papertrail_config.yml', failokay=True)
	#
	# #If we are not in debug mode, pre-compile all the JS
	# if not debug:
	#     #first, wipe the existing js...
	#     sys_call('rm `ls lib/*.coffee lib/*/*.coffee | sed s/\.coffee/.js/g`', failokay=True)
	#     #then compile the coffee script
	#     sys_call('coffee -c lib')
	#     sys_call('coffee -c bubble_private')
	#

	# if not debug:
	#     sys_call('npm prune')
	#     #npm is fragile for some reason, so we try it twice before giving up
	#     try:
	#         sys_call('npm install')
	#     except:
	#         sys_call('npm install')

	#compile browserify and sass
	# waiting_on = []
	# if not debug or not os.path.exists('lib/window.js'):
	#     waiting_on.append(async_call('sass --update sass:public/static/css'))


	# #Dependencies for our testing framework:
	# PipDependency('selenium', '2.35').ensure()
	# YumDependency('ImageMagick').ensure()
	#
	# PipDependency('iso8601').ensure()
	#

	# for w in waiting_on:
	#     w()
	#
	# if _failed:
	# 	raise Exception('One or more dependencies are not met... see output above')
