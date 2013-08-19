#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import os
import glob
import urllib
import urllib2
import binascii
import inspect
import zlib
import time

import msg_pb2

cwd = os.getcwd()
#sys.path.append('%s/protobuf-2.5.0/python' %(cwd, ))
#sys.path.append('%s/Protojson-master' %(cwd, ))

def dict_parser(*argv, **kwargs):
    """
    
    Arguments:
    - `*argv`:
    """
    msg = argv[0]
    obj = argv[1]
    name = argv[2]
    _t = kwargs.get('repeated', 0) and 'repeated' or 'required'
    if name and (_t != 'repeated'):
        msg = getattr(msg, name)
    ks = obj.keys()
    
    for idx, k in enumerate(ks):
        _par(msg, obj[k], k)

def list_parser(*argv, **kwargs):
    """
    
    Arguments:
    - `*argv`:
    """
    msg = argv[0]
    obj = argv[1]
    name = argv[2]
    if not obj:
        return
    _rp = kwargs.get('repeated', 0) and 'repeated' or 'required'
    if name:
        if _rp == 'repeated':
            name = '%s_node' % (name, )
    _m = getattr(msg, name)
    for o in obj:
        if isinstance(o, (dict, list)):
            _m = getattr(msg, name).add()
            _par(_m, o, name, repeated=1)
        else:
            _m.append(o)

def other_parser(*argv, **kwargs):
    """
    
    Arguments:
    - `*argv`:
    """
    msg = argv[0]
    obj = argv[1]
    name = argv[2].lower()
    if obj is None:
        obj = ''
    if name:
        setattr(msg, name, obj)
    else:
        msg = obj

def get_parser(obj):
    """
    
    Arguments:
    - `obj`:
    """
    _t = type(obj)
    _tn = 'other'
    if _t is dict:
        _tn = 'dict'
    elif _t is list:
        _tn = 'list'
    _f = '%s_parser' % (_tn, )
    _m = sys.modules[__name__]
    for _n, _func in  inspect.getmembers(_m):
        if _n == _f:
            return _func
    return None

def _par(*argv, **kwargs):
    """
    
    Arguments:
    - `obj`:
    """
    msg = argv[0]
    obj = argv[1]
    name = argv[2]
    _f = get_parser(obj)
    return _f(msg, obj, name, **kwargs)

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        _j= f.read()
        f.close()
        try:
            obj = json.loads(_j)
            m = msg_pb2.MSG()
            _par(m, obj, '')
            _m = m.SerializeToString()
            m1 = msg_pb2.MSG()
            js = time.clock()
            map(lambda x: json.loads(_j), range(1000))
            es = time.clock()
            json_cost = es-js
            js = time.clock()
            map(lambda x: m1.ParseFromString(_m), range(1000))
            es = time.clock()
            pb_cost = es-js
            print len(_j), \
                  len(zlib.compress(_j)), \
                  '%.4f' % json_cost, \
                  len(_m), \
                  len(zlib.compress(_m)), \
                  '%.4f' %  pb_cost
        except Exception, e:
            pass

