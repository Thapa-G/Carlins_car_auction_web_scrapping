from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import  NoSuchElementException,TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import time

driver = webdriver.Chrome()
dict = {"Name": [],"Make": [],"Model": [],"Odometer": [],"Body_type": [],"Transmission": [],"Auctioneer": [],"Link_to_auction": [],"Unique_identifers": [],"Hours_to_auction": [],"State": [],"Build_Date":[],"Fuel":[]}
driver.get("https://www.carlins.com.au/auctions/catalogues/")
wait = WebDriverWait(driver, timeout=10, poll_frequency=1, ignored_exceptions=[TimeoutException])
# element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'link-description')))

elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "view")))

second_td_Date = driver.find_elements(By.XPATH, "//tr[contains(@ng-repeat, 'x in lAuctionCatalogues')]/td[2]")
i=0
for index,element in enumerate(elements):
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-icon")))
    element.click()

    # state

    # print(element.text)
    time.sleep(5)
    
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-icon")))
    Cars= wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "link-description")))
    for car in Cars:
        try:
            a_tag=car.find_element(By.TAG_NAME,'a')

            # link

            href=a_tag.get_attribute("href")
            # print(href)
            dict["Link_to_auction"].append(href)
            lines=a_tag.text.splitlines()
            # print(lines)
            text_fetched_upper=lines[0].split(" ")
            text_fetched_lower=lines[1].split(" ")

            years=text_fetched_upper[0] #
            if  len(years)==4:
                year=years
            else:
                text_fetched_upper.insert(0,"0000")
                year="0000"
            # print(year)
            make=text_fetched_upper[1]
            model=text_fetched_upper[2]
            transmission=text_fetched_lower[-4]
            body_type=text_fetched_upper[-2]
            value=text_fetched_upper[-3]
            fuels=['lpg','petrol','diesel']
            for vale in fuels:
                if vale==value.lower():
                    fuel=value
                else:
                    fuel=text_fetched_upper[-4]
            odometer_place = text_fetched_lower[-3]
            if "KM:" in odometer_place:
                odometer1= odometer_place.split(':')[1].strip()
            else:
                odometer1="0"

            name=' '.join(text_fetched_upper[1:-3])
            unique_identifer = ' '.join([year, name, make, odometer1])

            hours=date_text = second_td_Date[i].text
            date = datetime.strptime(date_text, '%d/%m/%Y')

            current_date = datetime.now()
            diff_in_hours = (date - current_date).total_seconds() / 3600
            hour = int(diff_in_hours) + 2

            dict["State"].append(element.text)
            dict["Name"].append(name)
            dict["Make"].append(make)
            dict["Model"].append(model)
            dict["Unique_identifers"].append(unique_identifer)
            dict["Hours_to_auction"].append(hour)
            dict["Odometer"].append(odometer1)
            dict["Transmission"].append(transmission)
            dict["Auctioneer"].append("Carlins")
            dict["Fuel"].append(fuel)
            
            dict["Body_type"].append(body_type)
            dict["Build_Date"].append(year)

            
            
        except NoSuchElementException:
            print("No tag found")
    i=i+1
driver.quit()

df = pd.DataFrame(dict)
df.to_csv('Carlins.csv', index=False)   


