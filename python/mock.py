#!/usr/bin/env python3

from unittest.mock import MagicMock, Mock

def myfunc():
    import time
    time.sleep(1)
    return 'simulate communication time'

class Machine(object):
    def __init__(self):
        pass

    def communication(self):
        return 'access serial port, and get return from hardware'

if __name__ == '__main__':
    m = Machine()
    print(m.communication())

    m.communication = MagicMock(return_value='magicmock return')
    print(m.communication())

    mock = Mock()
    mock.return_value='mock return'
    m.communication = mock
    print(m.communication())
    
    mock2 = Mock(wraps=myfunc)
    m.communication = mock2
    print(m.communication())
    print(m.communication())
    print(m.communication())
    print(m.communication())
    print(m.communication())
    print(mock2.call_count)