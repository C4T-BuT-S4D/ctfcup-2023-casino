from os import getenv
from secrets import compare_digest

def check_task_token():
    token = input("task token: ")
    if not compare_digest(token, "b1d5f0d1e58be008"):
        exit(42)
