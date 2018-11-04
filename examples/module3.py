from caspyr import Session, User, Region
from caspyr import CloudAccountAws, CloudAccountAzure, CloudAccount, CloudAccountvSphere, CloudAccountNSXT
from caspyr import CloudZone, ImageMapping, FlavorMapping
from caspyr import NetworkProfile, StorageProfileAWS, StorageProfileAzure, StorageProfile
from caspyr import Project, Request, Deployment, Blueprint, Machine, DataCollector
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
    args = parser.parse_args()
    return args

def get_datacollector(session):
    return DataCollector.list(session)[0]

def create_nsxtaccount(session, data_collector):
    return CloudAccountNSXT.create(session,
                                   name = 'nsxmgr-01a.corp.local',
                                   fqdn = 'nsxmgr-01a.corp.local',
                                   rdc = data_collector,
                                   username = 'admin',
                                   password = 'VMware1!',
                                   )


def create_vsphereaccount(session, nsx_account):
    return CloudAccountvSphere.create(session,
                                      name = 'Trading vSphere',
                                      fqdn = 'vcsa-01a.corp.local',
                                      rdc = get_datacollector(session),
                                      username = 'administrator@corp.local',
                                      password = 'VMware1!',
                                      datacenter_moid = 'Datacenter:datacenter-21',
                                      nsx_cloud_account= nsx_account,
                                      )

def setup_org(session):
    dc = get_datacollector(session)
    create_nsxtaccount(session, dc['id'])




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

    setup_org(session)

if __name__ == '__main__':
    main()