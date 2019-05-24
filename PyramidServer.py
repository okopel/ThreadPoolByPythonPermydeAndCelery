from pyramid.response import Response
from pyramid.view import view_config
from pyramid.config import Configurator
from wsgiref.simple_server import make_server
from CeleryServer import mult
import sqlalchemy.sql
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.orm import mapper, sessionmaker
import pickle


# upload Json params by POST
@view_config(route_name='upload', request_method='POST')
def upload(request):
    dict = request.json
    for key in dict:
        ex = mult.delay(key, dict[key][0], dict[key][1], dict[key][2])
    return Response('upload {}'.format(ex.get()))


class Bookmarks(object):
    pass


# get Answer from DB by id by GET
@view_config(route_name='result', request_method='GET')
def result(request):
    id = int(request.matchdict['result_id'])
    engine = create_engine('sqlite:///results.sqlite', echo=True)
    metadata = MetaData(engine)
    table = Table('celery_taskmeta', metadata, autoload=True)
    mapper(Bookmarks, table)
    Session = sessionmaker(bind=engine)
    session = Session()
    x = session.execute(select([table.c.id, table.c.result]))
    for y in x:
        if y[0] == id:
            print("res of :{} is:{}".format(id, pickle.loads(y[1])))
            break
        else:
            print(y[0])
    #   return Response('<body><h1>exe is={} and the result is={}</h1></body>'.format(ex, res))
    return Response('<body><h1>There is not such ID ={}</h1></body>'.format(id))


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('upload', '/upload')
        config.add_view(upload, route_name='upload')

        config.add_route('result', '/results/{result_id}')
        config.add_view(result, route_name='result')

        wapp = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, wapp)
    server.serve_forever()
