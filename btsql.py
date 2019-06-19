from bottle import (
    Bottle, HTTPError, request, response, static_file, #view, 
    redirect, 
)
from bottle import jinja2_view
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from model import Base, Entity, AssetType, Asset
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

@app.route('/')
@view('index')
def index():
    pdb.set_trace()
    with open('request.environ.txt', 'w') as fo:
        fo.write(str(request.environ))
        #for k,v in request.environ.items():
        #    fo.write('{} = {}\n'.format(k, v))

# module assettype start
@app.route('/addassettype')
@view('add_assettype_template')
def add_assettype():
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
    redirect("/assettype")

@app.route('/assettype')
@view('assettype_template')
def get_assettype(db):
    response.content_type = 'text/html; charset=utf8'
    #at = db.query(AssetType).filter_by(id=3).first()
    ats = db.query(AssetType).all()
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
# module assettype end

# module asset start
@app.route('/addasset')
@view('add_asset_template')
def add_asset(db):
    ats = db.query(AssetType).all()
    return dict(name=ats)

@app.route('/asset', method='POST')
def post_asset(db):
    assettypeid = request.forms.getunicode('assettypeid')
    asiden = request.forms.getunicode('asiden')
    asorgan = request.forms.getunicode('asorgan')
    bill_dt = request.forms.getunicode('bill_dt')
    repayment_dt = request.forms.getunicode('repayment_dt')
    credit_limit = request.forms.getunicode('credit_limit')
    year_rate = request.forms.getunicode('year_rate')
    comment = request.forms.getunicode('comment')
    print(assettypeid, asiden, asorgan)
    if assettypeid == '' or asiden == '' or asorgan == '':
        redirect('/asset')
    asset = Asset(
        asiden=asiden, 
        asorgan=asorgan,
        bill_dt=bill_dt,
        repayment_dt=repayment_dt,
        credit_limit=credit_limit,
        year_rate=year_rate,
        comment=comment
    )
    db.add(asset)
    redirect("/asset")

@app.route('/asset')
def get_asset(db):
    pass
# module asset end
