from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from pages.bus_and_seat_page import Passenger_Details
from datetime import datetime
from conftest import *
from utilities import *
import time

class Payments_page(Passenger_Details):

    PAYMENT_OPTION_XPATH = (By.XPATH,'//span[contains(@class,"ant-radio") and .//*[@value="26"]]')
    PROCEED_TO_PAYMENT_XPATH = (By.XPATH,'//*[span[text()="Proceed to Payment"]]')
    CNF_DETAILS_XPATH = (By.XPATH,"//*[span[text()='OK']]")
    PAYMENT_POP_XPATH = (By.XPATH,'//span[contains(@class,"ptm-overlay-container")]')
    PAYMENT_POP_CLOSE_XPATH = (By.XPATH,'//span[contains(@class,"ptm-cross")]')
    QR_CLASS = (By.CLASS_NAME,"ptm-qr-img-container")

    def payment_option_select(self):
            payment_option = self.wait.until(EC.element_to_be_clickable(self.PAYMENT_OPTION_XPATH))      
            payment_option.click()
        
            proceed_to_payment = self.wait.until(EC.visibility_of_element_located(self.PROCEED_TO_PAYMENT_XPATH))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proceed_to_payment)
            proceed_to_payment.click()
            time.sleep(1)

        
    def booking_summary(self):
        take_screenshot(self.driver,'Passenger_Details')
        confirm_details = self.wait.until(EC.visibility_of_element_located(self.CNF_DETAILS_XPATH))
        confirm_details.click()

    def payment_discount_pop_up(self):
        try:    
            payment_disc_pop_up = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_POP_XPATH))
            payment_disc_pop_up_closes = self.wait.until(EC.visibility_of_element_located(self.PAYMENT_POP_CLOSE_XPATH))
            payment_disc_pop_up_closes.click()
        except TimeoutException:
            print("No payment discount pop_up")

        WebDriverWait(self.driver,50).until(EC.visibility_of_element_located(self.QR_CLASS))
        take_screenshot(self.driver,'Payment_Page')