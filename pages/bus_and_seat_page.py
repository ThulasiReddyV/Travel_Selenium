from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException

from pages.booking_page import Booking_page

class Bus_and_Seat_Selection(Booking_page):

    PARENT_DIV = (By.XPATH,'./ancestor::div[contains(@class,"ant-col-3")]')
    VIEW_SEATS_BUTTON_XPATH = (By.XPATH,'./following-sibling::div[contains(@class,"ant-col-4")]//button[@type = "button"]')
    
    BOARDING_POINT_ID = (By.ID,"boardingPoint")
    DROPPING_POINT_ID = (By.ID,"droppingPoint")
    BP_DP_SUBMIT_XPATH = (By.XPATH,'//*[span[text()="Submit"]]')
    SEAT_CONTINUE_XPATH = (By.XPATH,'//*[span[text()="Continue"]]')

    def bus_search(self,srv_no):
        try:

            bus_ser_srch = self.wait.until(EC.visibility_of_element_located((By.XPATH,f"//*[contains(@class,'Routeid') and contains(.,'{srv_no}')]")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bus_ser_srch)
            print(f"Service no {srv_no} Bus found ")
            parent_div = bus_ser_srch.find_element(*self.PARENT_DIV)
            view_seats = parent_div.find_element(*self.VIEW_SEATS_BUTTON_XPATH)
            view_seats.click()
            return True
        except TimeoutException:
            return False 


    def boarding_point_select(self,data):
        bd_point = self.wait.until(EC.visibility_of_element_located(self.BOARDING_POINT_ID))
        bd_point.click()
        bd_point.send_keys(data,Keys.RETURN)
        
    def dropping_point_select(self,data):
        dp_point = self.wait.until(EC.visibility_of_element_located(self.DROPPING_POINT_ID))
        dp_point.click()
        dp_point.send_keys(data,Keys.RETURN)

    def bp_dp_submit(self):
        bp_dp_submit = self.driver.find_element(*self.BP_DP_SUBMIT_XPATH)
        bp_dp_submit.click()
    
    def seat_check(self,seat_no):
        seat_sel = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH,f"//*[contains(@class,'available_seat') and .//text()= '{seat_no}']")))
        seat_class = seat_sel.get_attribute('class') 
    
        if 'available_seat' in seat_class:
            print(f"Seat no {seat_no} is  available")
            self.driver.find_element(*self.SEAT_CONTINUE_XPATH).click()
            return f"Seat no {seat_no} is available"
        else:
            print(f"Seat no {seat_no} is not available")
            return f"Seat no {seat_no} is not available"




    