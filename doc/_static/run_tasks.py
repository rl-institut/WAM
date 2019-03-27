
from app_name import tasks


running_task = None


def start_task():
    # Running task has to be stored, in order to get results
    running_task = tasks.multiply_by_ten.delay(10)


def task_is_ready():
    # Returns True if task has finished
    return running_task.ready()


def get_results():
    # Returns results of the tasks
    return running_task.get()
