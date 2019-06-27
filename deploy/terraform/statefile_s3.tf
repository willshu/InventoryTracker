terraform {
    backend "s3"{
        encrypt = true
        bucket = "scraper-tfstate"
        region = "us-east-1"
        key = "terraform.tfstate"
    }
}