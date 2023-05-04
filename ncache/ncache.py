import hashlib
import pickle
from pathlib import Path
from typing import Any
import os

__version__ = '0.3'

class Cache:
    def __init__(self, 
        filename:str, 
        nocache:bool=False, 
        tmpfilename:str=None # if None no temp file is created
    ):
        self.filename = filename
        if tmpfilename is None:
            tmpfilename = Path(filename).parent / f'~{Path(filename).name}.tmp'
        self.tmpfilename = tmpfilename
        self.nocache = nocache
        self.cache = {}

        def check_path(path:str):
            if Path(path).is_dir():
                raise Exception(f'Error: The path "{path}" is a difectory')
        for p in [self.filename, self.tmpfilename]:
            check_path(p)
        
    
    def if_cache_on(alt_exception=None, alt_value=None):
        def wrapper(fun):
            def inner(self, *args, **kwargs):
                if self.nocache == False:
                    return fun(self, *args, **kwargs)
                else:
                    if alt_exception is not None:
                        raise alt_exception
                    if alt_value is not None:
                        return alt_value
            return inner
        return wrapper

    def get_hash(self, obj:Any)->str:
        return hashlib.md5(pickle.dumps(obj)).hexdigest()

    def _get_cache_filename(self)->str:
        return self.filename

    @property
    def cache_filename(self)->str:
        return self._get_cache_filename()

    @if_cache_on()
    def load_cache(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.cache = pickle.load(f)
        else:
            print('Cache does not exists. Creating new one.')
            self.cache = {}
    
    @if_cache_on()
    def save_cache(self):
        with open(self.tmpfilename, 'wb') as f:
            pickle.dump(self.cache, f)
            os.rename(self.tmpfilename, self.filename)

    class NoCacheValue(Exception):
        pass

    @property
    def data(self)->dict:
        return self.cache

    @if_cache_on(alt_exception=NoCacheValue())
    def get_value(self, obj:Any)->Any:
        _hash = self.get_hash(obj)
        if _hash in self.cache.keys():
            val = self.cache[_hash]
            copy_fun = getattr(val, 'copy', None)
            if callable(copy_fun):
                result = copy_fun()
                return result
            else:
                return val
        else:
            raise self.NoCacheValue()

    @if_cache_on()
    def set_value(self, obj:Any, val:Any):
        _hash = self.get_hash(obj)
        copy_fun = getattr(val, 'copy', None)
        if callable(copy_fun):
            self.cache[_hash] = copy_fun()
        else:
            self.cache[_hash] = val