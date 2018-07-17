import requests
import base64

def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.decodestring(data)


sess = requests.Session()
res = sess.post('http://localhost:8000/api-token-auth/', json={'username':'admin', 'password':'admin123'})
print(res.json())
data = res.json()
if res.status_code == 200:
    token = data['token']
    header, payload, signature = ( decode_base64(s.encode()).decode() if i!=2 else s for i, s in enumerate(token.split('.')))
    print('JWT header:    {}'.format(header))  
    print('JWT payload:   {}'.format(payload))
    print('JWT signature: {}'.format(signature))
    res = sess.get('http://localhost:8000/test/', headers={'Authorization': 'JWT {}'.format(token)})
    print(res.json())
else:
    print('please check args.')