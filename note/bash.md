## BASH shell  
several shells:  
- sh: Bourne shell  
- csh: C shell  
- ksh:  
- tcsh:  
- bash: bourne Again SHell(GNU)  

how many shells can use: `/etc/shells`  
which user use which shell in default: `/etc/passwd`  

**`ctrl-u`**/`ctrl-k`: delete text in command line  
**`ctrl-w`**: delete current word
`ctrl-a`/`ctrl-e`: move curser to head/end  

`echo`: print the variable
`unset`: unset the variable

`env`: show the envirment variable(env var = global variable space)
- HOME: home directory
- SHELL: shell name
- HISTSIZE: history size
- MAIL: mailbox
- PATH: search path
- LANG: language, zh_TW.UTF-8, zh_TW.Big5
- RANDOM: random  

`set`: show all of the envirment viriable
- PS1
	- \d: date
	- \H, \h: hostname
	- \t, \T, \A, \@: time
	- \u: user
	- \v: version
	- \w: complete working directory
	- \$: hint charactor, # $

$: PID of current shell, ex: `echo $$`  

?: return code of last instruct, ex: `echo $?`  

`export`: private variable export to envirment variable  

`locale`: language variable, usage: `locale -a`, `locale`  
language file location: `/usr/lib/locale`  
configuration of whole system: `/etc/locale.conf`  

`read [-pt] var`: read from keyboard, and set to var  
```
-p: prompt  
-t: timeout
```

`declare [-aixr] var`: declare variable type, equal to `typeset`  
```
-a: array  
-l: integer  
-x: export  
-r: readonly  
```
`ulimit`: user limit, refer parameter in `man bash` and search ulimit  
`alias`/`unalias`: for example: `alias ll='ls -l'`  
`alias`: show all the alias setting  
`history`: view the old commands, notice: safety issue, record length: HISTSIZE  
when logout, will log to ~/.bash_history. if wanna force write, use `history -w`  
  
instruc excute sequence:  
1) absolute/related path to excute, like as: /bin/ls  
2) via alias, suck as `~/.bashrc`  
3) via bash build-in instruction  
4) via $PATH to search in system  
  
bash envirment configuration file:  
 - login shell: via tty1~tty6, need input password  
    - `/etc/profile`: whole system setting, do not modify it  
    - `~/.bash_profile` or `~/.bash_login` or `~/.profile`: personal setting here  
 - non-login shell: long via X-window  
    - **`~/.bashrc`**  
 - `~/.bash_history`: when login, bash will log back, and know previous input commands  
 - `~/.bash_logout`: when logout, u can add additional action here  


