# zabbix-iaac

This repository contains an Ansible playbook for automating the installation and configuration of Zabbix monitoring system on a local server.

## Overview

The playbook automates the following tasks:

- Installing Python dependencies
- Installing system dependencies
- Installing Zabbix server and components
- Setting up the database for Zabbix
- Configuring and starting Zabbix services

Additionally, there's a separate playbook for downloading and installing Ansible collections required for Zabbix in an offline environment.

## Repository Structure

```
zabbix_playbook/
├── inventory/
│   └── hosts                # Inventory file defining target hosts
├── roles/
│   ├── python_dependencies/ # Role for installing Python dependencies
│   ├── system_dependencies/ # Role for installing system dependencies
│   ├── zabbix_install/      # Role for installing Zabbix
│   ├── database_setup/      # Role for setting up the database
│   └── services_setup/      # Role for configuring services
├── site.yml                 # Main playbook file
└── zabbix_collection.yml    # Playbook for installing Ansible collections

zabbix_tasks/
├── group_vars/
│   └── all.yml              # Variables for Zabbix API connection
├── inventory/
│   ├── hosts                # Inventory file for target hosts
│   └── zabbix_inventory.py  # Dynamic inventory script for Zabbix
├── library/
│   └── zabbix_add_host.py   # Custom module for adding hosts to Zabbix
├── roles/
│   ├── agent_install/       # Role for installing Zabbix agent
│   └── zabbix_add_host/     # Role for adding hosts to Zabbix
├── site.yml                 # Main playbook for Zabbix tasks
└── restart_zabbix_agent_windows.yml # Playbook for restarting Zabbix agent on Windows
```

## Prerequisites

- Ansible installed on the control node
- Sudo/root access on the target server
- Internet access (or access to the offline repository for the collections)

## Usage

### Running the Main Playbook

To install and configure Zabbix on your local machine:

```bash
cd zabbix_playbook
ansible-playbook -i inventory/hosts site.yml
```

### Installing Ansible Collections (Offline Mode)

If you need to install the required Ansible collections in an offline environment:

```bash
cd zabbix_playbook
ansible-playbook -i inventory/hosts zabbix_collection.yml
```

This will download the collections from a specified repository and install them locally.

## Adding New Hosts to Zabbix Automatically

This repository includes functionality to automatically add new hosts to your Zabbix monitoring system. Here's how to use it:

### 1. Configure Zabbix API Connection

First, set up your Zabbix API connection details in `zabbix_tasks/group_vars/all.yml`:

```yaml
# Copy from all.yml.example and fill in your details
zabbix_url: "http://your-zabbix-server/zabbix"
zabbix_api_user: "Admin"
zabbix_api_password: "your_password"
```

### 2. Define Host Details

Add the new host details to your inventory file (`zabbix_tasks/inventory/hosts`):

```ini
[new_servers]
new-server ansible_host=192.168.1.100

[new_servers:vars]
zabbix_host_groups=["Linux servers"]
zabbix_templates=["Template OS Linux by Zabbix agent"]
zabbix_interface_port=10050
```

### 3. Run the Add Host Playbook

Execute the playbook to add the new host to Zabbix:

```bash
cd zabbix_tasks
ansible-playbook -i inventory/hosts site.yml --tags "add_host"
```

### 4. Using Dynamic Inventory

You can also use the dynamic inventory script to automatically fetch hosts from Zabbix:

```bash
# Make the script executable
chmod +x zabbix_tasks/inventory/zabbix_inventory.py

# Test the dynamic inventory
./zabbix_tasks/inventory/zabbix_inventory.py --list

# Use with a playbook
ansible-playbook -i zabbix_tasks/inventory/zabbix_inventory.py your_playbook.yml
```

### 5. Restarting Zabbix Agent on Windows Hosts

To restart the Zabbix agent on Windows hosts:

```bash
cd zabbix_tasks
ansible-playbook -i inventory/hosts restart_zabbix_agent_windows.yml
```

## Customization

You can customize the installation by modifying the variables in the respective role directories. Each role contains its own set of variables that control its behavior.

## Requirements

- Ansible 2.9 or higher
- Target system: Linux (tested on CentOS/RHEL and Ubuntu)

## Handling Sensitive Information

When working with this repository, please follow these security practices:

1. **Never commit sensitive information**: Passwords, tokens, or IP addresses should not be committed to the repository.
2. **Use example configuration files**: Create example files (like `hosts.example` and `all.yml.example`) that show the structure without real credentials.
3. **Use Ansible Vault**: Encrypt sensitive variables using Ansible Vault.
4. **Add sensitive files to .gitignore**: Make sure sensitive files are listed in the `.gitignore` file.


## Author

Robson
