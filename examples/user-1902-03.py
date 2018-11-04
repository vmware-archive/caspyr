from caspyr import Session, User, Region
from caspyr import CloudAccountAws, CloudAccountAzure, CloudAccount
from caspyr import CloudZone, ImageMapping, FlavorMapping
from caspyr import NetworkProfile, StorageProfileAWS, StorageProfileAzure, StorageProfile
from caspyr import Project, Request, Deployment, Blueprint, Machine
import requests
import argparse
import json
import time
import os

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token',
                        required=True,
                        action='store'
    )
    parser.add_argument('-o', '--org_id',
                        required=True,
                        action='store'
    )
    parser.add_argument('-u', '--user',
                        required=True,
                        action='store'
    )
    parser.add_argument('-s', '--shared_org_id',
                        required=True,
                        action='store'
    )
    parser.add_argument('-p', '--shared_org_token',
                        required=True,
                        action='store'
    )
    parser.add_argument('-r', '--remove',
                        required=False,
                        help='value 1 will remove user'
    )
    args = parser.parse_args()
    return args

def get_details(api_token):
    details = 'hol_secrets.json'
    with open(details) as f:
        j = json.load(f)
        for i in j:
            if i['token'] == api_token:
                return i
        f.closed


def send_slack_notification(payload):
    requests.post(url=os.getenv('slack_hook'), json=payload)

def send_wavefront_metric(metric):
    pass

def invite_user(session,
                user,
                api_token,
                org_id,
                cloud_assembly=False,
                code_stream=False,
                service_broker=False,
                log_intelligence=False,
                discovery=True):

    User.invite(session,
                id=org_id,
                usernames=[user],
                cloud_assembly=cloud_assembly,
                code_stream=code_stream,
                service_broker=service_broker,
                log_intelligence=log_intelligence,
                discovery=discovery)

def remove_user(session, org_id, username):
    User.remove(session,
                id=org_id,
                username=username
                )

def cancel_active_requests(session):
    while len(Request.list_incomplete(session)) > 0:
        for i in Request.list_incomplete(session):
            Request.cancel(session, i['id'])
            time.sleep(10)
    return

def delete_deployments(session):
    while len(Deployment.list(session)) > 0:
        for i in Deployment.list(session):
            Deployment.delete(session, i['id'])
    return

def delete_blueprints(session):
    while len(Blueprint.list(session)) > 0:
        for i in Blueprint.list(session):
            Blueprint.delete(session, i['id'])
    return

def delete_image_mappings(session):
    while len(ImageMapping.list(session)) > 0:
        for i in ImageMapping.list(session):
            ImageMapping.delete(session, i['id'])
    return

def delete_flavor_mapping(session):
    while len(FlavorMapping.list(session)) > 0:
        for i in FlavorMapping.list(session):
            FlavorMapping.delete(session, i['id'])
    return

def delete_storage_profile(session):
    while len(StorageProfile.list(session)) > 0:
        for i in StorageProfile.list(session):
            StorageProfile.delete(session, i['id'])
    return

def delete_network_profile(session):
    while len(NetworkProfile.list(session)) > 0:
        for i in NetworkProfile.list(session):
            NetworkProfile.delete(session, i['id'])
    return

def delete_orphaned_machines(session):
    while len(Machine.list_orphaned(session)) > 0:
        for i in Machine.list_orphaned(session):
            Machine.delete(session, i['id'])
    return

def delete_project(session):
    while len(Project.list(session)) > 0:
        for i in Project.list(session):
            Project.removezones(session, i['id'])
            time.sleep(5)
            Project.delete(session, i['id'])
    return

def delete_cloudzones(session):
    while len(CloudZone.list(session)) > 0:
        for i in CloudZone.list(session):
            CloudZone.delete(session, i['id'])
    return

def delete_cloudaccounts(session):
    while len(CloudAccount.list(session)) > 0:
        for i in CloudAccount.list(session):
            CloudAccount.unregister(session, i['id'])
            CloudAccount.delete(session, i['id'])
    return

def cleanup(session, data, username):
    org_name = data['name']
    org_id = data['org_id']
    cancel_active_requests(session)
    delete_deployments(session)
    delete_blueprints(session)
    delete_image_mappings(session)
    delete_flavor_mapping(session)
    delete_network_profile(session)
    delete_storage_profile(session)
    delete_orphaned_machines(session)
    delete_project(session)
    delete_cloudzones(session)
    delete_cloudaccounts(session)
    remove_user(session, org_id, username)
    info = ""
    info +=(f'*Cleanup on {org_name} completed.* \n')
    info +=(f'{len(Deployment.list(session))} deployments remaining. \n')
    info +=(f'{len(Blueprint.list(session))} blueprints remaining. \n')
    info +=(f'{len(ImageMapping.list(session))} image mappings remaining. \n')
    info +=(f'{len(FlavorMapping.list(session))} flavor mappings remaining. \n')
    info +=(f'{len(StorageProfile.list(session))} storage profiles remaining. \n')
    info +=(f'{len(Project.list(session))} projects remaining. \n')
    info +=(f'{len(CloudZone.list(session))} cloud zones remaining. \n')
    info +=(f'{len(CloudAccount.list(session))} cloud accounts remaining. \n')
    info +=(f'User {username} removed.')
    payload = { "text": info }
    send_slack_notification(payload)


def setup_org(session, data):
    i = CloudAccountAws.create(session,
                               name = 'Trading AWS',
                               access_key = data['aws_access_key'],
                               secret_key = data['aws_secret_key']
                              )
    CloudZone.create(session,
                     name = 'dev aws',
                     region_id = os.path.split(i._links['regions']['hrefs'][0])[1],
                     tags = [{ "key": "platform", "value": "aws" }]
                    )

    i = CloudAccountAzure.create(session,
                                 name = 'Trading Azure',
                                 subscription_id = data['azure_subscription_id'],
                                 tenant_id = data['azure_tenant_id'],
                                 application_id = data['azure_application_id'],
                                 application_key = data['azure_application_key']
                                )
    CloudZone.create(session,
                     name = 'dev aws',
                     region_id = os.path.split(i._links['regions']['hrefs'][0])[1],
                     tags = [{ "key": "platform", "value": "aws" }]
                     )


def main():
    args = getargs()
    session = Session.login(args.token)
    data = get_details(args.token)

    if args.remove is None:
        payload = { "text": f"*Inviting user {args.user} to org {data['name']}.*" }
        send_slack_notification(payload)
        invite_user(session = Session.login(args.token),
                    user=args.user,
                    api_token=args.token,
                    org_id=args.org_id,
                    cloud_assembly=True,
                    code_stream=True,
                    service_broker=True)

        invite_user(session = Session.login(args.shared_org_token),
                    user=args.user,
                    api_token=args.shared_org_token,
                    org_id=args.shared_org_id,
                    log_intelligence=True)

        setup_org(session, data)

    else:
        cleanup(session,
                username = args.user,
                data = data)

if __name__ == '__main__':
    main()