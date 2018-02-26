from bottle import route, run, template, post, get, request, abort, \
    HTTPError

# @route('/')
# @route('/hello')
# def hello():
#     return 'hello world'

@route('/')
@route('/hello/<name>')
def greet(name):
    return template('Hello {{ name }}, how are you?', name=name)

@route('/wiki/<pagename>')
def show_wiki_page(pagename):
    return '{} wiki'.format(pagename)

@get('/login')
@post('/login')  # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
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


import sys
run(host='localhost', port=sys.argv[1], debug=True)