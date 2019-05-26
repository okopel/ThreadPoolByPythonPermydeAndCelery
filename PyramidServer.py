"""""
Ori Kopel
okopel@gmail.com
AppCard May 2019
"""

from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

import config as settings
import dbManager
from CeleryServer import mult

"""""
# Create the DB
engine = create_engine('sqlite:///' + settings.client_data_path)
metadata_client_data = MetaData(engine)
table = Table(settings.client_data_name, metadata_client_data,
              Column('id', Integer, primary_key=True),
              Column('raw_data', String),
              Column('result', String), autoload=True)
# create the DB just if It does not exist
if not os.path.exists(settings.client_data_path):
    table.create()
"""

mydb = dbManager.DbManager.getInstance()


# upload Json params by POST
@view_config(route_name='upload', request_method='POST')
def upload(request):
    dict_of_req = request.json
    how_many_err = 0
    for k in dict_of_req:
        mult.delay(k, dict_of_req[k])
        # convert the list to string, and delete the ", " in the end
        raw_d = ''.join(str(e) + ', ' for e in dict_of_req[k])[:-2]
        how_many_err += mydb.insertEx(int(k), raw_d)
    if how_many_err < len(dict_of_req):
        print(settings.succ_sent)
        return Response(settings.succ_sent)
    else:
        print(settings.not_succ_sent)
        return Response(settings.not_succ_sent)


# get Answer from DB by id by GET
@view_config(route_name='result', request_method='GET')
def result(request):
    r_id = int(request.matchdict['result_id'])
    ans = mydb.getById(r_id)
    if ans == settings.tmp_var_name:  # The result isn't ready yet
        print(settings.ans_not_ready)
        return Response(settings.ans_not_ready)
    elif ans is None:  # The id is incorrect
        print(settings.ans_not_id.format(r_id))
        return Response(settings.ans_not_id.format(r_id))
    else:
        print(settings.ans_good.format(r_id, ans))
        return Response(json_body={"result": ans})


def open_server():
    with Configurator() as config:
        config.add_route('upload', '/upload')
        config.add_view(upload, route_name='upload')
        config.add_route('result', '/results/{result_id}')
        config.add_view(result, route_name='result')
        wapp = config.make_wsgi_app()
    server = make_server(settings.ip, settings.port, wapp)
    server.serve_forever()


if __name__ == '__main__':
    open_server()
