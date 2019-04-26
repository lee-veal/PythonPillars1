"""
title: flask_pillars_api
author: jlv4acl
date: 2019-01-15 15:22
"""

import os, json
from flask import Flask, jsonify,  request, abort, make_response

port = int(os.getenv('PORT', '3000'))

app = Flask(__name__)


@app.route('/')
def hello():
    print(port)
    return "Hello, World!"


@app.route('/bye')
def bye():
    return "hasta la vista  ...."


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not Today Pal"}), 404)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': True
    }
]


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_tasks(task_id):
    print(request.data)
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

#  curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})
#  curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks/3


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/locations/<int:location_id>', methods=['GET'])
def get_locations(location_id):
    with open('thd_location.json', 'r') as thd_locations:
        data = json.load(thd_locations)
        if location_id == 0:
            pretty_output = json.dumps(data, indent=4)
        else:
            pretty_output = "default"
            for location in data["locations"]:
                if location_id == location["locationNumber"]:
                    pretty_output = json.dumps(location, indent=4)
                    break

    return pretty_output


@app.route('/todo/api/v1.0/town/<string:city_name>', methods=['GET'])
def get_city_stores(city_name):
    with open('thd_location.json', 'r') as thd_locations:
        data = json.load(thd_locations)
        if city_name == "0":
            pretty_output = json.dumps(data, indent=4)
        else:
            location_list = []
            for location in data["locations"]:
                if city_name == location["cityName"]:
                    location_list.append(location)
            pretty_output = json.dumps(location_list, indent=4)

    return pretty_output


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

