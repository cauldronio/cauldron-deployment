data "digitalocean_ssh_key" "default" {
  name = var.default_ssh
}

resource "digitalocean_droplet" "cauldron" {
  name               = "cauldron"
  image              = var.do_image
  region             = var.do_region
  size               = var.do_size
  private_networking = true
  tags = [
    "terraform",
    "cauldron",
    var.do_usertag
  ]
  ssh_keys = [
    data.digitalocean_ssh_key.default.id
  ]

  connection {
    type    = "ssh"
    user    = "root"
    host    = digitalocean_droplet.cauldron.ipv4_address
    timeout = "2m"
    agent   = true
  }

  provisioner "remote-exec" {
    inline = [
      # Update system
      "sudo apt -y update",
      "sudo apt -y upgrade",
      # Allow SSH connections to debian user
      "sudo cp -r .ssh/ /home/debian/",
      "sudo chown -R debian /home/debian/.ssh/",
      "sudo chgrp -R debian /home/debian/.ssh/",
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
      # Add debian user to the docker group
      "sudo usermod -aG docker debian",
      # Install DOcker SDK for Python
      "sudo apt install -y python-pip",
      "pip install docker",
      # Install virtualenv
      "sudo apt install -y virtualenv",
      # Increase vm.max_map_count
      "sudo echo \"vm.max_map_count=262144\" > /etc/sysctl.d/local.conf",
      "sudo sysctl -p /etc/sysctl.d/local.conf"
    ]
  }
}
