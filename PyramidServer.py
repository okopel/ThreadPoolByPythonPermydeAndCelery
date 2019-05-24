"""""
Ori Kopel
okopel@gmail.com
"""

import os.path
from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import select, create_engine, MetaData, Table, Column, String, Integer

from CeleryServer import mult

# Create the DB
engine_client_data = create_engine('sqlite:///client_data.db')
metadata_client_data = MetaData(engine_client_data)
tableOfclientData = Table('client_data', metadata_client_data,
                          Column('id', Integer, primary_key=True),
                          Column('raw_data', String),
                          Column('result', String))
# create the DB just if It does not exist
if not os.path.exists("client_data.db"):
    tableOfclientData.create()


# upload Json params by POST
@view_config(route_name='upload', request_method='POST')
def upload(request):
    dict_of_req = request.json
    for k in dict_of_req:
        mult.delay(k, dict_of_req[k])
        # convert the list to string, and delete the ", " in the end
        raw_d = ''.join(str(e) + ', ' for e in dict_of_req[k])[:-2]
        msg = tableOfclientData.insert().values(id=int(k), raw_data=raw_d, result="WAIT")
        engine_client_data.execute(msg)
    try:
        return Response('The args sent!')
    except:
        print('The args sent!')


# get Answer from DB by id by GET
@view_config(route_name='result', request_method='GET')
def result(request):
    r_id = int(request.matchdict['result_id'])
    msg = select([tableOfclientData.c.result]).where(tableOfclientData.c.id == r_id)
    ans = engine_client_data.execute(msg).scalar()
    if ans == "WAIT":
        try:
            return Response('<body><h1>The answer isn\'t ready yet</h1></body>'.format(r_id))
        except:
            print('The answer isn\'t ready yet'.format(r_id))
    elif ans is None:
        try:
            return Response('<body><h1>There isn\'t such ID ={}</h1></body>'.format(r_id))
        except:
            print('There isn\'t such ID ={}'.format(r_id))
    else:
        try:
            return Response('<body><h1>res of :{} is:{})</h1></body>'.format(r_id, ans))
        except:
            print('res of :{} is:{}'.format(r_id, ans))


def open_server():
    with Configurator() as config:
        config.add_route('upload', '/upload')
        config.add_view(upload, route_name='upload')
        config.add_route('result', '/results/{result_id}')
        config.add_view(result, route_name='result')
        wapp = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, wapp)
    server.serve_forever()


if __name__ == '__main__':
    open_server()

"""
The default DB of CELERY
engine = create_engine('sqlite:///results.sqlite', echo=True)
metadata = MetaData(engine)
tableOfRes = Table('celery_taskmeta', metadata, autoload=True)
"""
