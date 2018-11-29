class Network(object):
    def __init__(self, network):
        pass

    @staticmethod
    def list(session):
        uri = f'/iaas/networks'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/networks/{id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/networks/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )


class Machine(object):
    def __init__(self):
        pass

    @staticmethod
    def list(session):
        uri = f'/iaas/machines'
        j = session._request(f'{session.baseurl}{uri}')
        return j['content']

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/machines/{id}'
        session._request(f'{session.baseurl}{uri}',
                         request_method='DELETE'
                         )

    @staticmethod
    def find_by_user(session, user):
        uri = (f"/iaas/machines?$filter=(((type eq 'VM_GUEST') and "
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
        uri = f'/provisioning/uerp{uri}'
        payload = session._request(f'{session.baseurl}{uri}')
        payload['customProperties']['__groupResourcePlacementLink'] = ""
        return session._request(f'{session.baseurl}{uri}',
                                request_method='PATCH',
                                payload=payload
                                )
