variable "do_usertag" {
  type        = string
  description = "Tag of the user doing the deployment"
  default     = "automation"
}

variable "pub_key" {
  type        = string
  description = "The path to your public SSH key"
  default     = "~/.ssh/id_rsa.pub"
}

variable "pvt_key" {
  type        = string
  description = "The path to your private SSH key"
  default     = "~/.ssh/id_rsa"
}

variable "ssh_fingerprints" {
  type        = list(string)
  description = "Your SSH key fingerprints"
  default     = []
}

variable "do_size" {
  type        = string
  description = "DigitalOcean default droplet size"
  default     = "s-6vcpu-16gb"
}

variable "do_region" {
  type        = string
  description = "DigitalOcean default region"
  default     = "fra1"
}

variable "do_image" {
  type        = string
  description = "DigitalOcean default OS distribution image"
  default     = "debian-10-x64"
  # Available images at
  # curl -XGET -H "Content-Type: application/json" \
  # -H "Authorization: Bearer $DIGITALOCEAN_TOKEN" \
  # "https://api.digitalocean.com/v2/images?type=distribution" | json_pp | grep slug
}
