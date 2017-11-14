#!/usr/bin/env python3
'''
State Pattern
1) keyboard in put 'a', switch to StateA
2) keyboard in put 'b', switch to StateB
3) Ctrl+C exit program
'''

class State(object):
    def __init__(self):
        pass
    def handle(self):
        pass

class StateA(State):
    def __init__(self):
        pass
    def handle(self, context):
        print('A') 
        s = input()
        if s == 'b':
            context.state = StateB()
        return

class StateB(State):
    def __init__(self):
        pass
    def handle(self, context):
        print('B') 
        s = input()
        if s == 'a':
            context.state = StateA()
        return
        
class Context(object):
    def __init__(self, state):
        self.state = state

    def operation(self):
        self.state.handle(self)

def main():
    init = StateA()
    c = Context(init)

    while True:
        c.operation()


if __name__ == '__main__':
	main()
