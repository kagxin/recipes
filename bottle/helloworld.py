from bottle import route, run, template, post, get, request, abort, \
    HTTPError, install, HTTPResponse, Bottle
from bottle_sqlite import SQLitePlugin

install(SQLitePlugin(dbfile='./test.db'))

# @route('/')
# @route('/hello')
# def hello():
#     return 'hello world'

@route('/')
@route('/hello/<name>')
def greet(name):
    return template('Hello {{ name }}, how are you???', name=name)

@route('/wiki/<pagename>')
def show_wiki_page(pagename):
    return '{} wiki'.format(pagename)

@get('/login')
@post('/login')  # or @route('/login', method='POST')
def do_login():
    print(request.headers['content_type'])
    print(request.body.read())
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username == 'user1' and password == u'password':
        return '<p> you login information was corrent. </p>'
    else:
        return '<p> Login failed. </p>'

@get('/show/<name:re:[a-z]+>')
def shows(name):
    return 'show {}'.format(name)

@get('/test/abort')
def test_abort():
    # abort(401, 'just test 401')
    return HTTPError(401, 'just test 401.')

@post('/pic')
def upload_pic():
    try:
        print(request.headers['content_type'])
        file = request.POST['pic']
    except KeyError:
        return HTTPResponse(status=400)

    file.save('./')
    return HTTPResponse(status=201)

@get('/get')
def test_get():
    s = request.GET.get('a')
    print(s)
    return HTTPResponse('haha')




import sys
for m in list(sys.modules.values()):
    if 'helloworld.py' in str(m):
        print(m)



# with Bottle() as b_app:
#     @b_app.route('/with')
#     def hello():
#         return HTTPResponse('with')

#     if len(sys.argv) == 2:
#         run(host='localhost', port=sys.argv[1], debug=True, reloader=True)
#     else:
#         run(host='localhost', port='8888', debug=True, reloader=True)

@route('/hello')
def greet(name):
    return HTTPResponse('hello2')

with Bottle() as b_app:
    @b_app.route('/hello')
    def hello():
        cl = request.headers.get('Content-length')
        cl = request.headers.get('content_length')
        print(cl)
        return HTTPResponse('hello')

    run(host='localhost', port='8888', debug=True, reloader=True)        
