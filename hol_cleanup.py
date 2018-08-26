#!/usr/bin/env python3

from sample import Session, Blueprint, Deployment, FlavorMapping, ImageMapping, StorageProfile, NetworkProfile, CloudZone, Project, CloudAccount, DataCollector, Project, CodeStream, ServiceBroker
import argparse, json, os

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token',
                        required=True,
                        action='store',
                        help='Viewable under USER SETTINGS > View My Profile > Access Key.')
    args = parser.parse_args()
    return args

def authenticate(token):
    print('Authenticating session')
    bearer = Session.login(token)
    return bearer

def list_requests(bearer):
    """
    Return all requests.
    """
    print('Looking for requests.')
    r = Blueprint.request(bearer)
    print(len(r),'requests found.')
    return r

def incomplete_requests(bearer, id):
    print('Checking requests status.')
    data = list()
    for i in id:
        j = Blueprint.request_detail(bearer, i)
        if j['status'] == 'STARTED':
            data.append(j['id'])
    print(len(data),'incomplete requests found')
    return data

def cancel_requests(bearer, id):
    print('Cancelling in progress requests.')
    for i in id:
        Blueprint.request_cancel(bearer, i)
    return

def deployments(bearer):
    print('Checking for deployments.')
    print(len(Deployment.list(bearer)),'deployments found')
    return Deployment.list(bearer)

def delete_deployments(bearer, id):
    print('Deleting deployments.')
    for i in id:
        Deployment.delete(bearer, i)
    return

def list_blueprints(bearer):
    print('Checking for blueprints.')
    data = list()
    j = Blueprint.list(bearer)
    for i in j:
        data.append(i)
    print(len(j),'blueprints found.')
    return(data)

def delete_blueprints(bearer, ids):
    print('Deleting blueprints.')
    for i in ids:
        Blueprint.delete(bearer, i)
    return

def list_flavorprofiles(bearer):
    print('Checking for flavor mappings.')
    data = list()
    j = FlavorMapping.list(bearer)
    for i in j:
        data.append(i['id'])
    if len(data) > 0:
        print('Flavor mappings found.')
    return data

def delete_flavorprofile(bearer, id):
    print('Deleting flavor mappings.')
    for i in id:
        FlavorMapping.delete(bearer, i)
    return

def get_imageprofile(bearer):
    print('Checking for image mappings.')
    data = list()
    for i in ImageMapping.list(bearer):
        data.append(i['id'])
    print(len(data),'image mappings found.')
    return data

def delete_imageprofile(bearer, id):
    print('Deleting image mappings.')
    for i in id:
        ImageMapping.delete(bearer, i)
    return

def list_networkprofile(bearer):
    print('Checking for network profiles.')
    data = list()
    j = NetworkProfile.list(bearer)
    for i in j:
        data.append(i['id'])
    print(len(data),'network profiles found.')
    return data

def delete_networkprofile(bearer, ids):
    NetworkProfile.delete(bearer, ids)
    print(len(ids),'network profiles deleted.')

def list_storageprofileaws(bearer):
    print('Checking for aws storage profiles.')
    data = list()
    j = StorageProfile.list_aws(bearer)
    print(j)
    for i in j:
        data.append(i['id'])
    print(len(j),'aws storage profiles found.')
    return data

def list_storageprofileazure(bearer):
    print('Checking for azure storage profiles.')
    data = list()
    j = StorageProfile.list_azure(bearer)
    for i in j:
        data.append(i['id'])
    print(len(j),'azure storage profiles found.')
    return data

def list_storageprofilevsphere(bearer):
    print('Checking for vsphere storage profiles.')
    data = list()
    j = StorageProfile.list_vsphere(bearer)
    for i in j:
        data.append(i['id'])
    print(len(j),'vsphere storage profiles found.')
    return data

def delete_storageprofileaws(bearer, ids):
    print('Deleting aws storage profiles.')
    for i in ids:
        StorageProfile.delete_aws(bearer, i)
    return

def delete_storageprofileazure(bearer, ids):
    print('Deleting aws storage profiles.')
    for i in ids:
        StorageProfile.delete_azure(bearer, i)
    return

def delete_storageprofilevsphere(bearer, ids):
    print('Deleting vsphere storage profiles.')
    for i in ids:
        StorageProfile.delete_vsphere(bearer, i)
    return

def list_project(bearer):
    print('Checking for projects.')
    data = list()
    j = Project.list(bearer)
    for i in j:
        data.append(i['id'])
    print(len(j),'projects found.')
    return data

