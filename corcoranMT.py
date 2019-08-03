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
driver.get("https://www.corcoran.com/nyc-real-estate/for-rent/search/manhattan?SaleType=Rent&Count=24&SearchingFrom=%2Fnyc-real-estate%2Ffor-rent%2Fsearch%2Fmanhattan&IsNewDev=false&OnlyExclusives=False&Price.Minimum=0&Price.Maximum=1000000000&Bedrooms.SearchValue=-0.5&Bathrooms.SearchValue=0.5&Borough=Manhattan&NeighborhoodID=5&NeighborhoodID=8&NeighborhoodID=94&NeighborhoodID=21&NeighborhoodID=22&NeighborhoodID=23&NeighborhoodID=24&NeighborhoodID=34&NeighborhoodID=36&NeighborhoodID=37&NeighborhoodID=39&NeighborhoodID=44&NeighborhoodID=47&NeighborhoodID=49&NeighborhoodID=50&NeighborhoodID=51&NeighborhoodID=523&NeighborhoodID=57&NeighborhoodID=62&NeighborhoodID=63&NeighborhoodID=66&NeighborhoodID=67&NeighborhoodID=524&NeighborhoodID=73&NeighborhoodID=76&NeighborhoodID=83&NeighborhoodID=85&NeighborhoodID=86&NeighborhoodID=87&NeighborhoodID=89&NeighborhoodID=91&NewSearchName=&SearchName=&TypeOfHome=homes+for+sale&SortBySimplified=Recommended&Page=323")

csv_file = open('corcoranMTtry.csv', 'w', encoding='utf-8', newline='')
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
        wait_row = WebDriverWait(driver, 10)
        rows = wait_row.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="info-wrapper info "]')))

        D = {}
        for listing in rows:
            try:
                address = listing.find_element_by_xpath(".//a").text
            except:
                address = 'empty address'
            try:
                price = int(''.join(listing.find_element_by_xpath(".//div[1]").text.split("$")[1].split(",")))
            except:
                price = 'empty price'
            try:
                description = listing.find_element_by_xpath(".//div[2]").text
            except:
                description = 'empty description'
            try:
                neighborhood = listing.find_element_by_xpath(".//div[3]/a").text
            except:
                neighborhood = 'empty neighborhood'

            D['address'] = address
            D['price'] = price
            D['description'] = description
            D['neighborhood'] = neighborhood

            writer.writerow(D.values())

        wait_button = WebDriverWait(driver, 10)
        next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,'//a[@title="Go to next page"]')))
        print('next button found =============')
        next_button.click()

    except Exception as e:
        print(e)
        csv_file.close()
        driver.close()
