'''
Factory Method
'''

# -----------------------------------------------
# Framework Zone

from abc import ABCMeta, abstractmethod

class MachineFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_machine(self): pass

    @abstractmethod
    def create_packaging_material(self): pass


# -----------------------------------------------
# Application Zone, User added

class DeltaFactory(MachineFactory):
    def create_machine(self, id):
        # do something else for create machine.
        return DeltaMachine(id)

    def create_packaging_material(self):
        return DeltaPackagingMaterial()


class SchneiderFactory(MachineFactory):
    def create_machine(self, id):
        # do something else for create machine.
        return SchneiderMachine(id)

    def create_packaging_material(self):
        return SchneiderPackagingMaterial()

# -----------------------------------------------
class DeltaMachine(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'Delta-{}'.format(self.id)


class DeltaPackagingMaterial(object):
    def __str__(self):
        return 'DeltaPackagingMaterial'

# -----------------------------------------------
class SchneiderMachine(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return 'Schneider-{}'.format(self.id)


class SchneiderPackagingMaterial(object):
    def __str__(self):
        return 'SchneiderPackagingMaterial'




# -----------------------------------------------
def main():

    f = DeltaFactory()
    for id in range(1, 4):
        m = f.create_machine(id)
        p = f.create_packaging_material()
        print('create {} + {}'.format(m, p))


    f = SchneiderFactory()
    for id in range(4, 7):
        m = f.create_machine(id)
        p = f.create_packaging_material()
        print('create {} + {}'.format(m, p))



if __name__ == '__main__':
    main()


'''
$ python3 04_factory_method.py 
create Delta-1 + DeltaPackagingMaterial
create Delta-2 + DeltaPackagingMaterial
create Delta-3 + DeltaPackagingMaterial
create Schneider-4 + SchneiderPackagingMaterial
create Schneider-5 + SchneiderPackagingMaterial
create Schneider-6 + SchneiderPackagingMaterial

'''
