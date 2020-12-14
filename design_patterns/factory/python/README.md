# basic -> simple factory

    - factory function with args
    - client example:
        m1 = create_machine('Delta', 1)
        m2 = create_machine('Schneider', 2)


# simple factory -> factory method

    - replace function to class
    - replace adjust parameters to select factories
    - client example:
        f = DeltaFactory()
        #f = SchneiderFactory()
        m = f.create_machine(1)
        m = f.create_machine(2)
        m = f.create_machine(3)


# factory method to abstract factory
    
    - implement multiple class method for every product in every product group
    - abstract factory = polymorphism factory



