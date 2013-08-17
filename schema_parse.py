#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import inspect

def dict_parser(*argv, **kwargs):
    """
    
    Arguments:
    - `*argv`:
    """
    obj = argv[0]
    name = argv[1].upper()
    vname = argv[1].lower()
    _idx = argv[2]
    ks = obj.keys()

    _t = kwargs.get('repeated', 0) and 'repeated' or 'optional'
    sons = ['message %s {' % (name, )]
    for idx, k in enumerate(ks):
        sons.append(_par(obj[k], k, idx+1))
    sons.append('}')
    if _idx:
        sons.append('%s %s %s = %d;' % (_t, name, vname, _idx))
    return '\n'.join(sons)

def list_parser(*argv, **kwargs):
    """
    
    Arguments:
    - `*argv`:
    """
    obj = argv[0]
    name = argv[1].upper()
    vname = argv[1].lower()
    _idx = argv[2]
    _rp = kwargs.get('repeated', 0) and 'repeated' or 'optional'
    if len(obj) < 1:
        return 'optional int32 %s = %d;' % (name, _idx)
    else:
        if _rp == 'repeated':
            rst = _par(obj[0], name+'_node', 1, repeated=1)
            return 'message ' + name + '{\n' + rst + '}\n repeated ' + name + ' ' + vname + ' = %d;' % _idx
        else:
            r = _par(obj[0], name, _idx, repeated=1)
            return r

def other_parser(*argv, **kwargs):
    """
    
    Arguments:
    - `*argv`:
    """
    obj = argv[0]
    name = argv[1].lower()
    idx = argv[2]
    _tp = kwargs.get('repeated', 0) and 'repeated' or 'required'
    _tp = kwargs.get('repeated', 0) and 'repeated' or 'optional'
    if isinstance(obj, (int, long)):
        _t = 'int32'
    elif isinstance(obj, float):
        _t = 'float'
    else:
        _t = 'string'
    return '%s %s %s = %d;' % (_tp, _t, name, idx)


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
    obj = argv[0]
    name = argv[1]
    idx = argv[2]
    _f = get_parser(obj)
    return _f(obj, name, idx, **kwargs)
    

if __name__ == '__main__':
    _c = ''
    with open(sys.argv[1], 'r') as f:
        _c = f.read()
        f.close()
    obj = json.loads(_c)
    obk = {'a': 'ba',
           'b': [1, 2, 3],
           'c': {"a1": 1},
           'd': [[{'a': 1}]],
           'e': [{'e1': 'e2'}]}
    print _par(obj, 'Msg', 0)
