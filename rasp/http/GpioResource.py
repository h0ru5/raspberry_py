'''
Created on 17.09.2013

@author: mail_000
'''
from bottle import route,run

@route('/')
def index():
    return {"ports" : range(1,27)}

def start(port):
    run(port=port)