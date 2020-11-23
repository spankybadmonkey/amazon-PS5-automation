#coding: utf-8

import time
import os
from os.path import join, dirname
from datetime import datetime
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver import DesiredCapabilities

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LOGIN_MAIL = os.environ.get("MAIL_ADDRESS")
LOGIN_PASSWORD = os.environ.get("PASSWORD")
ITEM_URL = "http://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp"
ACCEPT_SHOP = 'Amazon.com'
LIMIT_VALUE = 500    # Maximum USD for the purchase


def l(str):
    print("%s : %s" % (datetime.now().strftime("%Y/%m/%d %H:%M:%S"), str))

def launch():
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    opt.add_argument("--disable-xss-auditor")
    opt.add_argument("--disable-web-security")
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument("--allow-running-insecure-content")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--remote-debugging-port=921")
    opt.add_argument("--disable-webgl")
    opt.add_argument("--disable-popup-blocking")
    browser = webdriver.Chrome('./chromedriver' ,options=opt,desired_capabilities=d)
    browser.implicitly_wait(10)
    browser.set_page_load_timeout(20)
    return browser

if __name__ == '__main__':
    # Launch selenium
    print(format((ITEM_URL)))

    try:
        b = launch()
        b.get(ITEM_URL)
    except Exception as inst:
        l('Failed to open browser: {0}'.format(format(inst)))
        exit()

    time.sleep(3)

    # while True:
        # Check for inventory
    while True:
        try:
            shop = b.find_element_by_id('tabular-buybox-truncate-1').text

            if ACCEPT_SHOP not in shop:
                raise Exception("not Amazon.")

            b.find_element_by_id('add-to-cart-button').click()
            break
        except:
            time.sleep(60)
            b.refresh()

    # Purchase
    b.get('https://www.amazon.com/gp/cart/view.html/ref=nav_cart')
    b.find_element_by_id('proceedToCheckout').click()

    # Login
    try:
        b.find_element_by_id('ap_email').send_keys(LOGIN_MAIL)
        b.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
        b.find_element_by_id('signInSubmit').click()
    except:
        l('LOGIN PASS.')
        pass

    # Verify Price
    p = b.find_element_by_css_selector('td.grand-total-price').text
    if int(p.split(' ')[1].replace(',', '').replace('$', '')) > LIMIT_VALUE:
        l('PRICE IS TOO LARGE.')
        # continue

    # Place the order
    b.find_element_by_name('placeYourOrder1').click()
    # break

    l('ALL DONE.')
