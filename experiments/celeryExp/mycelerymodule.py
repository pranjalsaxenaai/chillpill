from celery import Celery

# The name of this module should be the same as the name of Celery App created
# i.e. the first argument of Celery constructor
# This same name will be used to start workers using => celery -A mycelerymodule worker --loglevel=info -P solo
# The name of instance "app" will be used to register tasks
# tasks module is included in the include argument of Celery constructor to configure the Celery App to include tasks from the tasks module
app = Celery(
    'mycelerymodule', 
    broker='redis://localhost:6379/0',  # Example using Redis as a message broker
    backend='redis://localhost:6379/0',
    include=['tasks'])  # Example using Redis as a result backend
