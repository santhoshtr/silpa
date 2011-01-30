# Copyright (c) 2006-2008 L. C. Rees
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#    
#    2. Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of Django nor the names of its contributors may be used
#       to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''RESTful WSGI URL dispatcher.'''

import re
import time
import copy
import sys
import random
import threading
from fnmatch import translate

__author__ = 'L.C. Rees (lcrees@gmail.com)'
__revision__ = '0.7'
__all__ = ['URLRelay', 'url', 'register']

def synchronized(func):
    '''Decorator to lock and unlock a method (Phillip J. Eby).

    @param func Method to decorate
    '''
    def wrapper(self, *__args, **__kw):
        self._lock.acquire()
        try:
            return func(self, *__args, **__kw)
        finally:
            self._lock.release()
    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper

def _handler(environ, start_response):
    start_response('404 Not Found', [('content-type', 'text/plain')])
    return ['Requested URL was not found on this server.']

def pattern_compile(pattern, pattern_type):
    '''Compile pattern.'''
    # Convert glob expression to regex
    if pattern_type == 'glob': pattern = translate(pattern)
    return re.compile(pattern)


class _Registry(object):

    '''Maintains order of URL preference while updating the central URL path
    registry.'''

    _register = list()

    def __iter__(self):
        '''Iterator for registry.'''
        return iter(self._register)   

    def add(self, pattern, mapping):
        '''Add tuple to registry.

        @param pattern URL pattern
        @param mapping WSGI application mapping
        '''        
        self._register.append((pattern, mapping))

    def get(self):
        '''Returns current registry.'''
        return tuple(self._register)


# URL registry
_reg = _Registry()

def register(pattern, application, method=None):
    '''Registers a pattern, application, and optional HTTP method.

    @param pattern URL pattern
    @param application WSGI application
    @param method HTTP method (default: None)
    '''
    if method is None:
        _reg.add(pattern, application)
    # Handle URL/method combinations
    else:
        # Update any existing registry entry
        for entry in _reg:
            if entry[0] == pattern:
                entry[1][method] = application
                return None
        # Add new registry entry
        _reg.add(pattern, {method:application})

def url(pattern, method=None):
    '''Decorator for registering a path pattern /application pair.

    @param pattern Regex pattern for path
    @param method HTTP method (default: None)
    '''
    def decorator(application):
        register(pattern, application, method)
        return application
    return decorator


class lazy(object):

    '''Lazily assign attributes on an instance upon first use.'''

    def __init__(self, method):
        self.method = method
        self.name = method.__name__

    def __get__(self, instance, cls):
        if instance is None: return self
        value = self.method(instance)
        setattr(instance, self.name, value)
        return value


class MemoryCache(object):

    '''Base Cache class.'''    
    
    def __init__(self, **kw):
        # Set timeout
        timeout = kw.get('timeout', 300)
        try:
            timeout = int(timeout)
        except (ValueError, TypeError):
            timeout = 300
        self.timeout = timeout
        # Get random seed
        random.seed()
        self._cache = dict()
        # Set max entries
        max_entries = kw.get('max_entries', 300)
        try:
            self._max_entries = int(max_entries)
        except (ValueError, TypeError):
            self._max_entries = 300
        # Set maximum number of items to cull if over max
        self._maxcull = kw.get('maxcull', 10)
        self._lock = threading.Condition()

    def __getitem__(self, key):
        '''Fetch a given key from the cache.'''
        return self.get(key)

    def __setitem__(self, key, value):
        '''Set a value in the cache. '''
        self.set(key, value)

    def __delitem__(self, key):
        '''Delete a key from the cache.'''
        self.delete(key) 

    def __contains__(self, key):
        '''Tell if a given key is in the cache.'''
        return self.get(key) is not None   

    def get(self, key, default=None):
        '''Fetch a given key from the cache.  If the key does not exist, return
        default, which itself defaults to None.

        @param key Keyword of item in cache.
        @param default Default value (default: None)
        '''
        values = self._cache.get(key)
        if values is None: 
            value = default
        elif values[0] < time.time():
            self.delete(key)
            value = default
        else:
            value = values[1]
        return copy.deepcopy(value)

    def set(self, key, value):
        '''Set a value in the cache.

        @param key Keyword of item in cache.
        @param value Value to be inserted in cache.
        '''
        # Cull timed out values if over max # of entries
        if len(self._cache) >= self._max_entries: self._cull()
        # Set value and timeout in cache
        self._cache[key] = (time.time() + self.timeout, value)

    def delete(self, key):
        '''Delete a key from the cache, failing silently.

        @param key Keyword of item in cache.
        '''
        try:
            del self._cache[key]
        except KeyError: 
            pass

    def keys(self):
        '''Returns a list of keys in the cache.'''
        return self._cache.keys()

    def _cull(self):
        '''Remove items in cache to make room.'''
        num, maxcull = 0, self._maxcull
        # Cull number of items allowed (set by self._maxcull)
        for key in self.keys():
            # Remove only maximum # of items allowed by maxcull
            if num <= maxcull:
                # Remove items if expired
                if self.get(key) is None: num += 1
            else: break
        # Remove any additional items up to max # of items allowed by maxcull
        while len(self.keys()) >= self._max_entries and num <= maxcull:
            # Cull remainder of allowed quota at random
            self.delete(random.choice(self.keys()))
            num += 1   


