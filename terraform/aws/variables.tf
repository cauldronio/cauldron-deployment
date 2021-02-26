variable "aws_usertag" {
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

variable "ssh_id" {
  type        = string
  description = "Your SSH key ID"
  default     = "default"
  # Available SSH IDs can be listed using
  # aws lightsail get-key-pairs | json_pp | grep name
}

variable "aws_size" {
  type        = string
  description = "AWS default instance size"
  default     = "nano_2_0"
  # Available sizes can be listed using
  # aws lightsail get-bundles | json_pp | grep bundleId
}

variable "aws_region" {
  type        = string
  description = "AWS default region"
  default     = "eu-west-3a"
  # Available regions can be listed using
  # aws lightsail get-regions | json_pp | grep name
}

variable "aws_image" {
  type        = string
  description = "AWS default OS distribution image"
  default     = "debian_10"
  # Available images can be listed using
  # aws lightsail get-blueprints | json_pp | grep blueprintId
}
