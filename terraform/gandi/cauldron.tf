resource "gandi_livedns_record" "cauldron" {
    zone    = var.domain_fqdn
    name    = var.record_name
    type    = var.record_type
    ttl     = var.record_ttl
    values  = var.record_values
}
