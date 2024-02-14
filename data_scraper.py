from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import date, timedelta
import time


# configure webdriver
options = Options()
# options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

...
driver = webdriver.Chrome(options=options)
#     https://amlf.cs.mcgill.ca/Web/view-schedule.php?sd=2024-1-8                    ^^^^^^^^^^^^^^^
#driver.get("https://amlf.cs.mcgill.ca/Web/view-schedule.php?")
driver.get("https://amlf.cs.mcgill.ca/Web/view-schedule.php?sd=2024-1-8")
# wait for page to load
#element = WebDriverWait(driver=driver, timeout=5).until(
#    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-target=directory-first-item]'))
#)

soup = BeautifulSoup(driver.page_source, 'lxml')
#css_selector = f"a[id={date.today()}] ~ .reservations"
date_range_on_page = soup.find('button', class_="change-date").findNext("div").text.strip().split("-")
first_date_on_page = date_range_on_page[0].strip()
last_date_on_page = date_range_on_page[1].strip().split("/")
print(last_date_on_page)
last_date_year = int("20" + last_date_on_page[2])
last_date_month = int(last_date_on_page[0])
last_date_day = int(last_date_on_page[1])
last_date = date(last_date_year, last_date_month, last_date_day)

print(f"last date on page is {last_date}")
driver.implicitly_wait(10)
#todays_reservation_table = soup.find('a', id=f"{date.today()+timedelta(days=5)}").findNext("table")
#print(f"today's reservation table is: {todays_reservation_table}")
#todays_reservations = todays_reservation_table.find_all("div", class_="reserved")

#print(f"today's reservations are: {todays_reservations}")

# Wait for the table to be present
table_locator = (By.ID, f"{date.today() + timedelta(days=5)}")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(table_locator)
)
#get today's reservation table
todays_reservation_table = soup.find('a', id=f"{date.today() + timedelta(days=5)}").findNext("table")

# Wait for the reservations to be present
reservations_locator = (By.CLASS_NAME, "reserved")
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(reservations_locator))
#get the reservations
todays_reservations = todays_reservation_table.find_all("div", class_="reserved")

print(f"today's reservations are: {todays_reservations}")


#if there are no reservations today, find a day with reservations
current_lookup_date = date.today()+timedelta(days=5) + timedelta(days=1)
if len(todays_reservations) == 0:
    i = 1
    while i<7:
        time.sleep(1)
        
        #print("----------------------")
        #print(f"next_reservation table on {current_lookup_date} is {next_reservation_table.prettify()}")
        #print("----------------------")
        table_locator = (By.ID, f"{current_lookup_date}")
        todays_reservation_table = WebDriverWait(driver, 10).until(EC.presence_of_element_located(table_locator))
        next_reservation_table = soup.find('a', id=f"{current_lookup_date}").findNext("table")

        # Wait for the reservations to be present
        reservations_locator = (By.XPATH, "//div[@class='reserved']")
        todays_reservations = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(reservations_locator))
        next_reservations = next_reservation_table.find_all("div", class_="reserved pending event")
        #next_reservations = next_reservation_table.select("div.reserved, div.reserved.pending.event")
        
        print(f"next_reservations on {current_lookup_date} is {next_reservations}")

        i += 1

        if current_lookup_date==last_date:
            print("No reservations this week!")
            break

        current_lookup_date += timedelta(days=1)

        if len(next_reservations) != 0:
            break
        


reservations = []

for reservation in todays_reservations:
    reservation_info = {}
    reservation_info["title"] = reservation.get_text()

    reservation_addresss = reservation['data-resid']
    driver.get(f"https://amlf.cs.mcgill.ca/Web/reservation/?rn={reservation_addresss}")
    time.sleep(5)

    soup2 = BeautifulSoup(driver.page_source, 'lxml')
    reservation_owner = soup2.select_one("#reservation-owner-section .reservation-content-section .reservation-label").findNext("div")
    reservation_info["owner"] = reservation_owner.get_text()
    res_time = soup2.select("#reservation-times-section .reservation-content-section .reservation-label")
    start_time = res_time[0].findNext("div")
    end_time = res_time[1].findNext("div")
    print(f"start time is {start_time.get_text()}")
    reservation_info["start_time"] = start_time.get_text().split(", ")[1]
    reservation_info["end_time"] = end_time.get_text().split(", ")[1]
    lab = soup2.select_one("#reservation-resources-section .reservation-selected-resources .reservation-resource").get_text()
    reservation_info["lab"] = lab
    instructor = soup2.select_one("#reservation-details-section .row .attribute .attribute-value").get_text()
    reservation_info["instructor"] = instructor
    reservations.append(reservation_info)
    
    
print(reservations)
# the pattern for the reservation link: https://amlf.cs.mcgill.ca/Web/reservation/?rn=56BC9F6B
# data-resid