resource "aws_lightsail_static_ip_attachment" "cauldron" {
  static_ip_name = aws_lightsail_static_ip.cauldron.id
  instance_name  = aws_lightsail_instance.cauldron.id
}

resource "aws_lightsail_static_ip" "cauldron" {
  name = "cauldron-ip"
}

resource "aws_lightsail_instance" "cauldron" {
  name              = "cauldron"
  availability_zone = var.aws_region
  blueprint_id      = var.aws_image
  bundle_id         = var.aws_size
  key_pair_name     = var.ssh_id
  tags = {
    terraform = "",
    cauldron = "",
    (var.aws_usertag) = ""
  }
}
