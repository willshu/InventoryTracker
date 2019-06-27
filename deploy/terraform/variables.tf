variable "aws_region"{
    type = string
    default = "us-east-1"
}
variable "vpc_cidr"{
    type = string
    default = "192.168.0.0/16"
}

variable "sshkeypair"{
    type = string
    default = "will-django-dev"
}