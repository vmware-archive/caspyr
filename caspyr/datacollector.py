class DataCollector(object):
    def __init__(self, rdc):
        pass

    @staticmethod
    def list(session):
        uri = '/iaas/data-collectors/'
        data = []
        j = session._request(f'{session.baseurl}{uri}')['content']
        for i in j:
            content = {}
            content['id'] = i['dcId']
            content['name'] = i['name']
            data.append(content)
        return data

    @classmethod
    def describe(cls, session, id):
        uri = f'/iaas/data-collectors/{id}'
        return session._request(f'{session.baseurl}{uri}')

    @staticmethod
    def delete(session, id):
        uri = f'/iaas/data-collectors/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )
