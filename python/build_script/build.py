#!/usr/bin/env python3

import os
import sys
import time
import compileall

if __name__ == '__main__':

    commands = []
    commands.append('ls')
    commands.append('rm *.pyc')
    commands.append('rm -rf dist')
    commands.append('rm -rf __pycache__')
    commands.append('ls')

    for c in commands:
        s = os.popen(c).read()
        time.sleep(0.5)
        print('> {}: \n{}'.format(c, s))
        
    
    compileall.compile_dir('.', force=True)
    
    commands = []
    commands.append("rename 's/\.cpython-34//' __pycache__/*")
    commands.append('mv __pycache__/ dist/')
    commands.append('rm dist/{}c'.format(__file__))
    
    for c in commands:
        s = os.popen(c).read()
        time.sleep(0.5)
        print('> {}: \n{}'.format(c, s))
        

    