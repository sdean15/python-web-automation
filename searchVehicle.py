from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import selenium.webdriver.chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


EXE_PATH = r'C:\Users\Spencer\Documents\chromedriver.exe'
WEBPAGE = 'https://www.cargurus.com/Cars/l-Used-GMC-Sierra-1500-Fargo-d116_L25989'
TIMEOUT = 10

listings = []

# create driver
driver = webdriver.Chrome(executable_path=EXE_PATH)

print("Connecting...")

# navigate to CarGurus sierra 1500 page in Fargo
driver.get(WEBPAGE)

print("Connected to page " + WEBPAGE)
print("fetching results...")

# navigate to select start year date
select_start_year = Select(driver.find_element_by_name('selectedStartYear'))

# select start date by value to 2016
select_start_year.select_by_value('c25231')


# navigate to select start year date
select_end_year = Select(driver.find_element_by_name('selectedEndYear'))

# select start date by value to 2019  (2018 = c26879)
select_end_year.select_by_value('c27478')


# navigate to radius
select_distance = Select(driver.find_element_by_id('distance'))

# select distance to 75.   valid values -(25, 50, 75, 100, 150)
select_distance.select_by_value('75')


# navigate to big "search button" and click it to get filtered results
driver.find_element_by_xpath('//*[@id="react-tabs-5"]/form/button').click()


# wait until page has new info and locates the SLT checkbox
slt_checkbox = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.ID, "TRIM_NAME-SLT")))

# have action move to the SLT checkbox and click the checkbox
ActionChains(driver).move_to_element(slt_checkbox).click(slt_checkbox).perform()


#  wait until page has new info and locates the color checkbox
color_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "COLOR-SILVER")))

# have the action move to the color checkbox and click
ActionChains(driver).move_to_element(color_checkbox).click(color_checkbox).perform()


#  wait until page refreshes with new info and locates the delivery checkbox
delivery_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "IS_SHIPPABLE")))

# navigate to delivery and click checkbox
ActionChains(driver).move_to_element(delivery_checkbox).click(delivery_checkbox).perform()


# we wait until all delivery listings are gone before putting local listings in the list
WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="cargurus-listing-search"]/div[1]/div/div[2]/div[1]/div[2]/div[2]/fieldset[6]/div[2]/div/label/span'), '0'))


# get the sponsored listing
sponsored_listing = driver.find_element_by_xpath('/html/body/main/div[2]/div[1]/div/div[2]/div[2]/div[5]/div[1]')

# run a script to remove the sponsored listing
driver.execute_script("""
var element = arguments[0];
 element.remove();""", sponsored_listing)


# gather all the local listings
listings = driver.find_elements_by_xpath('//*[@id="cargurus-listing-search"]//div[@class="EUQoKn"]')

# we pop the last 2 item in the list because for some reason they are empty all the time
listings.pop()
listings.pop()


print("Number of listings found: " + str(len(listings)))
print("\n")

# loop through all of our listings and print main info about each. Should equal # of listings found
for item in listings:

    try:
        title = item.find_element_by_tag_name('h4').text
        price = item.find_element_by_class_name('_4SFkcZ').text
        mileage = item.find_element_by_class_name('qUF2aQ').text
        location = item.find_element_by_class_name('_66MGoB').text
    except StaleElementReferenceException:
        listings.remove(item)
    except NoSuchElementException:
        listings.remove(item)

    print(title)
    print(price)
    print(mileage)
    print(location)
    print("\n")


print("Finished.")
driver.quit()











