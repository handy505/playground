### operation
Ctrl-f/Ctrl-b : forward page/backward page  
0 : head of line   
^ : first word of line  
$ : tail of line  
w/b: next/back word    
gg/G : file head/tail  
u : undo  
{}: prev/next section  

**jump between vim/shell for excute instruction. ex: compile code.**  
Ctrl-z / fg  
:sh / exit  
:! command  

Ctrl-v : **view mode to select characters**  
y : copy(yank)  
c : cut  
p : past  

dd : delete line  
dw : delete word  
d$ : delete to line tail  
d0 : delete to line head  
d^ : delete to line first-word  

**line alignment**  
:ce : center  
:le : left  
:ri : right  

### install  
`sudo apt-get install vim`  
`sudo apt-get install ctags`  
`sudo apt-get install cscope`  


### vim configuration:  
- global: ``/etc/vim/vimrc
- private: ``~/.vimrc``


### split window(build in)
`ctrl-W + s` / `ctrl-W + v`: split window  
`ctrl-W + [hjkl]`: move cursor between window  


### tab page(like chrome browser)  
	:tabedit {file}   edit specified file in a new tab
	:tabfind {file}   open a new tab with filename given, searching the 'path' to find it
	:tabclose         close current tab

	gt            go to next tab
	gT            go to previous tab
	Ctrl-PgDn     go to next tab
	Ctrl-PgUp     go to previous tab

### edit in binary mode
`:%! xxd` / `:%! xxd -r`  


### ctags  
`sudo apt-get install ctags`
`ctags -R *`  
`ctrl-]` & `ctrl-o`  


### taglist  
add `Bundle 'taglist.vim'` into `~/.vimrc`  
in vim, `:BundleInstall` to install plugin  
in vim, `:Tlist`  
`ctrl+ww`: switch windows  


### cscope
```
sudo apt-get install cscope
mkdir -p ~/.vim/plugin
cd -p ~/.vim/plugin
wget http://cscope.sourceforge.net/cscope_maps.vim
```
usage: `cd PROJECT` +  `cscope -bR`  

### The-NERD-tree
add `Plugin 'The-NERD-tree'` in `~/.vimrc`  
usage: `:NERDTree`  


### SnipMate
add below in `~/.vimrc`  
-`Plugin 'MarcWeber/vim-addon-mw-utils'`
-`Plugin 'tomtom/tlib_vim'`
-`Plugin 'garbas/vim-snipmate'`
-`Plugin 'honza/vim-snippets'`
usage: ex: main + `tab` in main.c



# atom
## install Atom in ubuntu(32bit + 64bit) via PPA
```
sudo add-apt-repository ppa:webupd8team/atom
sudo apt-get update
sudo apt-get install atom
```
open markdown panel: `ctrl-shift-m`  

# notepadqq
## like notepad++
keyword: notepadqq raspberry pi  
refer to:  
https://www.linuxbabe.com/desktop-linux/compile-notepadqq-debian-ubuntu-raspbian  
