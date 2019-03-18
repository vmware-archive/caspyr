# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0

import os


class User(object):
    """
    The user and organisation management runs through the centralised
    Cloud Services Portal and as such, we use a different baseurl for
    this module when compared with the other modules.
    """

    def __init__(self, org):
        self.name = org['name']
        self.display_name = org['displayName']
        self.ref_link = org['refLink']
        self.metadata = org['metadata']
        self.id = os.path.split(self.ref_link)[1]
        try:
            self.parent_ref_link = org['parentRefLink']
        except KeyError:
            pass

    @classmethod
    def describe(cls, session, id):
        baseurl = 'https://console.cloud.vmware.com'
        uri = f'/csp/gateway/am/api/orgs/{id}/'
        return cls(session._request(f'{baseurl}{uri}'))

    @staticmethod
    def list(session, id):
        baseurl = 'https://console.cloud.vmware.com'
        uri = f'/csp/gateway/portal/api/v2/orgs/{id}/users'
        return session._request(f'{baseurl}{uri}')['results']

    @staticmethod
    def find(session, id, search):
        baseurl = 'https://console.cloud.vmware.com'
        uri = (f'/csp/gateway/portal/api/orgs/{id}/users/search?'
               f'userSearchTerm={search}')
        return session._request(f'{baseurl}{uri}')['results']

    @staticmethod
    def remove(session, id, username):
        baseurl = 'https://console.cloud.vmware.com'
        uri = f'/csp/gateway/portal/api/orgs/{id}/users/'
        payload = {
            "emails": [
                username
            ]
        }
        return session._request(f'{baseurl}{uri}',
                                request_method='PATCH',
                                payload=payload)

    @staticmethod
    def invite(session,
               id,
               usernames,
               org_role='org_member',
               cloud_assembly=False,
               code_stream=False,
               service_broker=False,
               log_intelligence=False,
               network_insight=False
               ):
        baseurl = 'https://console.cloud.vmware.com'
        uri = f'/csp/gateway/am/api/orgs/{id}/invitations'
        payload = {
            'usernames': usernames,
            'orgRoleName': org_role,
            'serviceRolesDtos': []
        }
        if cloud_assembly:
            payload['serviceRolesDtos'].append({
                'serviceDefinitionLink': ('/csp/gateway/slc/api/definitions'
                                          '/external'
                                          '/Zy924mE3dwn2ASyVZR0Nn7lupeA_'
                                          ),
                'serviceRoleNames':
                    [
                        'automationservice:user',
                        'automationservice:cloud_admin'
                    ]
            })

        if code_stream:
            payload['serviceRolesDtos'].append({
                'serviceDefinitionLink': ('/csp/gateway/slc/api/definitions'
                                          '/external'
                                          '/ulvqtN4141beCT2oOnbj-wlkzGg_'
                                          ),
                'serviceRoleNames':
                    [
                        'CodeStream:administrator',
                        'CodeStream:viewer',
                        'CodeStream:developer'
                    ]
            })

        if service_broker:
            payload['serviceRolesDtos'].append({
                'serviceDefinitionLink': ('/csp/gateway/slc/api/definitions'
                                          '/external'
                                          '/Yw-HyBeQzjCXkL2wQSeGwauJ-mA_'
                                          ),
                'serviceRoleNames':
                [
                    'catalog:admin',
                    'catalog:user'
                ]
            })

        if log_intelligence:
            payload['serviceRolesDtos'].append({
                'serviceDefinitionLink': ('/csp/gateway/slc/api/definitions'
                                          '/external'
                                          '/7cJ2ngS_hRCY_bIbWucM4KWQwOo_'
                                          ),
                'serviceRoleNames':
                    [
                        'log-intelligence:admin',
                        'log-intelligence:user'
                    ]
            })

        if network_insight:
            payload['serviceRolesDtos'].append({
                'serviceDefinitionLink': ('/csp/gateway/slc/api/definitions'
                                          '/external'
                                          '/9qjoNafDp9XkyyQLcLCKWPsAir0_'
                                          ),
                'serviceRoleNames':
                    [
                        'vrni:admin',
                        'vrni:user'
                    ]
            })

        return session._request(f'{baseurl}{uri}',
                                request_method='POST',
                                payload=payload
                                )
