from routers import beta_mobile as bm


def test_catalog_cache_is_off_without_setting(monkeypatch):
    monkeypatch.delenv('CATALOG_CACHE_SECONDS', raising=False)
    bm._catalog_cache.clear()
    bm._cache_put(('p', 'k'), {'a': 1})
    assert bm._cache_get(('p', 'k')) is None


def test_catalog_cache_returns_copies_until_expiry(monkeypatch):
    monkeypatch.setenv('CATALOG_CACHE_SECONDS', '600')
    bm._catalog_cache.clear()
    clock = [100.0]
    monkeypatch.setattr(bm._time, 'monotonic', lambda: clock[0])
    stored = bm._cache_put(('p', 'k'), {'rows': [1]})
    first = bm._cache_get(('p', 'k'))
    first['rows'].append(2)  # a caller's change must not leak into the cache
    assert bm._cache_get(('p', 'k')) == {'rows': [1]} == stored
    clock[0] = 701.0
    assert bm._cache_get(('p', 'k')) is None
    bm._catalog_cache.clear()
