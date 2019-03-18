# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0

import sys
import requests


class CodeStream(object):
    @staticmethod
    def endpoint_list(session):
        uri = f'/pipeline/api/endpoints'
        try:
            data = list()
            r = requests.get(f'{session.baseurl}{uri}', headers = session.headers)
            r.raise_for_status()
            j=r.json()
            print(j)
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        return data

    @staticmethod
    def endpoint_delete(session, id):
        pass

    @staticmethod
    def pipeline_list(session):
        pass

    @staticmethod
    def pipeline_delete(session, id):
        pass

    @staticmethod
    def pipeline_execute(session, name, id='70e3e4c1e2605a75575cc0da1d0c0'):
        uri = f'pipeline/api/pipelines/{id}/executions'
        body = {
            "comments" : "",
            "input" : {
                "aname" : name,
                "zoneId" : "Z3AMG3UGADPSG9",
                "zoneName" : "vmwapj.com",
                "target" : "52.221.230.108"
            },
            "executionLink" : "/pipeline/api/executions/70e3e4c1e2605a75575cc0da1d0c0",
            "tags" : []
            }
        try:
            r = requests.post(f'{session.baseurl}{uri}', headers = session.headers, json=body)
            r.raise_for_status()
            j=r.json()
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)
        return

    @staticmethod
    def pipeline_cancel(session, id):
        pass

    @staticmethod
    def pipeline_status(session, id):
        pass