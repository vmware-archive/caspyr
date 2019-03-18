# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0

class Network(object):
    def __init__(self, network):
        pass

    @staticmethod
    def list(session):
        uri = f'/iaas/api/networks'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/api/networks/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/networks/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )


class Machine(object):
    def __init__(self):
        pass

    @staticmethod
    def list(session):
        uri = f'/iaas/api/machines'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/api/machines/{id}'
        return session._request(f'{session.baseurl}{uri}')

    @staticmethod
    def get_ip(session,
               machine_id,
               nic_index=0,
               address_index=0
               ):
        """Get the internal address of a machine.
        This method defaults to returning the first IP address of the first
        network interface on the provided machine id. You can adjust the
        interface and address index with the nic_index and address_index
        values.

        :param session: The Session object
        :type session: cls
        :param machine_id: The resource id of the machine
        :type machine_id: str
        :param nic_index: The index of the network interface for which you
            want to retrieve the address. Defaults to 0.
        :type nic_index: int
        :param address_index: The index of the address which you want to
            retrieve.
        Defaults to 0.
        """
        j = Machine.describe(session, machine_id)
        uri = j["_links"]["network-interfaces"]["hrefs"][nic_index]
        i = session._request(f'{session.baseurl}{uri}')
        return i['addresses'][address_index]

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/api/machines/{id}'
        session._request(f'{session.baseurl}{uri}',
                         request_method='DELETE'
                         )

    @staticmethod
    def find_by_user(session, user):
        uri = (f"/iaas/api/machines?$filter=(((type eq 'VM_GUEST') and "
               f"(lifecycleState ne 'RETIRED')) and "
               f"(tenantLinks.item eq "
               f"'/owner/provisioning/auth/csp/users/{user}'))"
               )
        return session._request(f'{session.baseurl}{uri}')['content']

    @staticmethod
    def list_orphaned(session):
        uri = f'/provisioning/uerp/resources/compute?$filter=customProperties.__groupResourcePlacementLink eq *'
        return session._request(f'{session.baseurl}{uri}')['documentLinks']

    @staticmethod
    def unregister(session, uri):
        uri = f'/provisioning/uerp/{uri}'
        payload = session._request(f'{session.baseurl}{uri}')
        payload['customProperties']['__groupResourcePlacementLink'] = ""
        return session._request(f'{session.baseurl}{uri}',
                                request_method='PATCH',
                                payload=payload
                                )
