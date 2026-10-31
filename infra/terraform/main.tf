
resource "hcloud_ssh_key" "fitness" {
  name       = "personal-fitness-ssh"
  public_key = file(pathexpand("~/.ssh/id_ed25519.pub"))
}

resource "hcloud_firewall" "fitness" {
  name = "personal-fitness-firewall"

  rule {
    direction   = "in"
    protocol    = "tcp"
    port        = "22"
    source_ips  = [var.ssh_allowed_cidr]
    description = "Allow SSH from my public IP"
  }
}

resource "hcloud_server" "fitness" {
  name        = "personal-fitness-server"
  server_type = "cx23"
  image       = "ubuntu-24.04"
  location    = "fsn1"

  ssh_keys     = [hcloud_ssh_key.fitness.id]
  firewall_ids = [hcloud_firewall.fitness.id]

  backups = false

  labels = {
    project     = "personal-fitness-tracker"
    environment = "production"
    managed_by  = "terraform"
  }
}
