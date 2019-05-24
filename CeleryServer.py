from time import sleep

from celery import Celery
import celeryconfig

app = Celery('tasks')
app.config_from_object(celeryconfig)


@app.task
def mult(key, x, y, z):
    # sleep(10)
    return x * y * z


"""""
def store_metadata(key, x, y, z):
    metadata = TaskMetaData()
    metadata.task_id = key
    metadata.task_ex = "{}*{}*{}".format(x, y, z)

    metadata.save()
"""
