
from wam.celery import app


@app.task
def multiply_by_ten(number):
    return number * 1000
