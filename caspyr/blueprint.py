"""Module for interacting with Blueprints.
"""

import os
import requests


class Blueprint:
    """
    Class for methods related to Blueprints.
    :method list: Returns the ids of all blueprints.
    :method describe: Returns the full schema of the blueprint.
    :method create: Creates a blueprint, returns an object.
    :method create_from_JSON: Creates a blueprint from JSON,
    returns an object.
    :method delete: Deletes the blueprint.
    """
    # pylint: disable=too-many-instance-attributes
    # returning a full fidelity class representation of the
    # API return for a Blueprint.

    def __init__(self, blueprint):
        self.name = blueprint['name']
        self.description = blueprint['description']
        self.tags = blueprint['tags']
        self.content = blueprint['content']
        self.valid = blueprint['valid']
        self.validation_messages = blueprint['validationMessages']
        self.status = blueprint['status']
        self.project_id = blueprint['projectId']
        self.project_name = blueprint['projectName']
        self.type = blueprint['type']
        self.id = blueprint['id']
        self.self_link = blueprint['selfLink']
        self.created_at = blueprint['createdAt']
        self.created_by = blueprint['createdBy']
        self.updated_at = blueprint['updatedAt']
        self.updated_by = blueprint['updatedBy']
        self.tenants = blueprint['tenants']

    @staticmethod
    def list(session):
        """Retrieves list of all blueprints that the logged-in
        user has access to.

        :param session: The session object.
        :type session: object
        :return: A list of blueprint ids.
        :rtype: list
        """

        uri = '/blueprint/api/blueprints/'
        data = []
        j = session._request(f'{session.baseurl}{uri}')
        for i in j['links']:
            i = os.path.split(i)[1]
            data.append({"id": i})
        return data

    @classmethod
    def describe(cls, session, blueprint_id):
        """Retrieves all details of the specified blueprint
        and creates a class object of it.

        :param session: The session object.
        :type session: object
        :param blueprint_id: The id of the blueprint that you want the details
        of.
        :type blueprint_id: string
        :return: Returns a blueprint class object.
        :rtype: cls
        """

        uri = f'/blueprint/api/blueprints/{blueprint_id}'
        return cls(session._request(f'{session.baseurl}{uri}'))

    @staticmethod
    def get_inputs(session, blueprint_id):
        """Retrieve the inputs that need to be submitted with the specified blueprint.

        :param session: The session object.
        :type session: object
        :param blueprint_id: The id of the blueprint that you want to retrieve
        the inputs for.
        :type id: string
        :return: [description]
        :rtype: [type]
        """

        uri = f'/blueprint/api/blueprints/{blueprint_id}/inputs-schema'
        return session._request(f'{session.baseurl}{uri}')

    @classmethod
    def create_from_json(cls,
                         session,
                         jsonfile
                         ):
        payload = open(jsonfile).read()
        uri = f'/blueprint/api/blueprints'
        return cls(session._request(f'{session.baseurl}{uri}',
                                    request_method='POST',
                                    payload=payload
                                    ))

    @classmethod
    def create(cls,
               session,
               bpname,
               displayname,
               description,
               number,
               raw_data_url
               ):

        # pylint: disable=too-many-arguments
        # require these arguments to create a bueprint

        uri = '/blueprint/api/blueprints'
        data = requests.get(raw_data_url)
        data_string = data.text
        payload = {
            'name': bpname,
            'displayName': displayname,
            'description': description,
            'iteration': number,
            'tags': [],
            'content': data_string
        }
        return cls(session._request(f'{session.baseurl}{uri}',
                                    request_method='POST',
                                    payload=payload
                                    ))

    @staticmethod
    def list_provider_resources(session):
        uri = '/blueprint/api/provider-resources'
        return session._request(f'{session.baseurl}{uri}')

    @staticmethod
    def describe_provider_resources(session, id):
        uri = f'/blueprint/api/provider-resources/{id}'
        return session._request(f'{session.baseurl}{uri}')

    @staticmethod
    def delete(session, id):
        uri = f'/blueprint/api/blueprints/{id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )

    @staticmethod
    def request(session,
                id,
                deployment_name,
                project_id,
                blueprint_version=None,
                reason=None,
                description=None,
                deployment_id=None,
                inputs=None,
                plan=False,
                destroy=False
                ):

        # pylint: disable=too-many-arguments
        # require these arguments to submit a blueprint request

        uri = '/blueprint/api/blueprint-requests'
        payload = {
            "deploymentName": deployment_name,
            "deploymentId": deployment_id,
            "reason": reason,
            "description": description,
            "projectId": project_id,
            "plan": plan,
            "destroy": destroy,
            "blueprintId": id,
            "blueprintVersion": blueprint_version,
            "inputs": inputs
        }
        return session._request(f'{session.baseurl}{uri}',
                                request_method='POST',
                                payload=payload
                                )
