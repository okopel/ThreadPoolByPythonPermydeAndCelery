from pyramid.response import Response
from pyramid.view import view_config
from pyramid.config import Configurator
from wsgiref.simple_server import make_server
from CeleryServer import mult
import time
import json


# upload Json params by POST
@view_config(route_name='upload', request_method='POST')
def upload(request):
    dict = request.json
    for key in dict:
        ex = mult.delay(dict[key][0], dict[key][1], dict[key][2])
    return Response('upload {}'.format(ex.get()))


# get Answer from DB by id by GET
@view_config(route_name='result', request_method='GET')
def result(request):
    id = request.matchdict['result_id']

    # if mydb.isInDB(id):
    #    ex, res = mydb.loadRes(id)
    #   return Response('<body><h1>exe is={} and the result is={}</h1></body>'.format(ex, res))
    # else:
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
