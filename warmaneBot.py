from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import requests
import time
from dotenv import load_dotenv

site_key = "6LfXRRsUAAAAAEApnVwrtQ7aFprn4naEcc05AZUR"
page_url = 'https://www.warmane.com/account/login'
vote_url = 'https://www.warmane.com/account'

load_dotenv()
user = os.getenv('user')
password = os.getenv('password')
api_key = os.getenv('api_key')

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome('chromedriver',options=chrome_options)
driver.get(page_url)

def redeem_points(user_war, password_war, driver):

    driver.get(page_url)
    driver.find_element_by_id("userID").send_keys(user_war)
    driver.find_element_by_id("userPW").send_keys(password_war)

    form = {"method": "userrecaptcha",
            "googlekey": site_key,
            "key": api_key,
            "pageurl": page_url,
            "json": 1}

    print(form)
    print(len(form['key']))

    response = requests.post('http://2captcha.com/in.php', data=form)
    request_id = response.json()['request']
    print(request_id)

    url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1"

    status = 0
    while not status:
        res = requests.get(url)
        if res.json()['status']==0:
            time.sleep(3)
            print("Status:", res.json())
        else:
            requ = res.json()['request']
            js = f'document.getElementById("g-recaptcha-response").innerHTML="{requ}";'
            driver.execute_script(js)
            driver.find_element_by_class_name('wm-ui-btn').click()
            print("Logged in")
            driver.get(vote_url)
            time.sleep(2)
            try:
                driver.find_element_by_css_selector(".wm-ui-hyper-custom-b[data-click='collectpoints']").click()
                time.sleep(5)
                points = driver.find_element_by_class_name("myPoints").get_attribute("innerHTML")
                print("Points redemeeded : " + points)
            except Exception as e:
                print("Error redeeming: " + e)

            status = 1


redeem_points(user, password, driver)
driver.quit()
