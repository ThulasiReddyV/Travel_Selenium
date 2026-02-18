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
    

    def gender(self,gender):
        print("Filling Passenger Details")

        gender_dp = self.wait.until(EC.element_to_be_clickable(self.GENDER_XPATH))
        gender_dp.click()
        gender_sel = self.wait.until(EC.visibility_of_element_located((By.XPATH,f'//*[text()="{gender.capitalize()}"]')))
        print(f"Gender: {gender.capitalize()}")
        gender_sel.click()

    def enter_pass_name(self,name):
        pass_name = self.wait.until(EC.visibility_of_element_located(self.PASS_NAME_XPATH))
        pass_name.clear()
        pass_name.send_keys(name)
        print(f"Name: {name}")

    def enter_pass_age(self,age):
        pass_age = self.wait.until(EC.visibility_of_element_located(self.PASS_AGE_XPATH))
        pass_age.clear()
        pass_age.send_keys(age)
        print(f"Age: {age}")

        
    def enter_pass_email(self,email):
        pass_email = self.wait.until(EC.visibility_of_element_located(self.PASS_EMAIL_XPATH))
        pass_email.clear()
        pass_email.send_keys(email)
        print(f"Email: {email}")


    def enter_pass_mobile_no(self,mobile):
        pass_mobile_no = self.wait.until(EC.visibility_of_element_located(self.PASS_MOBILE_NO_XPATH))
        pass_mobile_no.clear()
        pass_mobile_no.send_keys(mobile)
        print(f"Mobile: {mobile}")

    PAYMENT_OPTION_XPATH = (By.XPATH,'//span[contains(@class,"ant-radio") and .//*[@value="26"]]')
    PROCEED_TO_PAYMENT_XPATH = (By.XPATH,'//*[span[text()="Proceed to Payment"]]')
    DATA_PASS = (By.XPATH,"//*[contains(@class ,'confirmation-summary')]//tr/td")
    BOOO=(By.XPATH,"//div[contains(@class,'ant-row')]//*[local-name()='svg']/parent::div")

    def payment_option_select(self):
            payment_option = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_OPTION_XPATH))      
            payment_option.click()
        
            proceed_to_payment = self.wait.until(EC.visibility_of_element_located(self.PROCEED_TO_PAYMENT_XPATH))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proceed_to_payment)
            proceed_to_payment.click()
            time.sleep(1)

    def verify_pass(self):
        pass_data_elements = self.driver.find_elements(*self.DATA_PASS)
        list_of_pass_data =[]
    
        for element in pass_data_elements:
            for line in element.text.splitlines():
                if not line.strip():
                    continue
                parts = re.split(r'\s*-\s*|\s{2,}', line.strip())
                list_of_pass_data.extend([p.strip() for p in parts if p.strip()])

        mob = self.driver.find_elements(*self.BOOO)
        for el in mob:
            list_of_pass_data.extend([line.strip() for line in el.text.splitlines() if line.strip()])
            print(el.text.strip())
        print("hhihi")
        print(list_of_pass_data)

    