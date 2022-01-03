# proxy-scraper
Efficient and reliable proxy scraper, written in python.

## Filters
You can filter proxies based on three criterions:
- anonymity ('anonymous', 'elite proxy', 'transparent')
- https (True, False)
- country (Brazil, Kenya, France, ...)

## Methods:
- `loadProxies()` you must call this method after creating the object.
- `getAliveProxies()` sends back all the alive proxies. This method might take a while
- `getRandomAliveProxy()` will send you back one random alive proxy
