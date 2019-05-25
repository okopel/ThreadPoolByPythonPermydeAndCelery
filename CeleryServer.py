"""""
Ori Kopel
okopel@gmail.com
AppCard May 2019
"""

import os.path

from celery import Celery
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

import celeryconfig
import config as settings

# Initialization Celery Server
app = Celery('tasks')
app.config_from_object(celeryconfig)

# open exist DB to save the results
engine = create_engine('sqlite:///' + settings.client_data_path)
metadata = MetaData(engine)
tableOfRes = Table(settings.client_data_name, metadata,
                   Column('id', Integer, primary_key=True),
                   Column('raw_data', String),
                   Column('result', String))

# tableOfRes = Table(settings.client_data_name, metadata, autoload=True)
if not os.path.exists(settings.client_data_path):
    tableOfRes.create()


# This task get ID(=key) and some args
# calculate multiply of the args and and save it to DB
@app.task
def mult(key, args):
    ans = 1
    for num in args:
        ans *= num
    update_by_id(key, ans)
    return ans


# update the DB res by id
def update_by_id(r_id, ans):
    msg = tableOfRes.update().values(result=str(ans)).where(tableOfRes.columns.id == r_id)
    engine.execute(msg)
