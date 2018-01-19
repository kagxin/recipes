import asyncio
from inspect import getgeneratorstate

def simple_coro2(a):
    print('stated:a=', a)
    b = yield a
    print('received:b=', b)
    c = yield a + b
    print('received:c=', c)

my_coro2 = simple_coro2(5)
print(getgeneratorstate(my_coro2))
print(next(my_coro2))
print(getgeneratorstate(my_coro2))
print(my_coro2.send(28))
print(getgeneratorstate(my_coro2))
try:
    print(my_coro2.send(99))
except StopIteration:
    print(StopAsyncIteration)

print(getgeneratorstate(my_coro2))

print('-------------------------------------')


from functools import wraps

def coroutine(func):
    @wraps(func)

    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer


@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count



coro = averager()
print(coro.send(10))


class DemoException(Exception):
    """"""


def demo_finally():
    print('coroutine started.')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('*** DemoException handled. continuing...')
            else:
                print('received:{!r}'.format(x))
    finally:
        print('coro ending. and clean.')

if __name__ == '__main__':
    print('hello')