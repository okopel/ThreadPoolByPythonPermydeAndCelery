"""""
Ori Kopel
okopel@gmail.com
"""

from celery import Celery
from sqlalchemy import create_engine, MetaData, Table

import celeryconfig

# Initialization Celery Server
app = Celery('tasks')
app.config_from_object(celeryconfig)

# open exist DB to save the results
engine = create_engine('sqlite:///client_data.db', echo=True)
metadata = MetaData(engine)
tableOfRes = Table('client_data', metadata, autoload=True)


# This task get ID(=key) and some args
# calculate multiply of the args and and save it to DB
@app.task
def mult(key, args):
    ans = 1
    for num in args:
        ans *= num
    # sleep(10)
    update_by_id(key, ans)
    return ans


# update the DB res by id
def update_by_id(r_id, ans):
    msg = tableOfRes.update().values(result=str(ans)).where(tableOfRes.columns.id == r_id)
    engine.execute(msg)
