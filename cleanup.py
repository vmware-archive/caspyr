

import argparse, json, requests
from sample import Session, Blueprint, Deployment, Project

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

def find_requests(bearer):
    print('Finding incomplete provisioning requests')
    reqs = Blueprint.request(bearer)
    detail = Blueprint.request_detail(bearer,reqs)
    data = list()
    for i in detail:
        if i['status'] == 'STARTED':
            data.append(i['id'])
    print(len(data),'incomplete requests found')
    return data

def cleanup_reqs(bearer,reqs):
    stuck = find_requests(bearer)
    if len(stuck) == 0:
        print('No incomplete requests to clean up')
        return()
    else:
        stuck = Blueprint.request_cancel(bearer,reqs)
        while len(stuck) != 0:
            stuck
            print('Cleaning up',length(stuck),'incomplete requests')
            if len(stuck) == 0:
                break
        print('Cleaned up',stuck,'incomplete requests')
        return stuck

def cleanup_deploys(bearer):
    print('Cleaning up deployments')
    deploys = Deployment.list(bearer)
    cleanup = Deployment.delete(bearer,deploys)
    print('Cleaned up',len(deploys),'deployments')
    return cleanup

def cleanup_blueprints(bearer):
    print('Cleaning up blueprints')
    bps = Blueprint.list(bearer, 'pt')
    values = list()
    for bp in bps:
        values.append(bp)
    cleanup = Blueprint.delete(bearer, values)

def cleanup_projects(bearer):
    print('Cleaning up projects')
    pjs = Project.list(bearer)
    cleanup = Project.delete(bearer,pjs)
    print(cleanup)

def cleanup_cloudzones(bearer):
    print('Cleaning up Cloud Zones')
    projects
    czs = CloudZone.list(bearer)


def main():
    args = getargs()
    token = args.token
    bearer = authenticate(token)
    reqs = find_requests(bearer)
    cleanup_reqs(bearer,reqs)
    cleanup_deploys(bearer)
    cleanup_blueprints(bearer)
    cleanup_projects(bearer)




    """
    with open('sample/resources/hol_details.json') as f:
        data = json.load(f)
        print(data['HOL-1902-T1']['token'])
    f.closed
 

    vmcs = Session.login(refresh_token)
    request = Blueprint.request(vmcs)
    detail = Blueprint.request_detail(vmcs,request)
    data = list()
    for i in detail:
        if i['status'] == 'STARTED':
            data.append(i['id'])
    cancel = Blueprint.request_cancel(vmcs,data)
    deploys = Deployment.list(vmcs)

#    bps = Blueprint.list(vmcs)
#    Blueprint.delete(vmcs,bps)
    #print(data)
            #cancel = Blueprint.request_cancel(i['id'])
    #detail = Blueprint.request_detail(vmcs, request)
    #deployments = Deployment.list(vmcs)
    #cleanUp = Deployment.delete(vmcs,deployments)
    #for deployment in deployments['results']:
    #    print("Found deployment",deployment.name)
    #bps = Blueprints.list(vmcs)
    #bp = 'fc38ae3f99ad047556a2e11de6264'
    #delete = Blueprints.delete(vmcs, bps)
    """

if __name__ == '__main__':
    main()