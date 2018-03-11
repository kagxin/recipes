### python web框架autoreload原理（以bottle为例）

在使用django，bottle等web框架开发应用的时候，在修改代码之后不需要手动重启开发服务器，给开发者提供了很大的便利。这种机制是如何实现的呢，这篇博文就讨论一下这个问题。

这两天在看bottle的时候，发现它也有代码auto reload的功能，就到它的源码中看了一下。

当设置reloader=True的时候，主进程不会启动bottle服务，而是使用与主进程启动时相同的命令行参数创建一个新的子进程。然后主进程不断忙等待子进程结束，拿到子进程的return code，如果子进程返回的code为3，则重新以相同的命令行参数重新启动子进程，之前的代码的改动就被重新reload了。在子进程中，主线程在跑bottle的服务，另外一个线程在不断的check所有import的module文件是否修改（check原理之后会在代码中看到），如果检测到文件的改动，check线程会发送一个KeyboardInterrupt exception到主线程，kill掉bottle的服务，然后子进程以returncode=3退出。

在bottle源码中，autoreload功能主要涉及两个地方一个是run函数，另外一个是FileCheckerThread类。

先看一下run函数部分的代码片段（reloader部分带注释的bottle源码 ：https://github.com/kagxin/recipes/blob/master/bottle/bottle.py）。
reloader 为True是开启autoreload功能
```python
    if reloader and not os.environ.get('BOTTLE_CHILD'):  # reloader 为True，且环境变量中的BOTTLE_CHILD没有设置的时候，执行reloader创建新的子进程的逻辑
        import subprocess
        lockfile = None
        try:
            fd, lockfile = tempfile.mkstemp(prefix='bottle.', suffix='.lock')  # 临时文件是唯一的
            os.close(fd)  # We only need this file to exist. We never write to it
            while os.path.exists(lockfile):
                args = [sys.executable] + sys.argv  # 拿到完整的命令行参数
                environ = os.environ.copy()
                environ['BOTTLE_CHILD'] = 'true'
                environ['BOTTLE_LOCKFILE'] = lockfile  # 设置两个环境变量
                print(args, lockfile)
                p = subprocess.Popen(args, env=environ)  # 子进程的环境变量中，BOTTLE_CHILD设置为true字符串，这子进程不会再进入if reloader and not os.environ.get('BOTTLE_CHILD') 这个分支，而是执行之后分支开启bottle服务器
                while p.poll() is None:  # Busy wait...  等待运行bottle服务的子进程结束
                    os.utime(lockfile, None)  # I am alive!  更新lockfile文件，的access time 和 modify time
                    time.sleep(interval)
                if p.poll() != 3:
                    if os.path.exists(lockfile): os.unlink(lockfile)
                    sys.exit(p.poll())
        except KeyboardInterrupt:
            pass
        finally:
            if os.path.exists(lockfile):  # 清楚lockfile
                os.unlink(lockfile)
        return
    ...
    ...
```
    代码分析：

        程序执行，当reloader为True而且环境变量中没有BOTTLE_CHILD的时候，执行之后逻辑，BOTTLE_CHILD这个环境变量是用来的在Popen使用命令行参数启动子进程的时候，让启动的子进程不要进入当前分支，而是直接执行之后启动bottle服务的逻辑。
        先不要关注lockfile文件，它的主要作用是让子进程通过判断它的modify time是否更新，来判断主进程是否依然存活。while p.poll() is None:... 这段代码是在忙等待子进程结束，同时使用os.utime不断更新lockfile的aceess time和modify time。如果returncode==3说明子进程因文件修改而结束，则在当前循环中通过popen使用相同的命令行重新启动子进程。
``` python
    if reloader:
        lockfile = os.environ.get('BOTTLE_LOCKFILE')
        bgcheck = FileCheckerThread(lockfile, interval)  # 在当前进程中，创建用于check文件改变的线程
        with bgcheck:  # FileCheckerThread 实现了，上下文管理器协议, 
            server.run(app)
        if bgcheck.status == 'reload':  # 监控的module文件发生改变，以returncode=3退出子进程，父进程会拿到这个returncode重新启动一个子进程，即bottle服务进程
            sys.exit(3)
    else:
        server.run(app)
```
    代码分析：
        这个是子进程中的主体部分，在bgcheck这上下文管理器中，运行bottle服务，server.run(app)是阻塞的直到收到主线程结束信号。在这个上下文管理器中，运行着一个check文件改动的线程。如果文件改动就会向当前主线程发送KeyboardInterrupt终止server.run(app)。上下文管理器退出时会忽略这个KeyboardInterrupt异常，然后以returncode==3退出子进程。
``` python
class FileCheckerThread(threading.Thread):
    """ Interrupt main-thread as soon as a changed module file is detected,
        the lockfile gets deleted or gets too old. """

    def __init__(self, lockfile, interval):
        threading.Thread.__init__(self)
        self.daemon = True
        self.lockfile, self.interval = lockfile, interval
        #: Is one of 'reload', 'error' or 'exit'
        self.status = None

    def run(self):
        exists = os.path.exists
        mtime = lambda p: os.stat(p).st_mtime
        files = dict()

        for module in list(sys.modules.values()):
            path = getattr(module, '__file__', '')
            if path[-4:] in ('.pyo', '.pyc'): path = path[:-1]
            if path and exists(path): files[path] = mtime(path)  # 拿到所有导入模块文件的modify time

        while not self.status:
            if not exists(self.lockfile)\
            or mtime(self.lockfile) < time.time() - self.interval - 5:
                self.status = 'error'
                thread.interrupt_main()
            for path, lmtime in list(files.items()):
                if not exists(path) or mtime(path) > lmtime:  # 如果文件发生改动，
                    self.status = 'reload'
                    thread.interrupt_main()  # raise 一个 KeyboardInterrupt exception in 主线程
                    break 
            time.sleep(self.interval)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, *_):
        if not self.status: self.status = 'exit'  # silent exit
        self.join()
        return exc_type is not None and issubclass(exc_type, KeyboardInterrupt)
```
    代码分析：
        这个类有__enter__和__exit__这两个dunder方法，实现了上下文管理器协议。在进入这个上下文管理器的时候，启动这个线程，退出时等待线程结束，且忽略了KeyboardInterrupt异常，因为__exit__返回True之外的值时，with中的异常才会向上冒泡。
        在run方法中在for module in list(sys.modules.values()):...这个for循环中拿到所有module文件的modify time。然后在之后的while循环中，监测文件改动，如果有改动调用thread.interrupt_main()，在主线程（bottle所在线程）中raise，KeyboardInterrupt异常。

上面就是整个bottle auto reload机制的代码。
reloader部分带注释的bottle源码 ：https://github.com/kagxin/recipes/blob/master/bottle/bottle.py
欢迎拍砖砖交流╭(╯^╰)╮