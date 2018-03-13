DictProperty
cached_property
lazy_attribute
Bottle
HeaderProperty
_local_property
MultiDict
FormsDict
HeaderDict
auth_basic

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


