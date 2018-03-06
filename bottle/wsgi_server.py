from wsgiref.simple_server import make_server


def get_application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']


if __name__ == '__main__':
    httpd = make_server('', 8000, get_application)
    print('wsgi start.')
    httpd.serve_forever()
