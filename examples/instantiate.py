import argparse, json, os
from sample import Session, Blueprint, Deployment, Project, CloudZone, NetworkProfile, DataCollector, StorageProfile, ImageMapping, CloudAccount



def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token',
                        required=True,
                        action='store',
                        help='Viewable under USER SETTINGS > View My Profile > Access Key.')
    args = parser.parse_args()
    return args

def create_cloudzone(bearer, name, ca):
    j = ca['enabledRegionLinks']
    for i in j:
        r = os.path.split(i)[1]
    CloudZone.create(bearer, name, r)

def main():
    args = getargs()
    bearer = Session.login(args.token)

    # Create AWS Cloud Account and Cloud Zone
    ca = CloudAccount.createAWS(bearer, 'trading aws', access_key ,secret_key)
    create_cloudzone (bearer, 'dev aws', ca)

    # Create Azure Cloud Account and Cloud Zone
    ca = CloudAccount.createAzure(bearer, 'trading azure', subscription_id, tenant_id, application_id, application_key)
    print(ca)
    create_cloudzone (bearer, 'dev azure', ca)


if __name__ == '__main__':
    main()