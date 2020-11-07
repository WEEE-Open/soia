# -*- mode: ruby -*-
# vi: set ft=ruby :

# Greeting message displayed after vagrant up

# Vagrantfile config version 2
Vagrant.configure("2") do |config|
  # Use a CENTOS 8 Linux environment
  config.vm.box = "geerlingguy/centos8"
  config.vm.hostname = "ldap"

  # Disable the default vagrant share
  config.vm.synced_folder ".", "/vagrant", type: "rsync", disabled: true

  # Forward LDAP port
  config.vm.usable_port_range = 3800..3900
  config.vm.network "forwarded_port", guest: 389, host: 3890, protocol: "tcp", auto_correct: true

  # Use VirtualBox
  config.vm.provider "virtualbox" do |vb|
    vb.name = "VAGRANT LDAP Test server 8"

    # Allocate 4GB to VB
    vb.memory = 4096

    # Allocate 4 V-Cores to VB
    vb.cpus = 4
  end

  # Ansible provisioning at first startup
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/playbook.yml"
  end

  # Setup the greeting message
  config.vm.post_up_message = <<-END
  Your LDAP instance started successfully!
  The LDAP server is accessible at local host with a port in the range [3800 - 3900].
  The default port used is the 3890, however if a port collision is detected vagrant will assign another port.
  To find out which port is being effectively used, run the command "vagrant port" and look for port 389 on the guest.
  END
end
