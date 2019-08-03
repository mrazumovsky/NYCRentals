from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time

opt = webdriver.ChromeOptions()
# opt.add_experimental_option('w3c', False)
driver = webdriver.Chrome()#chrome_options=opt)
# driver = webdriver.Chrome()
driver.get("https://www.elliman.com/search/for-rent?sid=42658098")
login = driver.find_element_by_xpath('//div[@class="wysiwyg"]/p/a[2]')
login.click()
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
username = driver.find_element_by_xpath("//li[@id='email_address_li']/input")
password = driver.find_element_by_xpath("//li[@id='password_li']/input")
username.send_keys("michael.razumovsky@gmail.com")
password.send_keys("Tbilisi!993")
login_submit = driver.find_element_by_xpath("//input[@class='button']")
login_submit.click()
driver.get("https://www.elliman.com/search/for-rent?sid=42658098")


csv_file = open('de_manhattan.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
#time.sleep(10)

#next_button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
#time.sleep(4)
#rows = driver.find_elements_by_xpath('//div[@class="info-wrapper info "]')


index = 1
while True:
    time.sleep(1)
    try:
        print("Scraping Page number " + str(index))
        index = index + 1
        # Find all the reviews on the page
        # wait_row = WebDriverWait(driver, 10)
        # rows = wait_row.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='w_listitem_description']")))
        rows = driver.find_elements_by_xpath('//div[@class="w_listitem_description"]/ul')

        D = {}
        for listing in rows:
            try:
                Address = listing.find_element_by_xpath("./li/a").text
            except:
                Address = 'empty Address'
            try:
                Price = int(listing.find_element_by_xpath("./li[2]").text.replace('$','').replace(',','').split()[0])
            except:
                Price = 'empty Price'
            try:
                Rental = listing.find_element_by_xpath("./li[3]").text
            except:
                Rental = 'empty Rental'
            try:
                Bedbath = listing.find_element_by_xpath("./li[4]").text
            except:
                Bedbath = 'empty Bedbath'
            try:
                Sqfeet = listing.find_element_by_xpath("./li[5]").text
            except:
                Sqfeet = 'empty Sqfeet'

            D['address'] = Address
            D['price'] = Price
            D['rental'] = Rental
            D['bedbath'] = Bedbath
            D['Sqfeet'] = Sqfeet

            writer.writerow(D.values())

        # wait_button = WebDriverWait(driver, 10)
        # next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,'//span[@class="iui_paginator_next"]//a')))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next_button = driver.find_element_by_xpath('//span[@class="iui_paginator_next"]//a')
        print('next button found =============')
        next_button.click()

    except Exception as e:
        print(e)
        csv_file.close()

driver.close()
