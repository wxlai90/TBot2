import os
from TBot2 import TBot2

with open('.env', 'r') as f:
    envs = f.readlines()
    for env in envs:
        key, value = env.split("=")
        os.environ[key] = value

TOKEN = os.environ["BOT_TOKEN"]

t = TBot2(TOKEN)


@t.contains('apple')
def my_handler(req):
    return f"I love apple pies"


@t.catch_all()
def catch_all_handler(req):
    return "Sorry, I don't understand you."


t.ListenAndServe()
