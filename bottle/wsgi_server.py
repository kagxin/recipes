from wsgiref.simple_server import make_server, demo_app


def get_application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']



if __name__ == '__main__':
    with make_server('', 8000, demo_app) as httpd:
        sa = httpd.socket.getsockname()
        print("Serving HTTP on", sa[0], "port", sa[1], "...")
        httpd.serve_forever()
