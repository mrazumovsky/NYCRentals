from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time

opt = webdriver.ChromeOptions()
opt.add_experimental_option('w3c', False)
driver = webdriver.Chrome(chrome_options=opt)
# driver = webdriver.Chrome()
driver.get("https://www.compass.com/search/rentals/nyc/?cities=Queens&locations=%255B%257B%22geography%22:%22nyc%22,%22city%22:%22Queens%22%257D%255D")
login = driver.find_element_by_xpath('//button[@class="uc-corpNav-button uc-corpNav-menuItem textIntent-caption1 uc-corpNav-authBtn uc-corpNav-loginBtn"]')
login.click()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
username = driver.find_element_by_xpath("//input[@data-tn='loginForm-input-email']")
password = driver.find_element_by_xpath("//input[@data-tn='loginForm-input-password']")
username.send_keys("michael.razumovsky@gmail.com")
password.send_keys("Tbilisi!993")
login_submit = driver.find_element_by_xpath("//div[@class='uc-authenticationForm-actions']/button")
login_submit.click()


csv_file = open('compass_bk.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
#time.sleep(10)

#next_button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
#time.sleep(4)
#rows = driver.find_elements_by_xpath('//div[@class="info-wrapper info "]')


index = 1
while True:
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        print("Scraping Page number " + str(index))
        index = index + 1
        # Find all the reviews on the page
        wait_row = WebDriverWait(driver, 10)
        #rows = wait_row.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='uc-listingCard-content']")))
        rows = driver.find_elements_by_xpath('//div[@class="uc-listingCard-content"]')

        D = {}
        for listing in rows:
            try:
                Address = listing.find_element_by_xpath('.//a[@class="uc-listingCard-title"]').text
            except:
                Address = 'empty Address'
            try:
                Neighborhood = listing.find_element_by_xpath('.//h2[@class="uc-listingCard-subtitle"]').text
            except:
                Neighborhood = 'empty Price'
            try:
                Price = int(listing.find_element_by_xpath('.//div[@class="uc-listingCard-mainStats"]').text.replace('$','').replace(',',''))
            except:
                Price = 'empty Price'
            try:
                Bed = listing.find_element_by_xpath('.//div[@class="uc-listingCard-subStat uc-listingCard-subStat--beds"]').text
            except:
                Bed = 'empty Beds'
            try:
                Bath = listing.find_element_by_xpath('.//div[@class="uc-listingCard-subStat uc-listingCard-subStat--baths"]').text
            except:
                Bath = 'empty Bath'

            D['address'] = Address
            D['neighborhood'] = Neighborhood
            D['price'] = Price
            D['bed'] = Bed
            D['bath'] = Bath

            writer.writerow(D.values())

        wait_button = WebDriverWait(driver, 10)
        next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,'//button[@class="cx-paginator-btn cx-paginator-btn--next"]')))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #next_button = driver.find_element_by_xpath('//button[@class="cx-paginator-btn cx-paginator-btn--next"]')
        print('next button found =============')
        next_button.click()

    except Exception as e:
        print(e)
        csv_file.close()
        driver.close()
