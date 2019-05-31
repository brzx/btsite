from bottle import run
from btsql import app

if __name__ == '__main__':
    run(app, host='localhost', port=5000, debug=True, reloader=True, server='waitress')
