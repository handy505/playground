def func():
    return 'Hello'


def func2():
    result = func()
    result = '{} {}'.format('modified', result)
    return result
    

def null_decorator(func):
    return func


def modify_decorator(func):
    def wrapper():
        result = func()
        result = '{} {}'.format('modified', result)
        return result
    return wrapper


if __name__ == '__main__':

    # basic function execute return a value
    print( func() )

    # after func2 execute return a value
    print( func2() )

    # after decorator, return a function for execute
    print( null_decorator(func)() )

    # after decorator, return a function for execute
    print( modify_decorator(func)() )


'''
$ python3 demo1.py 
Hello
modified Hello
Hello
modified Hello

'''
