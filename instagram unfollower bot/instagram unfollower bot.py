from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config_insta import instagram_user,instagram_password

#set webdriverpath
PATH="C:\Program Files (x86)\chromedriver.exe"
driver=webdriver.Chrome(PATH)
"""
my_password= getpass.getpass("the password")
print(my_password)
"""

#get started by opening the instagram login page
driver.get("https://www.instagram.com/")
time.sleep(3)
#get input text element and input the username and passowrd
username= driver.find_element_by_name("username")
#input instagram the username
username.send_keys(instagram_user)


password=driver.find_element_by_name("password")
#input instagram the password 
password.send_keys(instagram_password)

time.sleep(3)
button_submit=driver.find_element_by_css_selector("button[type='submit']")
button_submit.click()

#go to the following page
time.sleep(3)
driver.get("https://www.instagram.com/"+instagram_user+"/following/")
time.sleep(3)
following_xpath=driver.find_element_by_xpath('//a[contains(@href,"/following/")]')
following_xpath.click()

#click the following page
time.sleep(3)
my_follow_btn_xpath = "//button[contains(text(), 'Following')]"
unfollow_button_xpath=driver.find_elements_by_xpath(my_follow_btn_xpath)
unfollow="//button[contains(text(), 'Unfollow')]"
#unfollow automation using for loop
for b in unfollow_button_xpath:
    time.sleep(2) # self-throttle
    try:
        b.click()
        time.sleep(2)
    except:
        pass
    unfollow_b=driver.find_element_by_xpath(unfollow)
    unfollow_b.click()
