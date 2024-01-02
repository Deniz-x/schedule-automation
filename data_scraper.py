from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import date
import time


# configure webdriver
options = Options()
# options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

...
driver = webdriver.Chrome(options=options)
#                         ^^^^^^^^^^^^^^^
driver.get("https://amlf.cs.mcgill.ca/Web/view-schedule.php?")
# wait for page to load
#element = WebDriverWait(driver=driver, timeout=5).until(
#    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-target=directory-first-item]'))
#)


soup = BeautifulSoup(driver.page_source, 'lxml')
#css_selector = f"a[id={date.today()}] ~ .reservations"
todays_reservation_table = soup.find('a', id=f"{date.today()}").findNext("table")
print(todays_reservation_table)
todays_reservations = todays_reservation_table.find_all("div", class_="reserved")
print(todays_reservations)

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