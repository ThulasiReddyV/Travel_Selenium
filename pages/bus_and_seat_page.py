from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.booking_page import Booking_page

class Bus_and_Seat_Selection(Booking_page):

    BOARDING_POINT_ID = (By.ID,"boardingPoint")
    DROPPING_POINT_ID = (By.ID,"droppingPoint")
    BP_DP_SUBMIT_XPATH = (By.XPATH,'//*[span[text()="Submit"]]')
    SEAT_CONTINUE_XPATH = (By.XPATH,'//*[span[text()="Continue"]]')

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
    
    def seat_check(self,data):
        seat_sel = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH,f"//*[contains(@class,'available_seat') and .//text()= '{data}']")))
        seat_class = seat_sel.get_attribute('class') 
    
        if 'available_seat' in seat_class:
            print(f"Seat no {data} is  available")
            self.seat_select(seat_sel)
        else:
            print(f"Seat no {data} is not available")
            return f"Seat no {data} is not available"


    def seat_select(self,seat_sel):
        seat_sel.click()
        self.driver.find_element(*self.SEAT_CONTINUE_XPATH).click()
        from pages.passenger_details_page import Passenger_Details
        return Passenger_Details(self.driver)


    