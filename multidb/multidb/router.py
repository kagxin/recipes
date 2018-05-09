
def counter():
    cnt = 0
    def add_one():
        nonlocal cnt
        cnt += 1
        return cnt
    return add_one


class DefaultRouter(object):
    def __init__(self):
        self.counter = counter()

    def db_for_read(self, model, **hints):
        cnt = self.counter()     # 如果存在多个从数据库，可以使用该闭包做一个简单的轮循等权路由
        print('read from slave. cnt:%d'%cnt)
        return 'slave'

    def db_for_write(self, model, **hints):
        print('write to defalut.')
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        return None
