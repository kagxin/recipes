# coding:utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
'''
Created on 2017年11月30日

@author: ilinkin
'''
import abc
import base64
from wechatpy.messages import TextMessage, ImageMessage, UnknownMessage
from device_event import DeviceTextEvent
from wechatpy.utils import to_binary
import xmltodict
import requests, json
from wechatpy import parse_message
from wechatpy.replies import TextReply, DeviceTextReply
from wechatpy.fields import Base64DecodeField
import logging

logger = logging.getLogger('django.request')

# https://github.com/doraemonext/wechat-python-sdk
TULINGURL = 'http://www.tuling123.com/openapi/api'




class MessageHandle(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def msg_type(self):
        """ """

    @abc.abstractmethod
    def get_send_msg(self, message):
        """" """


class TextMessgeHandle(MessageHandle):
    @property
    def msg_type(self):
        return TextMessage

    def get_send_msg(self, message):
        content = message.content + 'hello slient.'
        json_data = {
            'key': '23bef26bd5424f2d80428a6c2cf2867b',
            'info': message.content,
            'loc': u'上海嘉定区',
            'userid': message.source,
        }
        r = requests.post(TULINGURL, data=json.dumps(json_data))
        try:
            data = r.json()
            context = data['text']
        except KeyError:
            context = content
        reply = TextReply(content=context, message=message)
        return reply.render()


class UnknownMessageHandle(MessageHandle):
    @property
    def msg_type(self):
        return UnknownMessage

    def get_send_msg(self, message):
        return 'sucess'


class ImageMessgeHandle(MessageHandle):
    @property
    def msg_type(self):
        return ImageMessage

    def get_send_msg(self, msg):
        """ """
        return 'success'


class DeviceTextHandle(MessageHandle):
    @property
    def msg_type(self):
        return DeviceTextEvent

    def response_data(self, to_user, form_user, device_type, device_id, session_id, content):
        """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%u</CreateTime>
        <MsgType><![CDATA[device_text]]></MsgType>
        <DeviceType><![CDATA[%s]]></DeviceType>
        <DeviceID><![CDATA[%s]]></DeviceID>
        <SessionID>%u</SessionID>
        <Content><![CDATA[%s]]></Content>
        </xml>""" % (to_user, form_user, device_type,)

    def get_send_msg(self, msg):
        print(type(msg))
        #         print(msg.device_type)
        print(msg.content)
        print(['%x'%ord(a) for a in msg.content])
        return 'sucess'


class MSGHandle(object):
    def __init__(self):
        self.handles = (TextMessgeHandle(), ImageMessgeHandle(), UnknownMessageHandle(), DeviceTextHandle())
        self.device_handle = DeviceTextHandle()

    def get_send_msg(self, msg):
        message = parse_message(msg)
        if isinstance(message, DeviceTextEvent):
            self.device_handle.get_send_msg(message)
        for handle in self.handles:
            if isinstance(message, handle.msg_type):
                return handle.get_send_msg(message)

        return 'success'


message_handle = MSGHandle()

msg_list = [
    # u""" <xml><ToUserName><![CDATA[gh_b2007557ae68]]></ToUserName>
    #     <FromUserName><![CDATA[oDvyGsw49dRMYZSntyIulfdIh93M]]></FromUserName>
    #     <CreateTime>1512114546</CreateTime>
    #     <MsgType><![CDATA[text]]></MsgType>
    #     <Content><![CDATA[破坏形容]]></Content>
    #     <MsgId>6494482523298371248</MsgId>
    #     </xml>
    # """,
    # u"""<xml><ToUserName><![CDATA[gh_b2007557ae68]]></ToUserName><FromUserName><![CDATA[oDvyGs1dQS3MO0UAfxvuE2_XmZMA]]></FromUserName><CreateTime>1513060984</CreateTime><MsgType><![CDATA[device_text]]></MsgType><DeviceType><![CDATA[gh_b2007557ae68]]></DeviceType><DeviceID><![CDATA[gh_b2007557ae68_73516d32233606d2]]></DeviceID><Content><![CDATA[mG25BL58CDYwMiBCQTA2QTAwMwg=]]></Content><SessionID>799257</SessionID><MsgID>24765017939</MsgID><OpenID><![CDATA[oDvyGs1dQS3MO0UAfxvuE2_XmZMA]]></OpenID></xml>""",
    # u"""<xml><ToUserName><![CDATA[gh_b2007557ae68]]></ToUserName><FromUserName><![CDATA[oDvyGs1dQS3MO0UAfxvuE2_XmZMA]]></FromUserName><CreateTime>1513061403</CreateTime><MsgType><![CDATA[device_text]]></MsgType><DeviceType><![CDATA[gh_b2007557ae68]]></DeviceType><DeviceID><![CDATA[gh_b2007557ae68_73516d32233606d2]]></DeviceID><Content><![CDATA[mG25BL58CDYwMiBCQTA2QTAwMwg=]]></Content><SessionID>799258</SessionID><MsgID>24765165087</MsgID><OpenID><![CDATA[oDvyGs1dQS3MO0UAfxvuE2_XmZMA]]></OpenID></xml>""",
    u"""<xml><ToUserName><![CDATA[gh_b2007557ae68]]></ToUserName><FromUserName><![CDATA[oDvyGs1dQS3MO0UAfxvuE2_XmZMA]]></FromUserName><CreateTime>1513061439</CreateTime><MsgType><![CDATA[device_text]]></MsgType><DeviceType><![CDATA[gh_b2007557ae68]]></DeviceType><DeviceID><![CDATA[gh_b2007557ae68_73516d32233606d2]]></DeviceID><Content><![CDATA[mG25BL58CDYwMiBCQTA2QTAwMwg=]]></Content><SessionID>799259</SessionID><MsgID>24765177782</MsgID><OpenID><![CDATA[oDvyGs1dQS3MO0UAfxvuE2_XmZMA]]></OpenID></xml>""",
    u"""<xml><ToUserName><![CDATA[gh_b2007557ae68]]></ToUserName><FromUserName><![CDATA[oDvyGs1dQS3MO0UAfxvuE2_XmZMA]]></FromUserName><CreateTime>1513061478</CreateTime><MsgType><![CDATA[device_text]]></MsgType><DeviceType><![CDATA[gh_b2007557ae68]]></DeviceType><DeviceID><![CDATA[gh_b2007557ae68_73516d32233606d2]]></DeviceID><Content><![CDATA[aGVsbG8=]]></Content><SessionID>799260</SessionID><MsgID>24765190780</MsgID><OpenID><![CDATA[oDvyGs1dQS3MO0UAfxvuE2_XmZMA]]></OpenID></xml>""",
]

if __name__ == '__main__':

    for msg in msg_list:
        msg = message_handle.get_send_msg(msg)
        print(msg)

