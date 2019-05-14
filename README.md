# InventoryTracker

**About**

InventoryTracker is a simple e-commerce web scraper with a RESTful API that handles updates to the product database. 

This project is written in Python and Django and includes the following components

*InventoryTracker\product_scraper*

The scraper portion of the project that parses HTML and posts to the API asyncronously 

*InventoryTracker\product_api\api*

The main API, built with django_restful

*InventoryTracker\product_api\message_service*

Messaging service with API calls to Twilio for querying and buying products via SMS

*InventoryTracker\product_api\browser_automations*

Browser automation functions for purchasing products 

