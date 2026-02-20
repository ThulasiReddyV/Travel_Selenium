from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from pages.bus_and_seat_page import Bus_and_Seat_Selection
from datetime import datetime
from conftest import *
from utilities import *
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
    PASS_MOBILE_NUM_XPATH = (By.XPATH,'//*[@placeholder="Mobile"]')
    #PAYMENT_OPTION_XPATH = (By.XPATH,'//*[@value="26"]')

    DATA_NOT_FILLED_ERROR_CLASS = (By.CLASS_NAME,"ant-form-item-explain-error")
    BOOKING_SUMMARY_CLASS = (By.CLASS_NAME,"ant-modal-content")
    PAYMENT_OPTION_XPATH = (By.XPATH,'//span[contains(@class,"ant-radio") and .//*[@value="26"]]')
    PROCEED_TO_PAYMENT_XPATH = (By.XPATH,'//*[span[text()="Proceed to Payment"]]')
    SUMMARY_AREA_CLASS = (By.CLASS_NAME,"summary_area")
    SIDEBAR_AREA_CLASS = (By.CLASS_NAME,"sidebar-left")



    def select_gender(self,gender):
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
        pass_mobile_no = self.wait.until(EC.element_to_be_clickable(self.PASS_MOBILE_NUM_XPATH))
        pass_mobile_no.click()
        pass_mobile_no.clear()
        #self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pass_mobile_no)
        pass_mobile_no.send_keys(mobile)
        self.wait.until(lambda d: pass_mobile_no.get_attribute("value") == mobile)
        print(f"Mobile: {pass_mobile_no.get_attribute("value")}")


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
                    
                if re.match(r'^\d{2}/\d{2}/\d{4}$', value):
                    value = datetime.strptime(value, "%d/%m/%Y").strftime("%Y-%m-%d")

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
        
        error_ele = self.driver.find_elements(*self.DATA_NOT_FILLED_ERROR_CLASS)
        length_error_ele = len(error_ele)

        booking_summary_class_ele = self.driver.find_elements(*self.BOOKING_SUMMARY_CLASS)
        length_booking = len(booking_summary_class_ele)
        print(f"Errors: {length_error_ele}, Booking summary: {length_booking}")

        if length_error_ele == 0 and length_booking != 0:
            return True
        else:
            return False
    