import requests
import argparse
import json
import sys

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

def authenticate(token):
        baseurl = 'https://console.cloud.vmware.com'
        uri = f'/csp/gateway/am/api/auth/api-tokens/authorize?refresh_token={token}'
        headers = {"Content-Type" : "application/json", 'Accept': "application/json"}
        body = {'refresh_token': token}
        try:
            r = requests.post(f'{baseurl}{uri}', headers = headers, data = json.dumps(body))
            r.raise_for_status()
            j=r.json()
            return j['access_token']
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)

def invite_user(bearer, org_id, user):
        baseurl = 'https://console.cloud.vmware.com'
        uri = f'/csp/gateway/am/api/orgs/{org_id}/invitations'
        headers = {"Content-Type" : "application/json", 'Accept': "application/json", "csp-auth-token" : bearer}
        body = {
            "orgRoleName": "org_owner",
            "orgRoleNames": [ "" ],
            "serviceRolesDtos": [ {
                "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/Zy924mE3dwn2ASyVZR0Nn7lupeA_",
                "serviceRoleNames": [ "automationservice:user","automationservice:manager","automationservice:cloud_admin" ]
            },
            {
                "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/ulvqtN4141beCT2oOnbj-wlkzGg_",
                "serviceRoleNames": ["CodeStream:administrator","CodeStream:viewer","CodeStream:developer"]
            },
            {
                "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/Yw-HyBeQzjCXkL2wQSeGwauJ-mA_",
                "serviceRoleNames": ["catalog:admin","catalog:user"]
            } ],
            "usernames": [ user ]
        }
        try:
            r = requests.post(f'{baseurl}{uri}', headers = headers, data = json.dumps(body))
            r.raise_for_status()
            j=r.json()
            print('Invited user',user,'to org',org_id)
            return j
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit(1)

def invite_user_shared_org(bearer, org_id, user):
    baseurl = 'https://console.cloud.vmware.com'
    uri = f'/csp/gateway/am/api/orgs/{org_id}/invitations'
    headers = {"Content-Type" : "application/json", 'Accept': "application/json", "csp-auth-token" : bearer}
    body = {
        "orgRoleName": "org_owner",
        "orgRoleNames": [ "" ],
        "serviceRolesDtos": [ {
            "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/lGonr_lnBHywqKPn32Q8Uf22njY_",
            "serviceRoleNames": ["discovery:user"]
        },
        {
            "serviceDefinitionLink": "/csp/gateway/slc/api/definitions/external/7cJ2ngS_hRCY_bIbWucM4KWQwOo_",
            "serviceRoleNames": ["log-intelligence:admin","log-intelligence:user"]
        } ],
        "usernames": [ user ]
    }
    try:
        r = requests.post(f'{baseurl}{uri}', headers = headers, data = json.dumps(body))
        r.raise_for_status()
        j=r.json()
        print('Invited user',user,'to org',org_id)
        return j
    except requests.exceptions.HTTPError as e:
        print(e)
        sys.exit(1)

def remove_user(bearer, org_id, user):
    baseurl = 'https://console.cloud.vmware.com'
    uri = f'/csp/gateway/am/api/orgs/{org_id}/users'
    headers = {"Content-Type" : "application/json", 'Accept': "application/json", "csp-auth-token" : bearer}
    body = {
        "emails": [
            user
        ]
    }
    try:
        r = requests.patch(f'{baseurl}{uri}', headers = headers, data = json.dumps(body))
        r.raise_for_status()
        j=r.json()
        print('Removed user',user,'from org',org_id)
        return j
    except requests.exceptions.HTTPError as e:
        print(e)
        sys.exit(1)

def main():
    args = getargs()
    if args.remove is None:
        print('Inviting user',args.user,'to org',args.org_id)
        invite_user(authenticate(args.token), args.org_id, args.user)
        print('Inviting user',args.user,'to shared org',args.shared_org_id)
        invite_user_shared_org(authenticate(args.shared_org_token), args.shared_org_id, args.user)
    else:
        print('Removing user',args.user,'from org',args.org_id)
        remove_user(authenticate(args.token), args.org_id, args.user)
        print('Removing user',args.user,'from shared org',args.shared_org_id)
        remove_user(authenticate(args.shared_org_token), args.shared_org_id, args.user)

if __name__ == '__main__':
    main()