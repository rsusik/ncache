# Nano cache

A simple and lightweight dictionary-based persistent cache for storing large objects.

Install:
```
pip install ncache
```

Usage:

```
from ncache import Cache

cache = Cache('my.cache')
cache.load_cache()

values = []
try:
    _hash = cache.get_hash('key') 
    val = cache.get_value(_hash)  # raise NoCacheValue exception if not found
    values += [val]
    print('Value got from cache:', values)
except:
    # if not in cache then add it
    cache.set_value(_hash, val)
    values += [val]
    print('Value added:', values)
```
