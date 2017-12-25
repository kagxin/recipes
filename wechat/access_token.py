from wechatpy import WeChatClient
from wechatpy.session.memorystorage import MemoryStorage

appid = ''
secret = ''

class Singleton(type):
    def __init__(cls, name, bases, attrs):
        super(Singleton, cls).__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


# class decortor
def singleton(cls, *args, **kwargs):
    instance = {}

    def __singleton():
        if cls not in instance:
            instance[cls] = cls
        return instance[cls]

    return __singleton


@singleton
class Client(WeChatClient):

    def __init__(self, appid=appid, secret=secret, access_token=None,
                 session=None, timeout=None, auto_retry=True):
        super(WeChatClient, self).__init__(
            appid, access_token, session, timeout, auto_retry
        )
        self.appid = appid
        self.secret = secret


client = Client()
client1 = Client()

print(id(client))
print(id(client1))



print(str(client().access_token))
print(client().access_token)


access_token_memory = MemoryStorage()

c = WeChatClient(appid, secret, session=access_token_memory)
print(c.access_token)
print(c.access_token)


c = WeChatClient(appid, secret, session=access_token_memory)
print(c.access_token)
print(c.access_token)

## 在web应用中注意WeChatClient的session使用同一个存储对象，保证access_token_memory 按策略刷新。避免业务量较大应用access token获取次数超限
# 4300887784
# 4300887784
# 5_IXxqjJcVePWbniDrUfSppsISOKPaGo9dtxlgtZ73B9Tx4OWc1k1l-lkc-J7mJM1pOPIUTmS3vXp4CvkwMbYLRAn8PkoW6yIL1NHTjmLlkm2cqp4X3KIb6G319jIZHKgADAIQT
# 5_rj2TjX42W5oYG3iHUfSppsISOKPaGo9dtxlgtZ73B9Tx4OWc1k1l-lkc-J6FgfVPt-E2w1pf5ztKBSeCe5f8egQbfgjM9ebcmhi_WU13QtLQW4gXDFT2cngTY7gXFPgADANVF
# 5_o8mi5E0ezBQ1dx6uUfSppsISOKPaGo9dtxlgtZ73B9Tx4OWc1k1l-lkc-J5xGERFJ4q9n9cmRWC5BsRUsrkqzg3b_Vrp2DahjsOkVLLvBWBsI6hYmGQQJwwft5AQDHgADATGK
# 5_o8mi5E0ezBQ1dx6uUfSppsISOKPaGo9dtxlgtZ73B9Tx4OWc1k1l-lkc-J5xGERFJ4q9n9cmRWC5BsRUsrkqzg3b_Vrp2DahjsOkVLLvBWBsI6hYmGQQJwwft5AQDHgADATGK
# 5_o8mi5E0ezBQ1dx6uUfSppsISOKPaGo9dtxlgtZ73B9Tx4OWc1k1l-lkc-J5xGERFJ4q9n9cmRWC5BsRUsrkqzg3b_Vrp2DahjsOkVLLvBWBsI6hYmGQQJwwft5AQDHgADATGK
# 5_o8mi5E0ezBQ1dx6uUfSppsISOKPaGo9dtxlgtZ73B9Tx4OWc1k1l-lkc-J5xGERFJ4q9n9cmRWC5BsRUsrkqzg3b_Vrp2DahjsOkVLLvBWBsI6hYmGQQJwwft5AQDHgADATGK
