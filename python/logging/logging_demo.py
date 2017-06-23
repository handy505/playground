#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging

def main():
    logger = logging.getLogger('firstlogging')
    logging.basicConfig(level=logging.WARN)

    logger.debug('debug')
    logger.info('info')
    logger.warning('warn')
    logger.error('error')

if __name__ == '__main__':
    main()


