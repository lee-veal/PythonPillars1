"""
title: flask_pillars_api_auth
author: jlv4acl
date: 2019-01-17 15:22
"""

import os
import json
import requests
import config
from flask import Flask, jsonify,  request, abort, make_response

port = int(os.getenv('PORT', '4000'))

app = Flask(__name__)

client_id = os.environ.get('AUTH_CLIENT_ID')
client_secret = os.environ.get('AUTH_CLIENT_SECRET')

def newToken():
    token_url = 'https://master-data-security.apps-np.homedepot.com/security/oauth/token'

    data = [
        ('grant_type', 'client_credentials')
    ]
    print(client_id, client_secret)
    try:
        response = requests.post(token_url,
                                 data=data,
                                 auth=
                                    (
                                      config.AUTH_CLIENT_ID,
                                      config.AUTH_CLIENT_SECRET
                                    )
                                 )
        response_json = response.json()

        token = response_json["access_token"]
        head = {'Authorization': 'Bearer ' + token}

        #print("Got Token!", response_json["access_token"])
        print("Got Token!\n", head)
        print("Got Token!")
        return head
    except Exception as e:
        print (e)
        print("Error with Token")
        return("Error with Token\n")


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


@app.route('/todo/api/v1.0/locations/<int:location_id>', methods=['GET'])
def get_locations(location_id):

    head = newToken()
    markets_url = f'https://master-data-location.apps-np.homedepot.com//location/location/number/{location_id}/type/STR'
    print(markets_url)

    # markets_url = 'https://master-data-location.apps-np.homedepot.com//location/location/'
    response = requests.get(markets_url, headers=head)
    location_json = response.json()
    print(location_json)
    pretty_output = json.dumps(location_json, indent=4)

        # data = json.load(thd_locations)
        # if location_id == 0:
        #     markets_url = 'https://master-data-location.apps-np.homedepot.com//location/location/'
        #     pretty_output = json.dumps(data, indent=4)
        # else:
        #     pretty_output = "default"
        #     for location in locations_json["locations"]:
        #         if location_id == location["locationNumber"]:
        #             pretty_output = json.dumps(location, indent=4)
        #             break

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

