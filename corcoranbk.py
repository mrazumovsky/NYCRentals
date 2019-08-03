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
driver.get("https://www.corcoran.com/nyc-real-estate/for-sale/search/brooklyn?SaleType=Sale&Count=24&SearchingFrom=%2Fnyc-real-estate%2Ffor-sale%2Fsearch%2Fbrooklyn&IsNewDev=false&OnlyExclusives=False&Price.Minimum=0&Price.Maximum=1000000000&Bedrooms.SearchValue=-0.5&Bathrooms.SearchValue=0.5&Borough=Brooklyn&NeighborhoodID=6&NeighborhoodID=7&NeighborhoodID=4&NeighborhoodID=11&NeighborhoodID=13&NeighborhoodID=16&NeighborhoodID=17&NeighborhoodID=18&NeighborhoodID=19&NeighborhoodID=20&NeighborhoodID=25&NeighborhoodID=26&NeighborhoodID=28&NeighborhoodID=30&NeighborhoodID=31&NeighborhoodID=88&NeighborhoodID=32&NeighborhoodID=33&NeighborhoodID=35&NeighborhoodID=38&NeighborhoodID=40&NeighborhoodID=42&NeighborhoodID=43&NeighborhoodID=45&NeighborhoodID=46&NeighborhoodID=48&NeighborhoodID=53&NeighborhoodID=55&NeighborhoodID=61&NeighborhoodID=64&NeighborhoodID=296&NeighborhoodID=15&NeighborhoodID=69&NeighborhoodID=70&NeighborhoodID=71&NeighborhoodID=72&NeighborhoodID=75&NeighborhoodID=82&NeighborhoodID=92&NeighborhoodID=93&NewSearchName=&SearchName=&TypeOfHome=homes+for+sale&SortBySimplified=Recommended")

csv_file = open('corcoranbksales.csv', 'w', encoding='utf-8', newline='')
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
