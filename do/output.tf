output "public_ip" {
  value = digitalocean_droplet.cauldron.ipv4_address
}
