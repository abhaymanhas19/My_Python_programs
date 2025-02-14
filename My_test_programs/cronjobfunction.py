# from celery import Celery
# from kombu import Exchange, Queue

# app = Celery("cronjobfunction", broker="redis://localhost:6379/0", backend='redis://localhost:6379/0')
# app.conf.broker_connection_retry_on_startup=True
# app.conf.task_queues = (
#     Queue('demo', Exchange('demo'), routing_key='demo'),
# )

# @app.task
# def demo_task(messge):efkwenf
#     print("Executing demo task")

def test():
    name="abhay"
    
    
    def test1():
        nonlocal name
        for i in "abhaya":
            name+=i
            
    test1()
    test1()
    return name

print(test())

name=""
if  name:
    print("yes")