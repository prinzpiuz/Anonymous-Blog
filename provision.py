

import sys
import time
import requests

api_token = 'd073ebb787d57edfb03978525927cc41fac6f4bcbb0bedb65ae54fc3c6c6e482'
api_url_base = 'https://api.digitalocean.com/v2/'
filename = "id_rsa.pub"
with open(filename, 'r') as f:
    ssh_key = f.readline()

# ssh_key = {'name': sys.argv[1], 'public_key': ssh_key}
headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}


def create(name):
    data = {
            "name": name,
            "region": "blr1",
            "size": "s-1vcpu-1gb",
            "image": "ubuntu-16-04-x64",
            "ssh_keys": None,
            "backups": False,
            "ipv6": True,
            "user_data": None,
            "private_networking": None,
            "volumes": None,
            "tags": [
                name
            ]
        }
    api_url = '{0}droplets'.format(api_url_base)
    print(api_url)
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        print((response.content.decode('utf-8')))
    else:
        print("sorry")

def list(name):
    api_url = api_url_base+'droplets?tag_name='+name
    print(api_url)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        print((response.content.decode('utf-8')))
    else:
        print("sorry")

def delete(name):
    api_url = api_url_base+'droplets?tag_name='+name
    print(api_url)
    response = requests.delete(api_url, headers=headers)



if (sys.argv[1] == 'create'):
    name = sys.argv[2]
    create(name)
elif(sys.argv[1] == 'list'):
    name = sys.argv[2]
    list(name)
elif(sys.argv[1] == 'delete'):
    name = sys.argv[2]
    delete(name)

