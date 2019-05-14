from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
#from selenium.webdriver.firefox.options import Options
from message_service.browser_settings import shipping, billing, card
import time

def add_to_cart(url, driver):
    #driver = webdriver.Chrome(executable_path='/Users/willshu/Projects/product_scanner/product_api/message_service/chromedriver')
    driver.get(url)
    driver.find_element_by_id("form-action-addToCart").click()

def checkout(url, driver):
    driver = webdriver.Chrome(executable_path='/Users/willshu/Projects/product_scanner/product_api/message_service/chromedriver')
    driver.get(url)

def add_and_checkout(url):
    #driver = webdriver.Chrome(executable_path='/Users/willshu/Projects/product_scanner/product_api/message_service/chromedriver')
    #driver = webdriver.Firefox(executable_path='/Users/willshu/Projects/product_scanner/product_api/message_service/geckodriver')
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    # binary = "/usr/bin/firefox"
    # driver = webdriver.Firefox(firefox_binary=binary)
    driver = webdriver.Firefox(executable_path='/home/ec2-user/product_scanner_aws/product_api/message_service/geckodriver', options=options)
    driver.get(url)
    driver.find_element_by_id("form-action-addToCart").click()
    time.sleep(1)
    driver.find_element_by_xpath("//a[@href='/checkout.php']").click()
    time.sleep(1)
    driver.find_element_by_id('email').send_keys(shipping['email_address'])
    driver.find_element_by_id('checkout-customer-continue').click()
    time.sleep(2)
    country = Select(driver.find_element_by_name('countryCodeInput'))
    country.select_by_value('string:US')
    state = Select(driver.find_element_by_name('provinceCodeInput'))
    state.select_by_value('string:NY')
    driver.find_element_by_id('firstNameInput').send_keys(shipping['first_name'])
    driver.find_element_by_id('lastNameInput').send_keys(shipping['last_name'])
    driver.find_element_by_id('addressLine1Input').send_keys(shipping['address_street'])
    driver.find_element_by_id('addressLine2Input').send_keys(shipping['address_floor'])
    driver.find_element_by_id('cityInput').send_keys(shipping['address_city'])
    driver.find_element_by_id('postCodeInput').send_keys(shipping['address_zip'])
    driver.find_element_by_id('phoneInput').send_keys(shipping['phone'])
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #different billing
    same = driver.find_element_by_xpath('//*[@id="sameAsBilling"]')
    driver.execute_script("arguments[0].click();", same)
    cont = driver.find_elements_by_xpath('//*[@id="checkout-shipping-continue"]')[0]
    driver.execute_script("arguments[0].click();", cont)
    time.sleep(2)
    ship = driver.find_element_by_xpath("//*[@id='checkout-shipping-options']/div/shipping-options/div/shipping-options-list/ul/li[1]/div/label")
    driver.execute_script("arguments[0].click();", ship)
    time.sleep(1)
    driver.find_element_by_id('checkout-shipping-continue').click()
    #fill out billing
    time.sleep(2)
    country = Select(driver.find_element_by_name('countryCodeInput'))
    country.select_by_value('string:US')
    state = Select(driver.find_element_by_name('provinceCodeInput'))
    state.select_by_value('string:NY')
    driver.find_element_by_id('firstNameInput').send_keys(billing['first_name'])
    driver.find_element_by_id('lastNameInput').send_keys(billing['last_name'])
    driver.find_element_by_id('addressLine1Input').send_keys(billing['address_street'])
    driver.find_element_by_id('addressLine2Input').send_keys(billing['address_floor'])
    driver.find_element_by_id('cityInput').send_keys(billing['address_city'])
    driver.find_element_by_id('postCodeInput').send_keys(billing['address_zip'])
    driver.find_element_by_id('phoneInput').send_keys(billing['phone'])
    cont2 = driver.find_element_by_xpath('//*[@id="checkout-billing-continue"]')
    cont2.click()
    time.sleep(1)
    #enter card info
    driver.find_element_by_id('ccNumber').send_keys(card['card_number'])
    driver.find_element_by_id('ccExpiry').send_keys(card['expiration'])
    driver.find_element_by_id('ccName').send_keys(billing['first_name'] +' ' + billing['last_name'])
    driver.find_element_by_id('ccCvv').send_keys(card['cvv'])
    driver.execute_script("window.scrollTo(100, document.body.scrollHeight);")
    #agree to terms
    agree = driver.find_element_by_xpath('//*[@id="terms"]')
    driver.execute_script("arguments[0].click();", agree)
    driver.save_screenshot('/home/ec2-user/product_scanner_aws/product_api/message_service/screenshot_before.png')
    finish = driver.find_element_by_xpath('//*[@id="checkout-payment-continue"]')
    finish.click()
    time.sleep(2)
    driver.save_screenshot('/home/ec2-user/product_scanner_aws/product_api/message_service/screenshot_after.png')
    time.sleep(10)
    driver.close()
