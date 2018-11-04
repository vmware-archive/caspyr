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
        return session._request(f'{session.baseurl}{uri}', request_method='DELETE')

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
        session._request(f'{session.baseurl}{uri}', request_method='DELETE')

    @staticmethod
    def list_orphaned(session):
        uri = f'/iaas/machines?$filter=projectId eq \'*\''
        return session._request(f'{session.baseurl}{uri}')['content']
