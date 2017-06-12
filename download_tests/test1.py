import subprocess
import os

'''
1)
'''



## Repo urls to clone.
repo_urls = ['https://github.com/bubblegroup/bubble', 'https://github.com/jphaas/bubble_private']


## Test repo that is not private.
test_repo = 'https://github.com/fxrhxn/MacVMWare'

## Function to download repos
def download_repo(repo):

	## Clone "bubble_private" INSIDE of "bubble"
	if(repo == repo_urls[1]):
		print(repo)

	else:
		## Split the repo because subprocess requires the repos to be broken into a list. --> ['git', 'clone', 'repo']
		repo_split = ('git clone ' + repo).split()

		try:
			# Call the command that is split in the command line.
			subprocess.call(repo_split)
			print('Finished Cloning: ' + repo)
		except OSError:
			## Incase there's some error, catch that fucker.
			print('ERORR - Error while cloning ' + repo)


# Get the current line of directories.
cwd = os.getcwd()

# Split the directories up.
directories_split = cwd.split('/');

# Get the name of the current directory.
current_directory = directories_split[len(directories_split) - 1]


## Make sure the current directory is in desktop.
if(current_directory != 'Desktop'):
	print('ERROR - Please make sure you are in the "Desktop" directory.')
else:
	## For loop to split up the repo urls.
	for url in repo_urls:
		download_repo(url)
