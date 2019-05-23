from bottle import (
    Bottle, run, template, static_file, request, response,
    abort, redirect, install, 
)
import time

apq = Bottle()

@apq.route('/hello')
def hello():
    return {'key': 'word', 'value': "Hello World!"}

@apq.route('/helloagain')
def hello_again():
    if request.get_cookie('visited'):
        return 'Welcome back! Nice to see you again.'
    else:
        response.set_cookie('visited', 'yes')
        return 'Hello there! Nice to meet you'

@apq.route('/')
@apq.route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)

@apq.route('/wiki/<pagename>')
def show_wiki_page(pagename):
    response.set_header('Content-Language', 'en')
    response.set_header('Set-Cookie', 'name=value')
    response.add_header('Set-Cookie', 'name2=value2')
    pass

@apq.route('/action/<action>/<user>')
def user_api(action, user):
    return '{} and {}'.format(action, user)

@apq.route('/object/<id:int>')
def get_object(id):
    assert isinstance(id, int)

@apq.route('/show/<name:re:[a-z]+>')
def showname(name):
    assert name.isalpha()

@apq.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./static')

@apq.get('/login') # or @apq.route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@apq.post('/login') # or @apq.route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        response.set_cookie('account', username, secret='some-secret-key')
        return "<p>Welcome {}! Your login information was correct.</p>".format(username)
    else:
        return "<p>Login failed.</p>"

def check_login(username, password):
    if username == 'brian' and password == '123456':
        return True
    else:
        return False

@apq.route('/iso')
def get_iso():
    #response.charset = 'ISO-8859-15'
    return u'This will be sent with ISO-8859-15 encoding.'

@apq.route('/latin9')
def get_latin():
    response.content_type = 'text/html; charset=latin9'
    return u'ISO-8859-15 is also known as latin9.'

@apq.route('/chinese')
def get_chinese():
    return u'试试中文怎么样'

@apq.route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root='./static', download=filename)

@apq.route('/restricted')
def restricted_area():
    username = request.get_cookie('account', secret='some-secret-key')
    if username:
        return template("Hello {{name}}. Welcome back.", name=username)
    else:
        return 'You are not logged in. Access denied.'

@apq.route('/restricted401')
def restricted():
    abort(401, 'Sorry, access denied.')

@apq.route('/wrong/url')
def wrong():
    redirect('/hello')

@apq.route('/is_ajax')
def is_ajax():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return 'This is an AJAX request'
    else:
        return 'This is a normal request'

@apq.route('/forum')
def display_forum():
    forum_id = request.query.id
    page = request.query.page or '1'
    return template('Forum ID: {{id}} (page {{page}})', id=forum_id, page=page)

@apq.route('/my_ip')
def show_ip():
    ip = request.environ.get('REMOTE_ADDR')
    # or ip = request.get('REMOTE_ADDR')
    # or ip = request['REMOTE_ADDR']
    return template("Your IP is: {{ip}}", ip=ip)

def stopwatch(callback):
    def wrapper(*args, **kwargs):
        start = time.time()
        body = callback(*args, **kwargs)
        end = time.time()
        response.headers['X-Exec-Time'] = str(end - start)
        print(str(end-start))
        return body
    return wrapper

apq.install(stopwatch)

if __name__ == '__main__':
    run(apq, host='localhost', port=5000, debug=True, reloader=True)