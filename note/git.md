
Configuration
--------------

`git config --global handy`  
`git config --global handy8831505@gmail.com`  
`git config --global core.autocrlf true`  
`git config --global core.safecrlf true`  
`git config --global color.ui true`  
`git config --global push.default simple`  
`git config --global alias.hist 'log --pretty=format:"%h %ad | %s%d [%an]" --graph --date=short'`  


Usually Instruction
--------------------
**`git config --list`**
`git init`  
`git add <filename>`  
`git rm --cached <filename>`
**`git status`**  
**`git commit -am "message"`** add to stash + commit  
`git commit --amend -m "message"` modify last commit message content  
`git reset HEAD^` reset back to last commit( one ^ indicate one last version)    
`git reset --hard HEAD^` reset back and delete last commit  
**`git log`**  
`git checkout <xxxx>` jump to xxxx version  
`git checkout master` the lastest version in master branch  
`git checkout <hash-code>` / `git checkout master` jump bwteen old/new version

stash
------
`git stash list`  
`git stash`  
`git stash pop`  
`git stash clear`  


branch
-------
`git branch` list branch  
`git branch <name>`  
`git merge <name>`  merge <name> into current branch
`git branch -m <old-name> <new-name>` rename branch  
`git branch -r <name>`  
`git branch -d <name>`  
`git branch -D <name>`  


remote
-------
**`git clone https://github.com/handy505/hello.git`**  
**`git remote show origin`** watch the sync statuc bwteen remote/locat  
**`git remote add origin https://github.com/handy505/hello.git`** add remote repo   
`git push -u origin master` 1st time push to remote repo(repo is empty)    
**`git push origin master`** push to remote    
`git pull https://github.com/handy505/hello.git` pull back(equal fetch+merge) from remote      

`$ git push origin serverfix` remote add a branch from local branch serverfix  
`$ git fetch origin`  
`$ git checkout -b serverfix origin/serverfix` local get a new remote branch  


### usually alias, edit .gitconfig in $HOME(NOT nessessary, it will cause the different operation experience
-------------------------------------------------------------------------------------------------------------
	[alias]
	  co = checkout
	  ci = commit
	  st = status
	  br = branch
	  hist = log --pretty=format:"%h %ad | %s%d [%an]" --graph --date=short
	  type = cat-file -t
	  dump = cat-file -p


tag
----
`git tag <tag-name>` add tag  
`git tag -d <tag-name>` delete tag  


github's upload(push) hint
---------------------------
	…or create a new repository on the command line

	echo # wificheck >> README.md
	git init
	git add README.md
	git commit -m "first commit"
	git remote add origin https://github.com/handy505/wificheck.git
	git push -u origin master
