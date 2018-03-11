### bottle request的生与死

这篇博文讨论，从客户端发起一个http请求，到bottle生成一个request对象的过程，以及request对象的实现。

先画一个请求http过程的简单时序图：
    


bottle是一个支持wsgi的框架。当客户端发起一个http请求时，http报文会先经过wsgi服务器处理成一个environ
字典，传给bottle的app来处理。调用的的的Bottle.__call__ --> Bottle.wsgi --> Bottle._handle
--> request.bind 初始化request对象
