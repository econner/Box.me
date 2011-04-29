BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "myuser"
BROKER_PASSWORD = "mypassword"
BROKER_VHOST = "myvhost"

CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("box.suggestion_engine.docsims", )

#: We want the results to expire in 5 minutes, note that this requires
#: RabbitMQ version 2.1.1 or higher, so please comment out if you have
#: an earlier version.
#CELERY_AMQP_TASK_RESULT_EXPIRES = 300