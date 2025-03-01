#!/usr/bin/env python3
import json
import requests

ZABBIX_API_URL = "http://10.196.182.21/zabbix/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASSWORD = "zabbix"

def get_token():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {"user": ZABBIX_USER, "password": ZABBIX_PASSWORD},
        "id": 1,
        "auth": None
    }
    response = requests.post(ZABBIX_API_URL, json=payload)
    return response.json()["result"]

def get_hosts():
    token = get_token()
    payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {"output": ["host", "interfaces"]},
        "auth": token,
        "id": 2
    }
    response = requests.post(ZABBIX_API_URL, json=payload)
    hosts = response.json()["result"]

    inventory = {"_meta": {"hostvars": {}}}
    for host in hosts:
        hostname = host["host"]
        ip = host["interfaces"][0]["ip"]
        inventory["_meta"]["hostvars"][hostname] = {"ansible_host": ip}

    return inventory

print(json.dumps(get_hosts(), indent=4))

