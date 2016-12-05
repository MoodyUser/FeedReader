import json

from bottle import route, run, template, response
from dal.facebook import page_manager, feed_manager

'''
only GET, so bottle.
for more robust use mongodb-rest.
'''


@route('/')
def index():
    return template('rest/index')


@route('/pages', method='GET')
def pages():
    items = [item for key, item in page_manager.get_pages().items()]
    response.content_type = 'application/json'
    return json.dumps(items)


@route('/feeds')
def feeds():
    response.headers['Access-Control-Allow-Origin'] = '*'
    items = [item for key, item in feed_manager.get_feeds().items()]
    response.content_type = 'application/json'
    return json.dumps(items)


def run_server(host='localhost', port=8080):
    run(host=host, port=port)
