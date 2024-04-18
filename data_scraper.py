from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import date, timedelta
import time

def get_reservations():
    # configure webdriver
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
    options.add_argument("start-maximized")  # ensure window is full-screen

    ...
    driver = webdriver.Chrome(options=options)
    driver.get("https://amlf.cs.mcgill.ca/Web/view-schedule.php?")

    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    driver.implicitly_wait(10)
    
    #get today's reservation table
    todays_reservation_table = soup.find('a', id=f"{date.today()}").findNext("table")

    # Wait for the reservations to be present
    reservations_locator = (By.CLASS_NAME, "reserved")
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(reservations_locator))
    #get the reservations
    todays_reservations = todays_reservation_table.find_all("div", class_="reserved")

    reservations = []
    # for each reservation, the relevant reservation info is extracted into a dictionary which is saved in the reservations list
    for reservation in todays_reservations:
        reservation_info = {}
        reservation_info["title"] = reservation.get_text().strip()

        # the pattern for the reservation link: https://amlf.cs.mcgill.ca/Web/reservation/?rn=56BC9F6B
        reservation_addresss = reservation['data-resid']
        driver.get(f"https://amlf.cs.mcgill.ca/Web/reservation/?rn={reservation_addresss}")
        time.sleep(5)

        soup2 = BeautifulSoup(driver.page_source, 'lxml')
        reservation_owner = soup2.select_one("#reservation-owner-section .reservation-content-section .reservation-label").findNext("div")
        reservation_info["owner"] = reservation_owner.get_text()

        #get the reservation time block
        res_time = soup2.select_one("#reservation-times-section")

        res_time_content = res_time.select_one(".reservation-content-section")

        #get start time
        start_time_div = res_time_content.select_one("div:first-child")
        start_time_list = start_time_div.select_one("div:nth-child(2)").get_text().split(" ")[1:]
        start_time = ' '.join(start_time_list)

        #get end time
        end_time_div = start_time_div.find_next_sibling("div")
        end_time_list = end_time_div.select_one("div:nth-child(2)").get_text().split(" ")[1:]
        end_time = ' '.join(end_time_list)

        #add the times to dictionary
        reservation_info["start_time"] = start_time
        reservation_info["end_time"] = end_time

        lab = soup2.select_one("#reservation-resources-section .reservation-selected-resources .reservation-resource").get_text()
        reservation_info["lab"] = lab
        instructor = soup2.select_one("#reservation-details-section .row .attribute .attribute-value").get_text()
        reservation_info["instructor"] = instructor
        reservations.append(reservation_info)
        
        
    return reservations
