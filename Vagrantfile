
##### INFO #####

# vagrant file
#
# This vagrant file is intended for
# Provider: Virtual Box
# Vagrant: Vagrant 2.2 ++
# Vagrant API: Version 2
# Provision: Shell
# Guest OS: Ubuntu 16.04 LTS 64bit
# For Application: Tensor Flow 2.0
# Author: Arradi Nur Rizal


#=============================CONFIGURATION=================================
#Vagrant API Version
#Currently, there are only two supported versions: "1" and "2".
#Version 1 represents the configuration from Vagrant 1.0.x.
#"2" represents the configuration for 1.1+ leading up to 2.0.x.
VAGRANTFILE_API_VERSION = "2"

# The BOX used is Ubuntu 16.04 LTS 64 bit
BOX = "geerlingguy/ubuntu1604"

# Number of CPU we want to use
CPU = 2

# We set the vm's memory to 1024 MB
MEMORY = "4096"

# Network Settings.
IP = "30.0.10.10"

# Share/synced folder configuration
HOST_FOLDER_PROVISION = "./provision"
GUEST_FOLDER_PROVISION = "/provision"
HOST_FOLDER_PROJECTS = "./projects"
GUEST_FOLDER_PROJECTS = "/projects"
HOST_FOLDER_DATA = "./data"
GUEST_FOLDER_DATA = "/data"

#We use shell for provision
SHELL_PATH = "provision.sh"

#=================================CUSTOM CHECK =================================
module OS
    def OS.windows?
        (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) != nil
    end

    def OS.mac?
        (/darwin/ =~ RUBY_PLATFORM) != nil
    end

    def OS.unix?
        !OS.windows?
    end

    def OS.linux?
        OS.unix? and not OS.mac?
    end
end

#==========================================================================
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. For a detailed explanation
  # and listing of configuration options, please view the documentation
  # online. http://docs.vagrantup.com/v2/

  # The BOX
    config.vm.box = BOX

  # We set the vm's memory, enable ioapic, set natdnsresolver
    config.vm.provider "virtualbox" do |vb|
       vb.customize ["modifyvm", :id, "--memory", MEMORY]
       vb.customize ["modifyvm", :id, "--cpus", CPU]
       vb.customize ["modifyvm", :id, "--ioapic", "on"]
       vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
       vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/data", "1"]
    end    

  # Network Settings. Note, in 1.1++ no host only and no forward port option 
    config.vm.network "private_network", ip: IP

  # Configure shared/synced folder. we do not use NFS for Windows Host

    if OS.windows?
        config.vm.synced_folder HOST_FOLDER_PROVISION, GUEST_FOLDER_PROVISION, :owner=> 'vagrant', :group=>'www-data', type:'smb', mount_options: ['vers=3.0']
        config.vm.synced_folder HOST_FOLDER_PROJECTS, GUEST_FOLDER_PROJECTS, :owner=> 'www-data', :group=>'www-data', type:'smb', mount_options: ['vers=3.0']
        config.vm.synced_folder HOST_FOLDER_DATA, GUEST_FOLDER_DATA, :owner=> 'vagrant', :group=>'www-data', type:'smb', mount_options: ['vers=3.0']
    elsif OS.mac?
        config.vm.synced_folder HOST_FOLDER_PROVISION, GUEST_FOLDER_PROVISION, type:'nfs', mount_options:['actimeo=2']
        config.vm.synced_folder HOST_FOLDER_PROJECTS, GUEST_FOLDER_PROJECTS, type:'nfs', mount_options:['actimeo=2']
        config.vm.synced_folder HOST_FOLDER_DATA, GUEST_FOLDER_DATA, type:'nfs', mount_options:['actimeo=2']
    elsif OS.linux?
        config.vm.synced_folder HOST_FOLDER_PROVISION, GUEST_FOLDER_PROVISION, :nfs=> true, :linux__nfs_options => ['rw','no_subtree_check','all_squash','async']
        config.vm.synced_folder HOST_FOLDER_PROJECTS, GUEST_FOLDER_PROJECTS, :nfs=> true, :linux__nfs_options => ['rw','no_subtree_check','all_squash','async']
        config.vm.synced_folder HOST_FOLDER_DATA, GUEST_FOLDER_DATA, :nfs=> true, :linux__nfs_options => ['rw','no_subtree_check','all_squash','async']
    else
        config.vm.synced_folder HOST_FOLDER_PROVISION, GUEST_FOLDER_PROVISION, :owner=> 'vagrant', :group=>'www-data'
        config.vm.synced_folder HOST_FOLDER_PROJECTS, GUEST_FOLDER_PROJECTS, :owner=> 'vagrant', :group=>'www-data'
        config.vm.synced_folder HOST_FOLDER_DATA, GUEST_FOLDER_DATA, :owner=> 'vagrant', :group=>'www-data'
    end

  # Provision
    config.vm.provision "shell", :path=> SHELL_PATH
end