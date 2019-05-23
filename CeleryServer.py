from celery import Celery
import celeryconfig
import sqlalchemy
from sqlalchemy import create_engine

# app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='db+sqlite:///results.sqlite')


app = Celery('tasks')
app.config_from_object(celeryconfig)


# engine = create_engine('sqlite:///results.sqlite')


# app.conf.result_backend(engine)


@app.task
def mult(x, y, z):
    return x * y * z


# if __name__ == '__main__':


def sendRes():
    # send result to the DB
    return 0
