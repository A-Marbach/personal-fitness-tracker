
variable "ssh_allowed_cidr" {
  description = "Public IPv4 address allowed to access SSH, in CIDR notation"
  type        = string
  nullable    = false

  validation {
    condition     = can(cidrnetmask(var.ssh_allowed_cidr))
    error_message = "Enter a valid IPv4 CIDR, such as 203.0.113.10/32."
  }
}
