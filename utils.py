# -*- coding: utf-8 -*-

def make_column(row):
    c = []
    n = 0
    for r in row:
        n += 1
        c.append(r)
    return c


def sleep_ex(n):
    assert isinstance(n, (int, basestring)), repr(n)
    if isinstance(n, basestring):
        n, u = re.match(r'^(\d+)([smh])?$', n.lower()).groups()
        n = int(n) * {None: 1, 's': 1, 'm': 60, 'h': 3600}[u]
        time.sleep(n)

