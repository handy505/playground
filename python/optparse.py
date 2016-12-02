#!/usr/bin/env python3

import optparse

if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option("-m", "--minute",
        dest="minute",
        type="int",
        default=1,
        help="terminate after minutes, for debug[default=%default]")
    parser.add_option("-g", "--gui",
        dest="gui",
        type="string",
        default="tk",
        help="gui show/select [default=%default]")
    parser.add_option('-c', action='store_true', dest='consolemode',
        help='console mode')
    parser.add_option('-t', action='store_true', dest='testmode', 
        help='system test')
    opts, args = parser.parse_args()  
    print(opts)

