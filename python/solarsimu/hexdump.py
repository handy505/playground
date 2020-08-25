'''def hexdump(src, length=8):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
        result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    return b'\n'.join(result)
    '''

def hexdump(src, length=16):
    '''
    reference to http://code.activestate.com/recipes/142812-hex-dumper/
    modity python2 to python3
    '''
    result = []
    digits = 4 if isinstance(src, bytes) else 2
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = ' '.join(['{:>02X}'.format(x) for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
        line = '{:<04} {:<48s} {}'.format(i, hexa, text)
        result.append(line) 
    return '\n'.join(result)

if __name__ == '__main__':
    src = b'\x101234567890abcdefghijklmnopqrstuadsf;alsk\x10fjadsl;fjas;dlfkajd;fslkj'
    r = hexdump(src)
    print(r)
