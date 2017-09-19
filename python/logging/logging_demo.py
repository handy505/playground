#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import submod


logger = logging.getLogger()
#logging.basicConfig(filename='handy.log', level=logging.WARN)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

handler = logging.FileHandler('handy.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def main():


    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')

    submod.subfunc()

if __name__ == '__main__':
    main()


