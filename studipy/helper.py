def safe_get(d, *keys):
    for key in keys:
        try:
            d = d.get(key)
            if d is None:
                return None
        except AttributeError:
            return None
    return d
