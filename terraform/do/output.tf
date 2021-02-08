output "cauldron_public_ip" {
  value = digitalocean_droplet.cauldron.ipv4_address
}

output "cauldron_private_ip" {
  value = digitalocean_droplet.cauldron.ipv4_address_private
}
