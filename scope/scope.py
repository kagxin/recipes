

def F():
    x = 0
    def G():
        nonlocal x
        x += 1
        return x
    return G

g = F()
print(g())
print(g())
print(g())


def F():
    x = 0
    def G():
        y = x
        return y
    return G

g = F()
print(g())
print(g())
print(g())

def F():
    x = {'x':0}
    def G():
        x['x'] += 1
        return x['x']
    return G

g = F()
print(g())
print(g())
print(g())


# 作用域的LEGB法则
# 相对最内层函数来说

gl = 0  # G(global)

def F():
    x = 0  # E(enclosing)
    def G():
        t = 1  # L(local)
        return t
    return G

g = F()
print(g())


__name__ # B (built-in)
__file__
