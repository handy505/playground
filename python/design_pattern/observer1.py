#!/usr/bin python3
# 觀察者模式
# ref: http://dongweiming.github.io/python-observer.html

'''
概念：
1) observer向subject註冊
2) subject資料更新時，notify所有已註冊的observers
3) 每個observer有自已的update()決定做何反應

優點：降低耦合
對每個subject來說，只關心自已的資料，並維護已註冊的observer清單、發通知，除此之外，沒什麼好在意的。。
對每個observer來說，只關心資料更新後，自已要做什麼應對，而無需在意資料何時更新。

常見命名方式：
subject - observer

subject
+attach
+detach
+notify

observer
+update

有了觀察者模式後，才發展出委託的做法。
說穿了就是observer的update()可以改名罷了。
'''

class Subject(object):
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._observers:
            observer.update(self)


class Data(Subject):
    def __init__(self, name=''):
        super(Data, self).__init__()
        self.name = name
        self._data = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.notify()



class HexViewer(object):
    def update(self, subject):
        #print 'HexViewer: Subject %s has data 0x%x' % (subject.name, subject.data)
        print ('HexViewer: Subject {} has data {}'.format(subject.name, hex(subject.data)))

class DecimalViewer(object):
    def update(self, subject):
        #print 'DecimalViewer: Subject %s has data %d' % (subject.name, subject.data)
        print('DecimalViewer: Subject {} has data {}'.format(subject.name, subject.data))
        

if __name__ == '__main__':

    data1 = Data('Data 1')
    data2 = Data('Data 2')
    view1 = DecimalViewer()
    view2 = HexViewer()
    data1.attach(view1)
    data1.attach(view2)
    data2.attach(view2)
    data2.attach(view1)

    print("Setting Data 1 = 10")
    data1.data = 10
    print("Setting Data 2 = 15")
    data2.data = 15
    print("Setting Data 1 = 3")
    data1.data = 3
    print("Setting Data 2 = 5")
    data2.data = 5
    print("Update data1's view2 Because view1 is be filtered")
    data1.detach(view2)
    data2.detach(view2)
    print("Setting Data 1 = 10")
    data1.data = 10
    print("Setting Data 2 = 15")
    data2.data = 15        
