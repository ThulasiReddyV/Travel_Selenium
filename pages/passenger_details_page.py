from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from pages.bus_and_seat_page import Bus_and_Seat_Selection
from datetime import datetime
from conftest import *
from utilities import *
from datetime import datetime
import time
import re

class Passenger_Details(Bus_and_Seat_Selection):
    
    GENDER_XPATH = (By.CLASS_NAME,"ant-select-selection-item")
    #GENDER_XPATH = (By.XPATH,'//*[contains(@class,"ant-select-selection") and .//*[contains(@id,"title")]]')
    #GENDER_XPATH = (By.XPATH,'//*[@type,"search" and contains(@id,"title")]')
    PASS_GENDER_SEL_XPATH = (By.XPATH,'//*[text()="Male"]')
    PASS_NAME_XPATH = (By.XPATH,'//*[@placeholder="Name"]')
    PASS_AGE_XPATH = (By.XPATH,'//*[@placeholder="Age"]')
    PASS_EMAIL_XPATH = (By.XPATH,'//*[@placeholder="Email"]')
    PASS_MOBILE_NO_XPATH = (By.XPATH,'//*[@placeholder="Mobile"]')
    #PAYMENT_OPTION_XPATH = (By.XPATH,'//*[@value="26"]')
    FROM_IN_SUMMARY_XPATH = (By.XPATH,"//div[@class='summary_area']//span[text()='From']/following-sibling::span")
    TO_IN_SUMMARY_XPATH = (By.XPATH,"//div[@class='summary_area']//span[text()='To']/following-sibling::span")
    DATE_IN_SUMMARY_XPATH = (By.XPATH,"//div[@class='summary_area']//span[text()='Service Start Date']/following-sibling::span")
    SERVICE_NO_IN_SUMMARY_XPATH = (By.XPATH,"//div[@class='summary_area']//span[text()='Service No.']/following-sibling::span")
    SEAT_NO_IN_SUMMARY_XPATH = (By.XPATH,"//div[@class='summary_area']//span[text()='Seat No(s)']/following-sibling::span")
    BOARDING_IN_SUMMARY_XPATH = (By.XPATH,"//div[@class='summary_area']//span[text()='Boarding']/following-sibling::span")
    DROPPING_IN_SUMMARY_XPATH = (By.XPATH,"//div[@class='summary_area']//span[text()='Dropoff']/following-sibling::span")
    DATA_NOT_ENTERED_CLASS = (By.CLASS_NAME,"ant-form-item-explain-error")

    def gender(self,gender):
        print("Filling Passenger Details")

        gender_dp = self.wait.until(EC.element_to_be_clickable(self.GENDER_XPATH))
        gender_dp.click()
        gender_sel = self.wait.until(EC.visibility_of_element_located((By.XPATH,f'//*[text()="{gender.capitalize()}"]')))
        print(f"Gender: {gender.capitalize()}")
        gender_sel.click()

    def enter_pass_name(self,name):
        pass_name = self.wait.until(EC.element_to_be_clickable(self.PASS_NAME_XPATH))
        pass_name.click()
        pass_name.clear()
        pass_name.send_keys(name)
        self.wait.until(lambda d: pass_name.get_attribute("value") == name)
        print(f"Name: {pass_name.get_attribute("value")}")

    def enter_pass_age(self,age):
        pass_age = self.wait.until(EC.element_to_be_clickable(self.PASS_AGE_XPATH))
        pass_age.click()
        pass_age.clear()
        pass_age.send_keys(age)
        self.wait.until(lambda d: pass_age.get_attribute("value") == age)
        print(f"Age: {pass_age.get_attribute("value")}")


        
    def enter_pass_email(self,email):
        pass_email = self.wait.until(EC.element_to_be_clickable(self.PASS_EMAIL_XPATH))
        pass_email.click()
        pass_email.clear()
        pass_email.send_keys(email)
        self.wait.until(lambda d: pass_email.get_attribute("value") == email)
        print(f"Email: {pass_email.get_attribute("value")}")



    def enter_pass_mobile_no(self,mobile):
        pass_mobile_no = self.wait.until(EC.element_to_be_clickable(self.PASS_MOBILE_NO_XPATH))
        pass_mobile_no.click()
        pass_mobile_no.clear()
        #self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pass_mobile_no)
        pass_mobile_no.send_keys(mobile)
        self.wait.until(lambda d: pass_mobile_no.get_attribute("value") == mobile)
        print(f"Mobile: {pass_mobile_no.get_attribute("value")}")


    PAYMENT_OPTION_XPATH = (By.XPATH,'//span[contains(@class,"ant-radio") and .//*[@value="26"]]')
    PROCEED_TO_PAYMENT_XPATH = (By.XPATH,'//*[span[text()="Proceed to Payment"]]')
    ERROR_CLASS = (By.CLASS_NAME,"ant-form-item-explain-error")
    SUMMARY_AREA_CLASS = (By.CLASS_NAME,"summary_area")
    SIDEBAR_AREA_CLASS = (By.CLASS_NAME,"sidebar-left")


    
    
            
    def verify_booking_details(self):
        summary_area = self.wait.until(EC.visibility_of_element_located(self.SUMMARY_AREA_CLASS))
        
        bus_details = summary_area.find_elements(By.TAG_NAME,"div")
        booking_details = {}

        for ele in bus_details:
            spans = ele.find_elements(By.TAG_NAME,"span")
            if len(spans)>=2:
                
                key = spans[0].get_attribute("textContent").replace(":"," ").strip()
                value = spans[1].get_attribute("textContent")
                
                if key in ["Boarding","Dropoff"] and ' - ' in value:
                    parts = value.split("-")
                    print(f"BD ,{parts}")
                    if len(parts) >= 3:
                        value = parts[1].strip()
                    
                if value in value.strip().strftime("%d/%m/%y"):
                    value = datetime.strptime(value("%Y-%m-%d"))

                key_map = {
                    "From": "from_loc",
                    "To": "to_loc",
                    "Service Start Date": "Date_of_journey",
                    "Service No.": "bus_ser_no",
                    "Seat No(s)": "seat_no",
                    "Boarding": "boarding_pt",
                    "Dropoff": "dropping_pt"
                }

            if key in key_map:
                booking_details[key_map[key]] = value

        print(booking_details)
        return booking_details
    

    def payment_option_select(self):
        payment_option = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_OPTION_XPATH))     
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", payment_option)
        payment_option.click()

        proceed_to_payment = self.wait.until(EC.visibility_of_element_located(self.PROCEED_TO_PAYMENT_XPATH))
        #self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proceed_to_payment)
        proceed_to_payment.click()
        time.sleep(1)

    
    def error_check(self):
        
        error_ele = self.driver.find_elements(*self.ERROR_CLASS)
        length = len(error_ele)
        print(length)

        if length == 0:
            return True
        else:
            return False

    JOURNEY_DETAILS_VERIFY_XPATH = (By.XPATH,"//h4[text()='Journey Details']/following::table[1]//tr")
    PASS_DETAILS_VERIFY_XPATH = (By.XPATH,"//h4[text()='Passengers']/following::table[1]//tbody/tr")
    PASS_EMAIL_MOBILE_VERIFY_XPATH = (By.XPATH,"//h4[text()='Passengers']/following::div[contains(@class,'ant-col')]")

    def get_booking_summary(self):

        journey_details = self.driver.find_elements(*self.JOURNEY_DETAILS_VERIFY_XPATH)
        journey_ui = {}
    
        for ele in journey_details:
            header = ele.find_element(By.ID,"th").text.strip().lower()
            value = ele.find_element(By.ID,"td").text.strip()

            if header == "journey":
                from_to = value.split("→")
                journey_ui["from_loc"] = from_to[0].strip()
                journey_ui["to_loc"] = from_to[1].strip()

            elif header == "date":
                journey_ui["Date_of_journey"] = value

            elif header == "service no":
                journey_ui["bus_ser_no"] = value

            elif header == "boarding":
                journey_ui["boarding_pt"] = value

            elif header == "dropping":
                journey_ui["dropping_pt"] = value


        passenger_row = self.driver.find_element(*self.PASS_DETAILS_VERIFY_XPATH)
        cols = passenger_row.find_elements(By.TAG_NAME, "td")

        journey_ui["seat_no"] = cols[0].text.strip()

        name_text = cols[1].text.strip().split()
        title = name_text[0].strip().lower().replace(".", "")

        gender_map = {
            "mr": "Male",
            "mrs": "Female",
            "miss": "Female"
        }

        journey_ui["pass_gender"] = gender_map.get(title, "")
        journey_ui["pass_name"] = " ".join(name_text[1:])
        journey_ui["pass_age"] = cols[2].text.strip()

        # Email & Mobile
        pass_email = ""
        pass_mobile = ""

        email_mobile_divs = self.driver.find_elements(*self.PASS_EMAIL_MOBILE_VERIFY_XPATH)

        for div in email_mobile_divs:
            text = div.text.strip()
            if "@" in text:
                pass_email = text
            elif text.isdigit():
                pass_mobile = text

        journey_ui["pass_email"] = pass_email
        journey_ui["pass_mobile"] = pass_mobile

    
        print(journey_ui)
        return journey_ui

    def merge_booking_journey(self):

        booking = self.verify_booking_details()
        journey = self.get_booking_summary()
        ui_dict = {}
        mismatches = []

        all_keys = set(booking.keys()).union(set(journey.keys()))

        for key in all_keys:

            if key in booking and key in journey:
                if booking[key] == journey[key]:
                    ui_dict[key] = booking[key]
                else:
                    print(f"Value mismatch for key '{key}' → Expected: {booking[key]} | Actual: {journey[key]}")
                    mismatches.append(f"{key}: Expected={booking[key]} | Actual={journey[key]}"
                )

            elif key in booking:
                ui_dict[key] = booking[key]

            elif key in journey:
                ui_dict[key] = journey[key]
        
        if mismatches:
            raise AssertionError("Mismatches found:\n" + "\n".join(mismatches))
        
        return ui_dict





            




    