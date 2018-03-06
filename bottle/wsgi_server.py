from wsgiref.simple_server import make_server, demo_app


def get_application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']



if __name__ == '__main__':
    httpd = make_server('', 8000, demo_app)
    print('wsgi start.')
    httpd.serve_forever()
