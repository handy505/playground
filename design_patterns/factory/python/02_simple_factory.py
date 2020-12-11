'''
Simple Factory
'''

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


# Simple Factory
def create_machine(brand, id):
    if brand == 'Delta':
        return DeltaMachine(id)
    elif brand == 'Schneider':
        return SchneiderMachine(id)


def main():
    m1 = create_machine('Delta', 1)
    m2 = create_machine('Schneider', 2)

    print(m1)
    print(m2)


if __name__ == '__main__':
    main()

'''
$ python3 02.py
Delta-1
Schneider-2
'''
