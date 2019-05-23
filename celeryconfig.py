## Broker settings.
# broker_url = 'pyamqp://guest@localhost//'

# List of modules to import when the Celery worker starts.
# imports = ('myapp.tasks',)

## Using the database to store task state and results.
result_backend = 'db+sqlite:///results.sqlite'
# CELERY_RESULT_BACKEND = 'db+sqlite:///results.sqlite'
# task_annotations = {'tasks.add': {'rate_limit': '10/s'}}
broker = 'pyamqp://guest@localhost//'
# backend = 'db+sqlite:///results.sqlite'
result_extended = True
