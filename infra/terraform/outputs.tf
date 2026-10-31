
output "server_ipv4" {
  description = "Public IPv4 address of the Hetzner server"
  value       = hcloud_server.fitness.ipv4_address
}

output "server_name" {
  description = "Name of the Hetzner server"
  value       = hcloud_server.fitness.name
}
