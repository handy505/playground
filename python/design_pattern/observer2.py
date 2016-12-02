#!/usr/bin/env python3

class A(object):
    def __init__(self, name):
        self.name = name
        self.val = 0
        self.observers = []

    def __repr__(self):
        return '{}'.format(self.name)

    def attach(self, observer):
        self.observers.append(observer)

    def dettach(self, observer):
        self.observers.remove(observer)

    def notify_all(self):
        [o.update(self) for o in self.observers]

    def change(self):
        self.val += 1
        print('{} change my val = {}'.format(self.name, self.val))
        self.notify_all()


class B(object):
    def __init__(self, name):
        self.name = name

    def update(self, subject):
        print('{} update val = {} from {}'.format(self.name, subject.val, subject))


if __name__ == '__main__':
    a = A('machine')
    b1 = B('ui1')
    b2 = B('ui2')

    a.attach(b1)
    a.attach(b2)
    a.change()
    a.change()
    a.change()

