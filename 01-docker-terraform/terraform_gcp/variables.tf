variable "project" {
  description = "project ID in which we will create all instance"
  default     = "clear-arbor-426506-u6"
}
variable "credential" {
  description = "credential file path different for different users"
  default     = "./credential/terraform.json"
}