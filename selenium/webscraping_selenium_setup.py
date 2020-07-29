from selenium import webdriver
PATH="C:\Program Files (x86)\chromedriver.exe"
driver=webdriver.Chrome(PATH)

#open the website
driver.get("https://github.com/raniaarinta")
#get the title of the website
print("title website",driver.title())
