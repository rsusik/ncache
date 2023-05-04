# Nano cache

<p align="center">
<a href="https://pypi.org/project/ncache" target="_blank">
    <img src="https://img.shields.io/pypi/v/ncache?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://github.com/rsusik/ncache/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/rsusik/ncache" alt="Package version">
</a>
</p>

A simple and lightweight dictionary-based persistent cache for storing python objects.

## Installation:

```
pip install ncache
```

## Usage:

```python
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
    val = {'value'}
    cache.set_value(_hash, val)
    values += [val]
    print('Value added:', values)

cache.save_cache()
```
