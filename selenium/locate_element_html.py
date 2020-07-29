from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH="C:\Program Files (x86)\chromedriver.exe"
driver=webdriver.Chrome(PATH)

#open the website
driver.get("https://www.google.co.id/")
#find input element
search=driver.find_element_by_name("q")
#eneter value on an input element
search.send_keys("bts on mv")
search.send_keys(Keys.RETURN)

try:
    rso= WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,"rso"))
        )
    print(rso.text)
except:
    driver.quit()
    

