from bottle import (
    Bottle, HTTPError, run, request, response, static_file, #view, 
    redirect, 
)
from bottle import jinja2_view
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from model import Base, Entity, AssetType
import functools, pdb

#use jinja2 template
view = functools.partial(jinja2_view, template_lookup=['./views/jinja2_tpl'])

engine = create_engine('sqlite:///sql.db', echo=True)
app = Bottle()
plugin = sqlalchemy.Plugin(engine, Base.metadata, create=True)
app.install(plugin)

@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./static')

@app.get('/<name>')
def show(name, db):
    entity = db.query(Entity).filter_by(name=name).first()
    if entity:
        return {'id': entity.id, 'name': entity.name}
    return HTTPError(404, 'Entity not found.')
@app.put('/<name>')
def put_name(name, db):
    entity = Entity(name)
    db.add(entity)

@app.route('/addassettype')
@view('add_assettype_template')
def index():
    pass #

@app.route('/assettype', method='POST')
def post_assettype(db):
    #pdb.set_trace()
    assetname = request.forms.getunicode('assetname')
    detailtype = request.forms.getunicode('detailtype')
    if assetname == '' or detailtype == '':
        redirect('/assettype')
    at = AssetType(assetname=assetname, detailtype=detailtype)
    db.add(at)
    redirect("/")

@app.route('/')
@view('assettype_template')
def get_assettype(db):
    response.content_type = 'text/html; charset=utf8'
    #pdb.set_trace()
    #at = db.query(AssetType).filter_by(id=3).first()
    ats = db.query(AssetType).all()
    #print(ats)
    return dict(name=ats)

@app.route('/assettype/delete', method='POST')
def del_assettype(db):
    delid = request.forms.getunicode('id')
    try:
        delrow = db.query(AssetType).filter_by(id=int(delid)).one()
    except Exception as err:
        print(err)
    else:
        try:
            db.delete(delrow)
        except Exception as err:
            print(err)
        else:
            return {'data':'success'}

if __name__ == '__main__':
    run(app, host='localhost', port=5000, debug=True, reloader=True, server='waitress')