from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException

from pages.booking_page import Booking_page

class Bus_and_Seat_Selection(Booking_page):

    PARENT_DIV = (By.XPATH,'./ancestor::div[contains(@class,"ant-col-3")]')
    VIEW_SEATS_BUTTON_XPATH = (By.XPATH,'./following-sibling::div[contains(@class,"ant-col-4")]//button[@type = "button"]')
    
    BOARDING_POINT_DPD_ID = (By.ID,"boardingPoint")
    DROPPING_POINT_DPD_ID = (By.ID,"droppingPoint")
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
        bd_point_dpd = self.wait.until(EC.visibility_of_element_located(self.BOARDING_POINT_DPD_ID))
        bd_point_dpd.click()
        bd_point_dpd.send_keys(data)
        bd_point = self.wait.until(EC.element_to_be_clickable((By.XPATH,f'//*[contains(@class,"ant-select-item-option-content")and contains(normalize-space(.),"{data.upper()}")]')))
        bd_point.click()
        print(f"Boarding Point and Time {bd_point.text}")
        
    def dropping_point_select(self,data):
        dp_point_dpd = self.wait.until(EC.visibility_of_element_located(self.DROPPING_POINT_DPD_ID))
        dp_point_dpd.click()
        dp_point_dpd.send_keys(data)
        dp_point = self.wait.until(EC.element_to_be_clickable((By.XPATH,f'//*[contains(@class,"ant-select-item-option-content")and contains(normalize-space(.),"{data.upper()}")]')))
        dp_point.click()
        print(f"Dropping Point and Time {dp_point.text}")



    def bp_dp_submit(self):
        bp_dp_submit = self.driver.find_element(*self.BP_DP_SUBMIT_XPATH)
        bp_dp_submit.click()
    
    def seat_check(self,seat_no):
        print("Seat Selection")
        seat_sel = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH,f'//*[@rowspan="1" and normalize-space(.)= "{seat_no}"]')))
        child_of_seat_sel = seat_sel.find_element(By.XPATH,".//*")
        seat_class = child_of_seat_sel.get_attribute('class') 
        print(seat_class)
         
        if "available_seat" in seat_class:

            if "ladies" in seat_class:
                print(f"Seat no {seat_no} is available for female")
                seat_sel.click()
                self.driver.find_element(*self.SEAT_CONTINUE_XPATH).click()
                return f"Seat no {seat_no} is available for female"
            elif "gents" in seat_class or "available_seat" == seat_class:
                print(f"Seat no {seat_no} is available")
                seat_sel.click()
                self.driver.find_element(*self.SEAT_CONTINUE_XPATH).click()
                return f"Seat no {seat_no} is available"
        elif "onhld_gents" == seat_class or "onhld_ladies" == seat_class:
            print(f"Seat no {seat_no} is {seat_class} and unavailable present")
            return f"Seat no {seat_no} is {seat_class} and unavailable present"
            
        elif seat_class == "e_ticketing_seat":
            print(f"Seat no {seat_no} is unavailable")
            return f"Seat no {seat_no} is unavailable"
        




    