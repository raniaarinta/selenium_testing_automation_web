from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException as NE
import time
from config_twitter import user_twitter,passowrd_twiiter
import csv
from textblob import TextBlob

#set webdriverpath
PATH="D:\python\chromedriver.exe"
driver=webdriver.Chrome(PATH)

def get_data(data):
    username = data.find_element_by_xpath('.//span').text
    try:
        handle = data.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except NE:
        return
    
    try:
        postdate = data.find_element_by_xpath('.//time').get_attribute('datetime')
    except NE:
        return
    
    comment = data.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = data.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    text = comment + responding
    reply = data.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet = data.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like = data.find_element_by_xpath('.//div[@data-testid="like"]').text
    blob= TextBlob(text)
    polarity=blob.sentiment[0]
    subjectivity=blob.sentiment[1]
    tweet = (username, handle, postdate, text, reply, retweet, like,polarity,subjectivity)
    return tweet



print(user_twitter,passowrd_twiiter)
#get started by opening the instagram login page
driver.get("https://twitter.com/login")
time.sleep(10)

username=driver.find_element_by_name("session[username_or_email]")
username.send_keys(user_twitter)

password= driver.find_element_by_name("session[password]")
password.send_keys(passowrd_twiiter)
time.sleep(10)

password.send_keys(Keys.RETURN)
time.sleep(10)
driver.get("https://twitter.com/explore")
time.sleep(10)
search= driver.find_element_by_xpath('//input[@aria-label="Search query"]')
search.send_keys('#coronavirus')
search.send_keys(Keys.RETURN)
time.sleep(10)


driver.find_element_by_link_text('Top').click()
# get all tweets on the page
data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in page_cards[-100:]:
        tweet = get_data(card)
        if tweet:
            tweet_id = ''.join(str(tweet))
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
            
    scroll_attempt = 0
    while True:
        # check scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1
            
            # end of scroll region
            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                time.sleep(10) # attempt another scroll
        else:
            last_position = curr_position
            break

# close the web driver
driver.close()

with open('tweet_nlp.csv', 'w', newline='', encoding='utf-8') as f:
    header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Comments', 'Likes', 'Retweets','polarity','subjectivity']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)