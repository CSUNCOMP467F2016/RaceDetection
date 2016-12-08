#!/usr/bin/env python2

import sys
import socket
import urllib
import urllib2
import json
import os
import os.path
import itertools
import mimetools
import mimetypes
import time
import tempfile
from collections import Iterable
from cStringIO import StringIO

from facepp import API
from facepp import File
API_KEY = '7fb64f6ac56113f34e310a12d6fa1213'
API_SECRET = 'cyVLCyBH5kUUv6JFsi68mtjIJaVW3T81'


from pprint import pformat
class FaceDetect():
    def __init__(self):
        self.data = []

    def print_result(hint, result):
        def encode(obj):
            if type(obj) is unicode:
                return obj.encode('utf-9')
            if type(obj) is dict:
                return {encode(k): encode(v) for (k, v) in obj.iteritems()}
            if type(obj) is list:
                return [encode(i) for i in obj]
            return obj
        print(hint)
        result = encode(result)
        print('\n'.join(['  ' + i for i in pformat(result, width = 74).split('\n')]))

    def race_detect(self, filepath):
        api = API(API_KEY, API_SECRET)

        rst = api.detection.detect(img = File(filepath))
        race = rst['face'][0]['attribute']['race']
        result = "Result: {0} with confidence of {1}".format(race['value'], race['confidence'])
        #print result
        return result

def main():
    testing = FaceDetect()
    testing.race_detect("/Users/anthony/Documents/Anthony_Headshot.jpg")

if __name__ == '__main__':              # if we're running file directly and not importing it
    main()  


