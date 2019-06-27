
provider "aws" {
    profile    = "default"
    region     = var.aws_region
}

resource "aws_instance" "node1" {
    instance_type = "t2.micro"
    ami           = "ami-016a8193f03cf4a79"
    count = "1"
    subnet_id = aws_subnet.product_scanner_subnet.id
    vpc_security_group_ids = [aws_security_group.product_scanner_sec_groups.id]
    associate_public_ip_address = true  
    key_name = var.sshkeypair
}

resource "aws_vpc" "product_scanner_vpc"{
    cidr_block = var.vpc_cidr
}
resource "aws_subnet" "product_scanner_subnet"{
    cidr_block = "192.168.1.0/24"
    vpc_id = aws_vpc.product_scanner_vpc.id
    tags = {
        Name = "AppSubnet"
    }
}
resource "aws_security_group" "product_scanner_sec_groups"{
    name = "container_hosts"
    vpc_id = aws_vpc.product_scanner_vpc.id
    description = "Default Sec group for Container OS"
    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port = 0
        to_port = 65535
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_internet_gateway" "igw"{
    vpc_id = aws_vpc.product_scanner_vpc.id
}

resource "aws_route_table" "route_table" {
    vpc_id = aws_vpc.product_scanner_vpc.id
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.igw.id
    }
}

resource "aws_route_table_association" "rta" {
    subnet_id = aws_subnet.product_scanner_subnet.id
    route_table_id = aws_route_table.route_table.id
}

