from celery import shared_task


@shared_task(bind=True, name="my_task")
def my_task(self):
    print("Hello World")
