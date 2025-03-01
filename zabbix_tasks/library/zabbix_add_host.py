#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from zabbix_utils import ZabbixAPI

def create_or_update_host(module):
    zabbix_url = module.params['zabbix_url']
    api_token = module.params['api_token']
    host_name = module.params['host_name']
    ip_address = module.params['ip_address']
    group_name = module.params['group_name']
    template_ids = module.params['template_ids']

    try:
        api = ZabbixAPI(url=zabbix_url, token=api_token)

        existing_groups = api.hostgroup.get(filter={"name": group_name})
        if existing_groups:
            group_id = existing_groups[0]['groupid']
        else:
            new_group = api.hostgroup.create(name=group_name)
            group_id = new_group['groupids'][0]

        interface = {
            "type": 1,
            "main": 1,
            "useip": 1,
            "ip": ip_address,
            "dns": "",
            "port": "10050"
        }

        # Converta os `template_ids` para números inteiros
        # Converta os `template_ids` para números inteiros de forma robusta
        templates = [{"templateid": int(str(templateid).strip())} for templateid in template_ids]
 
        create_host = api.host.create(
            host=host_name,
            interfaces=[interface],
            groups=[{"groupid": group_id}],
            templates=templates,
            inventory_mode=1
        )

        module.exit_json(changed=True, msg="Host criado com sucesso!", host=create_host)

    except Exception as e:
        module.fail_json(msg=f"Erro ao criar ou atualizar o host: {str(e)}")

def main():
    module = AnsibleModule(
        argument_spec=dict(
            zabbix_url=dict(required=True, type='str'),
            api_token=dict(required=True, type='str'),
            host_name=dict(required=True, type='str'),
            ip_address=dict(required=True, type='str'),
            group_name=dict(required=True, type='str'),
            template_ids=dict(required=True, type='list')
        )
    )

    create_or_update_host(module)

if __name__ == '__main__':
    main()

