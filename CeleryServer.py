"""""
Ori Kopel
okopel@gmail.com
AppCard May 2019
"""

from celery import Celery

import celeryconfig
import dbManager

# Initialization Celery Server
app = Celery('tasks')
app.config_from_object(celeryconfig)

# get instance of the singleton DB
mydb = dbManager.DbManager.getInstance()


# This task get ID(=key) and some args
# calculate multiply of the args and and save it to DB
@app.task
def mult(key, args):
    ans = 1
    for num in args:
        ans *= num
    suc = mydb.updateResById(key, ans)
    if suc is None:
        print(key, "cant update")
    return ans
