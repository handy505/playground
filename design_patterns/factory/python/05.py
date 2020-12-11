'''
Factory Method

Factory: create
Method: polymorphism
'''

# -----------------------------------------------
# Framework Zone

from abc import ABCMeta, abstractmethod

class MachineFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_machine(self): pass


# -----------------------------------------------
# Application Zone, User added

class DeltaMachine(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'Delta-{}'.format(self.id)


class SchneiderMachine(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'Schneider-{}'.format(self.id)


class DeltaFactory(MachineFactory):
    def create_machine(self, id):
        # do something else for create machine.
        return DeltaMachine(id)


class SchneiderFactory(MachineFactory):
    def create_machine(self, id):
        # do something else for create machine.
        return SchneiderMachine(id)


def main():

    f = DeltaFactory()

    machines = []
    for id in range(1, 4):
        m = f.create_machine(id)
        machines.append(m)

    for m in machines:
        print(m)

    print('----------- replace brand -----------')

    f = SchneiderFactory() # replace this to change brand

    machines = []
    for id in range(1, 4):
        m = f.create_machine(id)
        machines.append(m)

    for m in machines:
        print(m)


if __name__ == '__main__':
    main()


'''
$ python3 05.py 
Delta-1
Delta-2
Delta-3
----------- replace brand -----------
Schneider-1
Schneider-2
Schneider-3
'''
