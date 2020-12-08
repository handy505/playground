#!/usr/bin/env python3

class Machine(object):
    def __init__(self):
        self.val = 0

class DecorateMachine(Machine):
    pass

class ADecorateMachine(DecorateMachine):
    def __init__(self, origin):
        self.origin = origin 
    
    @property
    def val(self):
        v = self.origin.val
        return '~{}~'.format(v)
        
    @val.setter
    def val(self, arg):
        self.origin.val = arg

class BDecorateMachine(DecorateMachine):
    def __init__(self, origin):
        self.origin = origin 
    
    @property
    def val(self):
        v = self.origin.val
        return '#{}#'.format(v)
        
    @val.setter
    def val(self, arg):
        self.origin.val = arg

if __name__ == '__main__':
    m = Machine()
    m.val = 0
    print(m.val)
    m.val = 9
    print(m.val)

    m = ADecorateMachine(m)
    m.val = 0
    print(m.val)
    m.val = 9
    print(m.val)

    m = BDecorateMachine(m)
    m.val = 0
    print(m.val)
    m.val = 9
    print(m.val)

'''output 
0
9
~0~
~9~
#~0~#
#~9~# 
'''
    
