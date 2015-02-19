# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 00:31:39 2015

@author: kerpowski
"""

import functools
import inspect

def debug_print(*x):
    if False:
        print(*x)

class Dispatcher(object):
    class dispatch_method(object):
        def __init__(self, method):
            debug_print('in dispatch method 2 init', self)
            functools.update_wrapper(self, method)
            self.method = method
            
        def __call__(self, func):
            debug_print('in dispatch method 2 call', func, func.__class__)   
            if(not hasattr(func, '_dispatch_handlers')):
                func._dispatch_handlers = set([])
            func._dispatch_handlers.add(self.method)
            return func
            
    def __init__(self, cls):
        debug_print('in dispatch init', self)
        self.cls = cls
        self.instance_map = {}
        functools.update_wrapper(self, cls)
        for n, x in inspect.getmembers(cls):
            if(hasattr(x, '_dispatch_handlers')):
                debug_print(x)
                for h in x._dispatch_handlers:
                    if h in self.instance_map:
                        raise Exception('multiple dispatchers declared for: ' + h)
                    self.instance_map[h] = x

        # JAKE: nested functions are painful... is there a cleaner way here?
        def dispatch_definition(c, line):
        # Here we 
        # 1) split the linput line
        # 2) find the appropriate dispatch method
        # 3) call that method and return it's response
            debug_print('dispatching')
            command = line.split()
            if len(command) == 0:
                if None in self.instance_map:
                    self.instance_map[None].__call__(self, [])       
            else:
                if command[0] in self.instance_map:
                    debug_print('found the method!')
                    return self.instance_map[command[0]](c, *command[1:])
                else:
                    debug_print('method not found, invoking default!')
                    if None in self.instance_map: 
                        return self.instance_map[None](c, *command[1:])
                    else:
                        raise Exception('No default handler found for ' + str(c.__class__))
            debug_print(self.instance_map)
                                        
        setattr(cls, 'dispatch', dispatch_definition)

    def __get__(self, obj, type=None):
        debug_print('in dispatch get', obj, type)            
    
    def __call__(self, type=None, *args, **kwargs):
        debug_print('in dispatch call', self.cls, args, kwargs)   
        instance = self.cls(*args, **kwargs)              
        return instance
