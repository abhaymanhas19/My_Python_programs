# from celery import Celery
# from kombu import Exchange, Queue

# app = Celery("cronjobfunction", broker="redis://localhost:6379/0", backend='redis://localhost:6379/0')
# app.conf.broker_connection_retry_on_startup=True
# app.conf.task_queues = (
#     Queue('demo', Exchange('demo'), routing_key='demo'),
# )

# @app.task
# def demo_task(messge):
#     print("Executing demo task")