class URLRelay(object):

    '''Passes HTTP requests to a WSGI callable based on URL path component and
    HTTP request method.
    '''

    def __init__(self, **kw):
        # Values can be 'regex' or 'glob'
        pattern_type = kw.get('pattern_type', 'regex')
        # Add any iterable of pairs consisting of a path pattern and either a
        # callback name or a dictionary of HTTP method/callback names
        self._paths = tuple(
            (pattern_compile(u, pattern_type), v) 
            for u, v in kw.get('paths', _reg.get())
        )
        # Shortcut for full module search path
        self._modpath = kw.get('modpath', '')
        # 404 handler
        self._response = kw.get('handler', _handler)
        # Default function
        self._default = kw.get('default')
        # Set maximum number of items to cull from cache if over max
        self._maxcull = kw.get('maxcull', 10)
        # Set cache max entries
        self._max_entries = kw.get('max_entries', 300)
        # Set cache time out
        self._timeout = kw.get('timeout', 300)        

    def __call__(self, env, start_response):
        try:
            # Fetch app and any positional or keyword arguments in path
            app, arg, kw = self.resolve(env['PATH_INFO'], env['REQUEST_METHOD'])
            # Place args in environ dictionary
            env['wsgiorg.routing_args'] = (arg, kw)            
        except (ImportError, AttributeError):
            # Return 404 handler for any exceptions
            return self._response(env, start_response) 
        return app(env, start_response)
    
    @lazy
    def _cache(self):
        '''URL <-> callable mapping Cache.'''
        return MemoryCache(
            timeout=self._timeout, 
            maxcull=self._maxcull, 
            max_entries=self._max_entries,
        )

    def _getapp(self, app):
        '''Loads a callable based on its name
    
        @param app An WSGI application'''
        if isinstance(app, basestring):
            try:
                # Add shortcut to module if present
                dot = app.rindex('.')
                # Import module
                return getattr(__import__(app[:dot], '', '', ['']), app[dot+1:])
            # If nothing but module name, import the module
            except ValueError:
                return __import__(app, '', '', [''])
        return app        
    
  
    def _loadapp(self, app):
        '''Loads an application based on its name.

        @param app Web application name'''
        # Add module shortcut to module string
        if self._modpath != '' and isinstance(app, basestring):
            app = '.'.join([self._modpath, app])
        newapp = self._getapp(app)
        return newapp

    def resolve(self, path, method):
        '''Fetches a WSGI app based on URL path component and method.

        @param path URL path component
        @param method HTTP method
        '''
        key = ':'.join([path, method])
        # Try fetching app from cache
        app = self._cache.get(key)
        if app is not None: return app
        # Loop through path patterns -> applications
        for pattern, app in self._paths:
            # Test path for match
            search = pattern.search(path)
            # Continue with next iteration if no match
            if not search: continue
            # Get any app specifically linked to an HTTP method
            if isinstance(app, dict): 
                app = app.get(method)
                if app is None: continue             
            app = self._loadapp(app)
            # Ensure we have a callable
            assert hasattr(app, '__call__')
            # Extract any keyword arguments in the path
            kw = search.groupdict()
            # Extract any positional arguments
            args = tuple(i for i in search.groups() if i not in kw)
            # Cache app, positional and keyword arguments
            self._cache[key] = (app, args, kw)
            return app, args, kw
        # Return default app if no matching path and default app is set
        if self._default is not None:
            default = self._loadapp(self._default)
            return default, (), {}
        raise ImportError()
