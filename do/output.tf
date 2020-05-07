output "cauldron_public_ip" {
  value = digitalocean_droplet.cauldron.ipv4_address
}

output "cauldron_private_ip" {
  value = digitalocean_droplet.cauldron.ipv4_address_private
}

output "elastic_public_ip" {
  value = digitalocean_droplet.elasticsearch.ipv4_address
}

output "elastic_private_ip" {
  value = digitalocean_droplet.elasticsearch.ipv4_address_private
}

output "database_public_ip" {
  value = digitalocean_droplet.database.ipv4_address
}

output "database_private_ip" {
  value = digitalocean_droplet.database.ipv4_address_private
}
