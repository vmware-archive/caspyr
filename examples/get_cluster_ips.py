import argparse
import os
from caspyr import Session, Machine


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token',
                        required=True,
                        action='store'
                        )
    parser.add_argument('-n', '--cluster_name',
                        required=True,
                        help='The value of the tag assigned to the machine'
                        )
    args = parser.parse_args()
    return args


def get_ips(token, cluster_name):
    s = Session.login(token)
    ips = [Machine.get_ip(s, master['id']) for master in Machine.find_by_tag(s, key=cluster_name, value='master')]
    print(ips)


def main():
    args = getargs()
    get_ips(token=args.token, cluster_name=args.cluster_name)

if __name__ == '__main__':
    main()
