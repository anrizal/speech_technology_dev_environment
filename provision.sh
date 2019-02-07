#!/bin/sh

##### INFO #####

# provision.sh
#
# This script will start provision a clean Ubuntu 16.04 LTS 64bit Vagrant box
# using ansible to be used for Factory Development
#
# Author: Arradi Nur Rizal

#============================= Preconfiguration ================================
export DEBIAN_FRONTEND=noninteractive

#============================= Installing ansible ===================================
if [ ! -f /usr/bin/ansible-playbook ]
    then
    apt-get install software-properties-common
    apt-add-repository ppa:ansible/ansible
    apt-get update
    apt-get install -y ansible
fi

#============================= Running ansible playbook ===================================

ansible-playbook --inventory="localhost," -c local  /provision/ansible/main.yml