#!/bin/bash

# Define o diretório de destino
DEST_DIR="/opt/server_deploy"

# URL do pacote ansible-core
ANSIBLE_CORE_URL="http://10.196.182.20/repo/ansible/ansible-core-2.14.17-1.el9.x86_64.rpm"

# URL da coleção community.mysql (se necessário, ajuste para o seu servidor interno)
MYSQL_COLLECTION_URL="http://10.196.182.20/repo/ansible/community-mysql-3.11.0.tar.gz"

# Verifica se o script está sendo executado como root
if [ "$EUID" -ne 0 ]; then
  echo "Por favor, execute como root."
  exit 1
fi

# Cria o diretório de destino se ele não existir
echo "Criando o diretório $DEST_DIR..."
mkdir -p "$DEST_DIR"

# Verifica se o diretório está vazio
if [ "$(ls -A $DEST_DIR)" ]; then
  echo "O diretório $DEST_DIR já existe e não está vazio. Saindo."
  exit 1
fi

# Define os pacotes a serem instalados via dnf
deps=("python3-packaging" \
      "python3-resolvelib" \
      "git-core" \
      "python3-cryptography" \
      "sshpass")

# Instala os pacotes usando dnf
echo "Instalando pacotes via dnf..."
for dep in "${deps[@]}"; do
  echo "Instalando $dep..."
  dnf install -y "$dep" || { echo "Erro ao instalar $dep. Saindo."; exit 1; }
done

# Baixa e instala o pacote ansible-core
echo "Baixando e instalando o ansible-core..."
wget -O /tmp/ansible-core.rpm "$ANSIBLE_CORE_URL" || { echo "Erro ao baixar o ansible-core. Saindo."; exit 1; }
rpm -Uvh /tmp/ansible-core.rpm || { echo "Erro ao instalar o ansible-core. Saindo."; exit 1; }

# Baixa e instala a coleção community.mysql
echo "Baixando e instalando a coleção community.mysql..."
wget -O /tmp/community-mysql.tar.gz "$MYSQL_COLLECTION_URL" || { echo "Erro ao baixar a coleção community.mysql. Saindo."; exit 1; }
ansible-galaxy collection install /tmp/community-mysql.tar.gz || { echo "Erro ao instalar a coleção community.mysql. Saindo."; exit 1; }

# Define permissões no diretório
echo "Configurando permissões..."
chown -R root:root "$DEST_DIR"
chmod -R 755 "$DEST_DIR"

echo "Instalação concluída. Execute o playbook Ansible em /opt/server_deploy/deploy/ansible/!"

