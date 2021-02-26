variable "domain_fqdn" {
  type        = string
  description = "The FQDN of the domain"
  default     = "cauldron.io"
}

variable "record_name" {
  type        = string
  description = "The name of the record"
  default     = "botergia"
}

variable "record_type" {
  type        = string
  description = "The type of the record"
  default     = "A"
}

variable "record_ttl" {
  type        = number
  description = "The TTL of the record"
  default     = 600
}

variable "record_values" {
  type        = list(string)
  description = "A list of the values of the record"
  default     = ["127.0.0.1"]
}
