'''
Simple Factory Usage
1) create many machines
2) use for loop
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
    machines = []
    for id in range(1, 4):
        m = create_machine('Delta', id)
        machines.append(m)

    for id in range(4, 7):
        m = create_machine('Schneider', id)
        machines.append(m)

    for m in machines:
        print(m)


if __name__ == '__main__':
    main()

'''
$ python3 03.py
Delta-1
Delta-2
Delta-3
Schneider-4
Schneider-5
Schneider-6
'''
