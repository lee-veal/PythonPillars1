"""
title: test_Flask
author: jlv4acl
date: 2019-01-16 13:29
"""

# from app import app
from flask_pillars_api import app
import pytest, json

class TestFlask:

    def test_flask(self):
        self.app = app.test_client()
        result = self.app.get('/todo/api/v1.0/tasks/1')

        print(result.get_data)
        print(result.data.decode())
        print(result.content_type)

        # assert the status code of the response
        assert result.status_code == 200

        assert result.content_type == "application/json"

    def test_last_city(self):
        self.app = app.test_client()
        print(self.app)
        result = self.app.get('/todo/api/v1.0/town/0')

        print("=============got here")
        print(result.get_data)
        locations = json.loads(result.data.decode())
        list_location = locations["locations"]
        last_location = list_location[-1]
        print("last::: ", last_location)

        assert last_location["cityName"] == "GARLAND"

    def test_location(self):
        self.app = app.test_client()
        print(self.app)
        result = self.app.get('/todo/api/v1.0/locations/554')
        print(result.status_code)

        location = result.data.decode()
        print(location)

        assert result.status_code == 200

        assert result.content_type == "application/json"

