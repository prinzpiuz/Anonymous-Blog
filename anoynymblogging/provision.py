"""Usage.

Usage:
  provision.py create <name> <tag>
  provision.py list <tag>
  provision.py delete <tag>

Options:
  -h --help     Show this screen.

"""

import sys
import requests
from docopt import docopt
import json
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)
# reading .env file
environ.Env.read_env()

api_token = env('DO_TOKEN')
api_url_base = 'https://api.digitalocean.com/v2/'

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}


def create(args):
    name = args['<name>']
    tag = args['<tag>']
    print(name)
    print(tag)
    data = {
        "name": name,
        "region": "blr1",
        "size": "s-1vcpu-1gb",
        "image": "ubuntu-16-04-x64",
        "ssh_keys": [23341811],
        "backups": False,
        "ipv6": True,
        "user_data": None,
        "private_networking": None,
        "volumes": None,
        "tags": [
            "name" + tag
        ]
    }
    api_url = '{0}droplets'.format(api_url_base)
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 202:
        data = json.loads(response.text)
        print("sucess")
        return {'id': ((data.get("droplet")).get("id")), 'status': ((data.get("droplet")).get("status"))}
    else:
        print("sorry")


def list(tag):
    api_url = api_url_base + 'droplets?tag_name=' + tag
    print(api_url)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 202:
        print((response.content.decode('utf-8')))
    else:
        print("sorry")


def delete(tag):
    api_url = api_url_base + 'droplets?tag_name=' + tag
    requests.delete(api_url, headers=headers)
    print("done")


if __name__ == '__main__':
    arguments = docopt(__doc__)

    if arguments['create']:
        r = create(arguments)
        print(r)
    elif arguments['list']:
        list(arguments['<tag>'])
    elif arguments['delete']:
        delete(arguments['<tag>'])
