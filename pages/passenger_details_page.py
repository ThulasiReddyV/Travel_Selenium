from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from pages.bus_and_seat_page import Bus_and_Seat_Selection
from datetime import datetime
from conftest import *

class Passenger_Details(Bus_and_Seat_Selection):
    
    GENDER_XPATH = (By.CLASS_NAME,'ant-select-selection-item')
    #GENDER_XPATH = (By.XPATH,'//*[contains(@class,"ant-select-selection") and .//*[contains(@id,"title")]]')
    #GENDER_XPATH = (By.XPATH,'//*[@type,"search" and contains(@id,"title")]')
    PASS_GENDER_SEL_XPATH = (By.XPATH,'//*[text()="Male"]')
    PASS_NAME_XPATH = (By.XPATH,'//*[@placeholder="Name"]')
    PASS_AGE_XPATH = (By.XPATH,'//*[@placeholder="Age"]')
    PASS_EMAIL_XPATH = (By.XPATH,'//*[@placeholder="Email"]')
    PASS_MOBILE_NO_XPATH = (By.XPATH,'//*[@placeholder="Mobile"]')
    #PAYMENT_OPTION_XPATH = (By.XPATH,'//*[@value="26"]')
    PAYMENT_OPTION_XPATH = (By.XPATH,'//span[contains(@class,"ant-radio") and .//*[@value="26"]]')
    PROCEED_TO_PAYMENT_XPATH = (By.XPATH,'//*[span[text()="Proceed to Payment"]]')
    CNF_DETAILS_XPATH = (By.XPATH,"//*[span[text()='OK']]")
    PAYMENT_POP_XPATH = (By.XPATH,'//span[contains(@class,"ptm-overlay-container")]')
    PAYMENT_POP_CLOSE_XPATH = (By.XPATH,'//span[contains(@class,"ptm-cross")]')

    def gender(self,gender):
        print("Filling Passenger Details")

        gender_dp = self.wait.until(EC.element_to_be_clickable(self.GENDER_XPATH))
        print("Gender Selection")
        gender_dp.click()
        gender_sel = self.wait.until(EC.visibility_of_element_located((By.XPATH,f'//*[text()="{gender.capitalize()}"]')))
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


    def payment_option_select(self):
        payment_option = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_OPTION_XPATH))      
        payment_option.click()
     
        proceed_to_payment = self.wait.until(EC.visibility_of_element_located(self.PROCEED_TO_PAYMENT_XPATH))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proceed_to_payment)
        proceed_to_payment.click()

    
    def booking_summary(self):
        
        self.driver.save_screenshot(f"{screenshots}/Passenger_Deatils_{timestamp}.png")
        confirm_details = self.wait.until(EC.visibility_of_element_located(self.CNF_DETAILS_XPATH))
        confirm_details.click()

    def payment_discount_pop_up(self):
        try:    
            payment_disc_pop_up = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_POP_XPATH))
            payment_disc_pop_up_closes = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_POP_CLOSE_XPATH))
            payment_disc_pop_up_closes.click()
        except TimeoutException:
            print("No payment discount pop_up")

        self.driver.save_screenshot(f"{screenshots}/Payment_Page_{timestamp}.png")
