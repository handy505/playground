#!/usr/bin/env python3

MESSAGE = '''\
State Pattern
1) keyboard input 'a', switch to StateA
2) keyboard input 'b', switch to StateB
3) Ctrl+C exit program
'''

class State(object):
    def __init__(self): pass
    def handle(self): pass


class StateA(State):
    def __init__(self):
        pass
    def handle(self, context):
        print('StateA') 
        s = input()
        if s == 'b':
            context.state = StateB()
        return


class StateB(State):
    def __init__(self):
        pass
    def handle(self, context):
        print('StateB') 
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
    print(MESSAGE)

    init = StateA()
    c = Context(init)

    while True:
        c.operation()


if __name__ == '__main__':
	main()
