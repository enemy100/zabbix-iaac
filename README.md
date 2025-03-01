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

## License

[Specify your license here]

## Author

Robson
