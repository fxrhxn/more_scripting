
debug = True;

class Dependency:
	def name(self):
		return self._name

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

	def check_debug(self):
		raise Exception('No check routine defined for ' + self.name())

	def check_prod(self):
		return self.check_debug()

	def upgrade(self):
		return self.upgrade_debug()


	def upgrade_debug(self):

		#Function that installs the npm file.
		def install_npm(command):
			try:
				os.system(command)
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

		fail('Installing dependency: ' + self.name())

		# if(self.name() == 'Node version node@0.12.15'):
		# 	install_nodejs('Node version goes here. ')
		#
		# elif(self.name() == 'npm install -g coffee-script@1.6.3'):
		# 	install_npm(bubble_coffeescript_cmd)
		#
		# elif(self.name() == 'npm install -g node-inspector@0.12.1'):
		# 	install_npm(bubble_node_inspector_cmd)
		#
		# elif(self.name() == 'npm install -g shrinkpack@0.13.1'):
		# 	install_npm(bubble_shrkinkpack_cmd)
		#
		# elif(self.name() == 'ruby gem rb-fsevent'):
		# 	install_ruby(bubble_fsevent_cmd)
		#
		# elif(self.name() == 'ruby gem sass'):
		# 	install_ruby(bubble_sass_cmd)
		#
		# elif(self.name() == 'ruby gem listen'):
		# 	install_ruby(bubble_listen_cmd)
		#
		# elif(self.name() == 'ruby gem rb-fsevent'):
		# 	install_ruby(bubble_fsevent_cmd)
		#
		# elif(self.name() == 'pip install selenium==2.35'):
		# 	install_pip(bubble_selenium_cmd)
		#
		# elif(self.name() == 'pip install iso8601'):
		# 	install_pip(bubble_iso8601_cmd)
		#

	def upgrade_prod(self): raise Exception('No upgrade routine defined')


'''
// check_debug()

// check_prod()

// u

'''

def check_debug(self):
	raise Exception('No check routine defined for ' + self.name())

def check_prod(self):
	return self.check_debug()

def upgrade(self):
	return self.upgrade_debug()



def check(a):
	if debug:
		if hasattr(a, 'remote_only'):
			return True
		return a.check_debug()
	else:
		if hasattr(a, 'local_only'):
			return True
		return a.check_prod()


check('a')
###
