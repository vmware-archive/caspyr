import requests
import json
import os
import sys

class Request(object):
    def __init__(self, request):
        self.id = request['id']
        self.progress = request['progress']
        self.message = request['message']
        self.name = request['name']
        self.status = request['status']
        self.self_link = request['selfLink']

    @classmethod
    def list(cls, session):
        uri = f'/iaas/request-tracker/'
        return session._request(f'{session.baseurl}{uri}')['content']

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/request-tracker/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @staticmethod
    def cancel(session, id):
        uri = f'/blueprint/api/blueprint-requests/{id}?action=cancel'
        return session._request(f'{session.baseurl}{uri}')

    @classmethod
    def list_incomplete(cls, session):
        r = cls.list(session)
        data = []
        for i in r:
            d = cls.describe(session, i['id'])
            if d.status != 'FINISHED':
                data.append({ "id" : d.id })
        return data
