resource "digitalocean_droplet" "elasticsearch" {
  name               = "elasticsearch"
  image              = var.do_image
  region             = var.do_region
  size               = var.do_size
  private_networking = true
  tags = [
    "terraform",
    "cauldron",
    "elasticsearch",
    var.do_usertag
  ]
  ssh_keys = var.ssh_fingerprints

  connection {
    type    = "ssh"
    user    = "root"
    host    = digitalocean_droplet.elasticsearch.ipv4_address
    timeout = "2m"
    agent   = true
  }

  provisioner "remote-exec" {
    inline = [
      # Update system
      "sudo apt -y update",
      "sudo apt -y upgrade",
      # Create cauldron user
      "sudo useradd -m -s /bin/bash cauldron",
      # Allow SSH connections to cauldron user
      "sudo cp -r .ssh/ /home/cauldron/",
      "sudo chown -R cauldron /home/cauldron/.ssh/",
      "sudo chgrp -R cauldron /home/cauldron/.ssh/",
      # Install some prerequisite packages that allow apt to use packages via HTTPS
      "sudo apt install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common",
      # Add the GPG key for the official Docker repository
      "curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -",
      # Add Docker repository to APT sources
      "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable\"",
      # Remove the name caching servie
      "sudo apt remove -y unscd",
      # Install Docker
      "sudo apt -y update",
      "sudo apt -y install docker-ce",
      # Add cauldron user to the docker group
      "sudo usermod -aG docker cauldron",
      # Install Docker SDK for Python 3
      "sudo apt install -y python3-pip",
      "pip3 install docker",
      # Install rsync
      "sudo apt install -y rsync",
      # Install virtualenv
      "sudo apt install -y virtualenv",
      # Increase vm.max_map_count
      "sudo echo \"vm.max_map_count=262144\" > /etc/sysctl.d/local.conf",
      "sudo sysctl -p /etc/sysctl.d/local.conf"
    ]
  }
}