def remove_projectzones(bearer, ids):
    print('Removing zones from projects.')
    for i in ids:
        Project.removezones(bearer, i)
    return

def list_cloudzone(bearer):
    print('Checking for cloud zones.')
    data = list()
    j = CloudZone.list(bearer)
    for i in j:
        data.append(i['id'])
    print(len(j),'cloud zones found.')
    return data

def delete_cloudzone(bearer, ids):
    print('Deleting cloud zones')
    for i in ids:
        CloudZone.delete(bearer, i)
    return

def delete_project(bearer, ids):
    print('Deleting projects.')
    for i in ids:
        Project.delete(bearer, i)
    return

def list_cloudaccounts(bearer):
    print('Checking for cloud accounts')
    data = list()
    j = CloudAccount.list(bearer)
    for i in j:
        data.append(i)
    print(data)
    return data

def delete_cloudaccounts(bearer, ids):
    print('Deleting cloud accounts')
    for i in ids:
        CloudAccount.delete(bearer, i)
    return

def list_datacollectors(bearer):
    print('Checking for data collectors')
    data = list()
    j = DataCollector.list(bearer)
    for i in j:
        data.append(i)
    return data

def delete_datacollectors(bearer, ids):
    print('Deleting data collectors')
    for i in ids:
        DataCollector.delete(bearer, i)
    return

def get_details(token):
    with open('sample/resources/hol_details.json') as f:
        data = json.load(f)
        for i in data:
            if i['token'] == token:
                return i
        f.closed

def create_cloudzone(bearer, name, ca, tags):
    i = ca['_links']['regions']['hrefs'][0]
    i = os.path.split(i)[1]
    print(i)
    CloudZone.create(bearer, name, i, tags=tags)
    return

def setup_org(bearer, data):
    i = CloudAccount.createAWS(bearer, 'dev aws', data['aws_access_key'], data['aws_secret_key'])
    create_cloudzone(bearer, 'dev aws', i, [{ "key": "platform", "value": "aws" }])
    i = CloudAccount.createAzure(bearer, 'dev azure', data['azure_subscription_id'], data['azure_tenant_id'], data['azure_application_id'], data['azure_application_key'])
    create_cloudzone(bearer, 'dev azure', i, [{ "key": "platform", "value": "azure" }])



def main():
    with open('sample/resources/hol_details.json') as f:
        data = json.load(f)
        for i in data:
            print('Resetting org',i['name'])
            #args = getargs()
            bearer = Session.login(i['token'])

            ids = incomplete_requests(bearer, list_requests(bearer))
            if len(ids) > 0:
                cancel_requests(bearer, ids)

            ids = deployments(bearer)
            if len(ids) > 0:
                delete_deployments(bearer, ids)

            ids = list_flavorprofiles(bearer)
            if len(ids) > 0:
                delete_flavorprofile(bearer, ids)

            ids = get_imageprofile(bearer)
            if len(ids) > 0:
                delete_imageprofile(bearer, ids)

            ids = list_networkprofile(bearer)
            if len(ids) > 0:
                delete_networkprofile(bearer, ids)

            if len(CloudAccount.listaws(bearer)) > 0:
                ids = (list_storageprofileaws(bearer))
                if len(ids) > 0:
                    delete_storageprofileaws(bearer, ids)

            if len(CloudAccount.listazure(bearer)) > 0:
                ids = (list_storageprofileazure(bearer))
                if len(ids) > 0:
                    delete_storageprofileazure(bearer, ids)

            if len(CloudAccount.listvsphere(bearer)) > 0:
                ids = list_storageprofilevsphere(bearer)
                if len(ids) > 0:
                    delete_storageprofilevsphere(bearer, ids)

            ids = list_blueprints(bearer)
            if len(ids) > 0:
                delete_blueprints(bearer, ids)

            ids = list_project(bearer)
            if len(ids) > 0:
                remove_projectzones(bearer, ids)
                delete_project(bearer, ids)

            ids = list_cloudzone(bearer)
            if len(ids) > 0:
                delete_cloudzone(bearer, ids)

            ids = list_cloudaccounts(bearer)
            if len(ids) > 0:
                delete_cloudaccounts(bearer, ids)

            ids = list_datacollectors(bearer)
            if len(ids) > 0:
                delete_datacollectors(bearer, ids)


            print(ServiceBroker.sources_list(bearer))

            setup_org(bearer, (get_details(i['token'])))





if __name__ == '__main__':
    main()