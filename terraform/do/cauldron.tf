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
  ssh_keys = var.ssh_fingerprints
}
