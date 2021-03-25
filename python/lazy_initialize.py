import time

class LazyProperty:
    def __init__(self, method):
        self.method = method
        self.method_name = method.__name__

    def __get__(self, instance, cls):
        if not instance:
            return None
        value = self.method(instance)
        setattr(instance, self.method_name, value)
        return value



class Test:
    def __init__(self):
        self.x = 'foo'
        self.y = 'bar'
        #self._resource = None

    @LazyProperty
    def resource(self):
        print('execute resource method')
        #self._resource = 100
        #return self._resource
        time.sleep(1)
        return 100
    

if __name__ == '__main__':
    t = Test()
    print(t.x)
    print(t.y)
    print(t.resource)
    print(t.resource)
