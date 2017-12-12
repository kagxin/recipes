import base64
from wechatpy.utils import to_binary, to_text
from wechatpy.fields import Base64DecodeField, StringField, Base64EncodeField
from wechatpy.events import register_event, BaseEvent


class Base64DecodeNotTextField(Base64DecodeField):

    def __base64_decode(self, text):
        return base64.b64decode(to_binary(text))

@register_event('device_text')
class DeviceTextEvent(BaseEvent):
    event = 'device_text'
    device_type = StringField('DeviceType')
    device_id = StringField('DeviceID')
    session_id = StringField('SessionID')
    content = Base64DecodeNotTextField('Content')
    open_id = StringField('OpenID')
