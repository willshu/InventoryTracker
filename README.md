# InventoryTracker

**About**

InventoryTracker is a simple e-commerce web scraper with a RESTful API that handles updates to the product database. 

I originally intended this to scrape for interesting products and be alerted to them as they were added. The initial version stored data in a Python list and sent a push each time the length increased. Later, I added persistent object storage via the Django ORM and alerting via Twilio. Since some products were "rare" and sold out within minutes, I added some Selenium browser automations to execute automated purchasing of products in response to inbound SMS messages

This is a personal project that currently lacks many features. Some of my more ambitious goals for making this project more useful include:
1. User accounts in Django and user-specific product tables
2. Ability to enter a URL and syntactically locate XPATHs in the DOM for customized scraping
3. Build a browser plug-in to gather raw data about product attributes 
4. Build a ML model from raw data and scrape without the need for individual, baked-in rulesets 
5. Leverage user-generated data from (3) and (4) to further train the model 

This project is written in Python and Django, and is intended to be run on a Docker host with the included docker-compose.yml

**Structure (simplified)**
```
InventoryTracker
|-- deploy
|   `-- terraform
|       |-- main.tf
|       |-- terraform.tfvars
|       |-- variables.tf
|       `-- statefile_s3.tf
|-- product_api
|   |-- api
|   |   |-- urls.py
|   |   |-- views.py
|   |   |-- models.py
|   |   `-- serializers.py
|   |-- message_service
|   |   |-- browser_automations.py
|   |   `-- views.py
|   |-- product_api
|   |   |-- settings.py
|   |   `-- urls.py
|   |-- config.env
|   |-- static
|   |-- start.sh
|   `-- Dockerfile
|-- product_scraper
|   |-- scraper.py
|   |-- config.env
|   `-- Dockerfile
|-- product_gateway
|   |-- nginx
|   |   `-- nginx.conf
|   `-- Dockerfile
`-- docker-compose.yml
```
**Folder Details**
------

**InventoryTracker/deploy/terraform**
- Teraform files for deploying to AWS
- Existing database is used

**InventoryTracker/product_scraper**
- The scraper portion of the project that parses HTML 
- Posts to the above API asyncronously 

**InventoryTracker/product_api/api**
- API, built with django_restful
- Also uses django_rest_auth

**InventoryTracker/product_api/message_service**
- Interactive SMS service with API calls to Twilio for querying ORM over a mobile device
- Enables two way messaging

**InventoryTracker/product_api/product_api**
- Main Django project folder

**InventoryTracker/product_api/browser_automations**
- Browser automation functions for purchasing products 
- Requires config file for storing sensitive billing info
- Uses headless Firefox or Chrome driver

**InventoryTracker/product_api/product_gateway**
 - Nginx config for load balancing and proxying
 

