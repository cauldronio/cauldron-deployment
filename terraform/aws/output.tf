output "cauldron_public_ip" {
  value = aws_lightsail_static_ip.cauldron.ip_address
}
