# Cloud Automation Services SDK for Python
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.

# SPDX-License-Identifier: Apache-2.0

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
        try:
            self.validation_messages = blueprint['validationMessages']
        except:
            KeyError
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
        j = session._request(f'{session.baseurl}{uri}')
        return j['objects']

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
        return cls(session._request(f'{session.baseurl}{uri}')[''])

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
    def create(cls,
               session,
               project_id,
               bp_name,
               description,
               version,
               content
               ):
        """Creates a blueprint from a valid YAML input.

        :param session: The session object.
        :type session: object
        :param project_id: The unique ID of the project in which to place
        this blueprint.
        :type project_id: str
        :param bp_name: The name of the blueprint.
        :type bp_name: str
        :param description: A description of what the blueprint is/does.
        :type description: str
        :param version: The version of the blueprint you are passing.
        :type version: str
        :param content: Valid blueprint YAML, should be enclosed in double
        quotes.
        :type content: str
        :return: blueprint
        :rtype: object
        """
        # pylint: disable=too-many-arguments
        # require these arguments to create a blueprint

        uri = '/blueprint/api/blueprints'
        payload = {
            'projectId': project_id,
            'name': bp_name,
            'description': description,
            'tags': [],
            'content': content,
            'version': version
        }
        i = session._request(f'{session.baseurl}{uri}',
                             request_method='POST',
                             payload=payload
                             )
        return cls.describe(session,
                            blueprint_id=i['id']
                            )

    @staticmethod
    def list_provider_resources(session):
        """Returns a list of provider types.

        :param session: The session object.
        :type session: obj
        :return: A list of provider types and metadata.
        :rtype: list
        """

        uri = '/blueprint/api/provider-resources'
        return session._request(f'{session.baseurl}{uri}')['objects']

    @staticmethod
    def describe_provider_resources(session, provider_resource_id):
        """Returns the detailed schema of a given provider resource.

        :param session: The session object.
        :type session: obj
        :param provider_resource_id: The unique id of the provider resource
        you want to query.
        :type provider_resource_id: str
        :return: Returns the schema of the provider resource as a json object.
        :rtype: obj
        """

        uri = f'/blueprint/api/provider-resources/{provider_resource_id}'
        return session._request(f'{session.baseurl}{uri}')

    @staticmethod
    def delete(session, blueprint_id):
        """Deletes a blueprint from the system.

        :param session: The session object.
        :type session: object
        :param blueprint_id: The unique blueprint id.
        :type blueprint_id: str
        :return: Returns the HTTP status code.
        :rtype: int
        """

        uri = f'/blueprint/api/blueprints/{blueprint_id}'
        return session._request(f'{session.baseurl}{uri}',
                                request_method='DELETE'
                                )

    @staticmethod
    def request(session,
                blueprint_id,
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
        """Requests a blueprint through Cloud Assembly.

        :param session: The session object.
        :type session: object
        :param blueprint_id: The unique id of the blueprint to request.
        :type blueprint_id: str
        :param deployment_name: The name of the resulting deployment from the
        blueprint request.
        :type deployment_name: str
        :param project_id: The unique project id that you are making the
        request from.
        :type project_id: str
        :param blueprint_version: The version of the blueprint to request,
        defaults to None which uses the current draft.
        :type blueprint_version: str, optional.
        :param reason: The reason for the new request, defaults to None.
        :type reason: str, optional.
        :param description: A description for the deployment that will show on
        the deployments page, defaults to None.
        :type description: str, optional.
        :param deployment_id: The unique id of the deployment to iterate on.
        Only used when updating an existing deployment, defaults to None.
        :type deployment_id: str, optional.
        :param inputs: Input values to pass as part of the request, defaults
        to None.
        :type inputs: obj, optional.
        :param plan: Simulate the request and check what resources will be
        created, modified or deleted. Defaults to False.
        :type plan: bool, optional
        :param destroy: Used to destroy an existing deployment, defaults to
        False.
        :type destroy: bool, optional.
        :return: blueprint
        :rtype: obj
        """

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
            "blueprintId": blueprint_id,
            "blueprintVersion": blueprint_version,
            "inputs": inputs
        }
        return session._request(f'{session.baseurl}{uri}',
                                request_method='POST',
                                payload=payload
                                )
