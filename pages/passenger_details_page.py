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
    PASS_DETAILS_VERIFY_XPATH = (By.XPATH,"//*[contains(@class ,'confirmation-summary')]//tr/td")
    PASS_EMAIL_MOBILE_VERIFY_XPATH=(By.XPATH,"//div[contains(@class,'ant-row')]//*[local-name()='svg']/parent::div")
    ERROR_CLASS = (By.CLASS_NAME,"ant-form-item-explain-error")
    SUMMARY_AREA_CLASS = (By.CLASS_NAME,"summary_area")
    SIDEBAR_AREA_CLASS = (By.CLASS_NAME,"sidebar-left")


    def booking_details(self):
        summary_area = self.driver.find_elements(*self.SUMMARY_AREA_CLASS)
        bk_data =[]
        for ele in summary_area:
            bk_data.extend(ele.text.splitlines())
        print((bk_data))


    def payment_option_select(self):
        payment_option = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_OPTION_XPATH))     
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", payment_option)
        payment_option.click()

        proceed_to_payment = self.wait.until(EC.visibility_of_element_located(self.PROCEED_TO_PAYMENT_XPATH))
        #self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proceed_to_payment)
        proceed_to_payment.click()
        time.sleep(1)
    
    def dummy(self):
        
        error_ele = self.driver.find_elements(*self.ERROR_CLASS)
        length = len(error_ele)
        print(length)

        if length == 0:
            return True
        else:
            return False
            
    def verify_boarding(self):
        summary_area = self.wait.until(EC.visibility_of_element_located(self.SUMMARY_AREA_CLASS))
        
        bus_details = summary_area.find_elements(By.TAG_NAME,"div")
        length = len(bus_details)
        print(f"bus deta {length}")
        booking_data = {}

        for ele in bus_details:
            print(ele.text)
            spans = ele.find_elements(By.TAG_NAME,"span")
            print(len(spans))

            if len(spans)>=2:
                
                key = spans[0].text.strip().replace(":"," ").strip()
                value = spans[1].text.strip()
                print(f"k={key}--->v={value}")

                if key in ["Boarding","Dropoff"] and '-' in value:
                    parts = value.split("-")
                    print(f"BD ,{parts}")
                    #if len(parts) == 3:
                    value = parts[1].strip()

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
                    booking_data[key_map[key]] = value

                print(booking_data)


            










    def verify_pass(self,org_dict):
        pass_details_elements = self.driver.find_elements(*self.PASS_DETAILS_VERIFY_XPATH)
        list_of_pass_data =[]
            
        for element in pass_details_elements:
            for line in element.text.splitlines():
                if not line.strip():
                    continue
                parts = re.split(r'\s*-\s*|\s{2,}', line.strip())
                list_of_pass_data.extend([p.strip() for p in parts if p.strip()])

        email_mobile = self.driver.find_elements(*self.PASS_EMAIL_MOBILE_VERIFY_XPATH)
        for el in email_mobile:
            list_of_pass_data.extend([line.strip() for line in el.text.splitlines() if line.strip()])
        
        print(list_of_pass_data)

        org_list = list(org_dict.values())
        print(org_list)



    