'''
Basic
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



def main():
    m1 = DeltaMachine(1)
    m2 = SchneiderMachine(2)

    print(m1)
    print(m2)


if __name__ == '__main__':
    main()

