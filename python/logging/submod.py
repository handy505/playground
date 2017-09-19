
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging

logger = logging.getLogger()

def subfunc():
    print('excute subfunc, {}'.format(__name__))
    logger.info('aaabbbccc')
