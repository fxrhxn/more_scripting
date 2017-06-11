import subprocess
import os



import os
cwd = os.getcwd()

## Repo urls to clone.
repo_urls = ['https://github.com/bubblegroup/bubble', 'https://github.com/jphaas/bubble_private']



## Function to download repos
def download_repo(repo):

	## Split the repo because subprocess requires the repos to be broken into a list. --> ['git', 'clone', 'repo']
	repo_split = ('git clone ' + repo).split()

	try:
		# Call the command that is split in the command line.
		subprocess.call(repo_split)
		print('Finished Cloning: ' + repo)
	except OSError:
		## Incase there's some error, catch that fucker.
		print('ERORR - Error while cloning ' + repo)



# ## For loop to split up the repo urls.
# for url in repo_urls:
# 	download_repo(url)
#

directories_split = cwd.split('/');

current_directory = directories_split[len(directories_split) - 1]

print(current_directory)
