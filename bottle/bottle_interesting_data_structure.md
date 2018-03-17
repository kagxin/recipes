## Bottle中几个有趣的类结构

#### DictPropery
这个类的作用是将类中返回类字典对象的方法，变成一个read_only可控的属性(描述符)。
```python
class Bottle(object):

    @DictProperty('environ', 'bottle.request.query', read_only=True)
    def query(self):
        """ The :attr:`query_string` parsed into a :class:`FormsDict`. These
            values are sometimes called "URL arguments" or "GET parameters", but
            not to be confused with "URL wildcards" as they are provided by the
            :class:`Router`. """
        get = self.environ['bottle.get'] = FormsDict()
        pairs = _parse_qsl(self.environ.get('QUERY_STRING', ''))
        for key, value in pairs:
            get[key] = value
        return get
    GET = query

class DictProperty(object):
    """ Property that maps to a key in a local dict-like attribute. """

    def __init__(self, attr, key=None, read_only=False):  # attr, key, read_only接收装饰器的三个位置参数
        self.attr, self.key, self.read_only = attr, key, read_only

    def __call__(self, func):  # func接收类方法request.query
        functools.update_wrapper(self, func, updated=[])
        self.getter, self.key = func, self.key or func.__name__
        return self

    def __get__(self, obj, cls):  # 当访问request.GET的时候，就会调用该方法, obj为当前对象，cls为当前类
        if obj is None: return self  # obj为None说明被装饰的方法作为类变量来访问(Bottle.query)，返回描述符自身
        key, storage = self.key, getattr(obj, self.attr) 
        if key not in storage: storage[key] = self.getter(obj)  # 如果bottle.request.query不在storage也就是不在request.environ中的时候，在request.environ中添加'bottle.request.query':request.query(self)， 即reqeuest.query(self)的返回值：GET参数的字典.
        return storage[key]

    def __set__(self, obj, value):  # 当request.GET被赋值时，调用__set__
        if self.read_only: raise AttributeError("Read-Only property.")  # raise read only
        getattr(obj, self.attr)[self.key] = value  # 在request.environ字典中添加一个'bottle.request.query':value。

    def __delete__(self, obj):  # 当该类方法被装饰的方法别删除是调用
        if self.read_only: raise AttributeError("Read-Only property.")
        del getattr(obj, self.attr)[self.key]  # 从request.environ字典中删除bottle.request.query
```

DictProperty这个类是一个装饰器，也是一个描述符。可以看出它实际上是在操作，它的托管实例request的environ字典，当第一次访问这个描述符的实例时，会把request.query(self)的结果放到environ这个字典里。之后多次访问request.GET时，不用重复计算直接在environ中拿到结果。

#### Bottle
```python
class Bottle(object):

    def __call__(self, environ, start_response):  # 因为bottle__call__方法就是wsgi的协议函数，所以Bottle()实例就作为了wsgi服务器的appliction函数
        """ Each instance of :class:'Bottle' is a WSGI application. """
        return self.wsgi(environ, start_response)

    def __enter__(self):  # return
        """ Use this application as default for all module-level shortcuts. """
        default_app.push(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        default_app.pop()
```
bottle实现了上下文管理器协议，所以你可以像下面这样写，上下文管理器中的这个端点'/hello'，不会受with块外的那个同名端点影响。当然这两个端点也不在一个Bottle实例上。。。。
```python

@route('/hello')
def greet(name):
    return HTTPResponse('hello2')

with Bottle() as b_app:
    @b_app.route('/hello')
    def hello():
        return HTTPResponse('hello')

    run(host='localhost', port='8888', debug=True, reloader=True)
```

#### MultiDict
这个类实现了一个，value使用list存储的字典 ，存储重复 key 值时候 values 会以 list 形式都保存起来，默认返回list中最后一个value
``` python
class MultiDict(DictMixin):
    """ This dict stores multiple values per key, but behaves exactly like a
        normal dict in that it returns only the newest value for any given key.
        There are special methods available to access the full list of values.
    """

    def __init__(self, *a, **k):
        self.dict = dict((k, [v]) for (k, v) in dict(*a, **k).items())

    def __delitem__(self, key):
        del self.dict[key]

    def __getitem__(self, key):
        return self.dict[key][-1]

    def __setitem__(self, key, value):
        self.append(key, value)

    def keys(self):
        return self.dict.keys()

    def get(self, key, default=None, index=-1, type=None):
        try:
            val = self.dict[key][index]
            return type(val) if type else val
        except Exception:
            pass
        return default

    def append(self, key, value):
        """ Add a new value to the list of values for this key. """
        self.dict.setdefault(key, []).append(value)

    def replace(self, key, value):
        """ Replace the list of values with a single value. """
        self.dict[key] = [value]

    def getall(self, key):
        """ Return a (possibly empty) list of values for a key. """
        return self.dict.get(key) or []

    #: Aliases for WTForms to mimic other multi-dict APIs (Django)
    getone = get
    getlist = getall
```
可以探查一下 MultiDict生成对象的update 和 pop方法的行为：
``` python
In [69]: dm = MultiDict()
In [70]: dm['a'] = 1
In [71]: dm['a'] = 2
In [72]: dm.getlist('a')
Out[72]: [1, 2]
In [73]: dm.update({'a':3})
In [74]: dm.getlist('a')
Out[74]: [1, 2, 3]
In [75]: dm.pop('a')
Out[75]: 3
In [76]: dm['a']
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
<ipython-input-76-54e5ceebc4de> in <module>()
----> 1 dm['a']
e:\py3env\lib\site-packages\bottle-0.13.dev0-py3.6.egg\bottle.py in __getitem__(self, key)
   2093
   2094     def __getitem__(self, key):
-> 2095         return self.dict[key][-1]
   2096
   2097     def __setitem__(self, key, value):
KeyError: 'a'
```
MultiDict没有重写update方法为什么，使用update方法给更新key'a'的时候，会默认将value加到value list里呢。因为update方法是的实现是通过操作dict[key]实现的。也就是使用了__getitem__, __setitem__, __delitem__方法。只要重新定制了这三个under方法，update就拥有现在的行为。可以定位到MutableMapping类中看一个update的实现。
FormsDict类继承了MultiDict所以有类似的行为。
HeaderDict类也继承了MulticDict，不过重写了__setitem__，__getitem__等方法，value还是以list的形式存储但只能有一个item。
```python
In [85]: hd = HeaderDict()
In [86]: hd['a']='b'
In [87]: hd['a']='c'
In [89]: hd.getall('a')
Out[89]: ['c']
```
HeaderDict的key在存取的时候使用str.title处理过，所以key是无关大小写的，同时对key中的'-'和'_'也做了等效处理,也就是request.headers.get('CONTENT-LENGTH')和request.headers.get('content_length')等效。
