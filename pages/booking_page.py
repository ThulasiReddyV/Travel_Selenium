from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_to_booking_page import Base_to_Booking_page


class Booking_page(Base_to_Booking_page):
    
    FROM_CITY = (By.XPATH,'//*[@id="rc_select_0"]')
    TO_CITY = (By.XPATH,'//*[@id="rc_select_1"]')
    DOJ_SEL = (By.XPATH,'//*[@id="depart"]/div[1]')
    CALENDER_SEL = (By.XPATH,'/html/body/div[4]/div/div/div')
    #DATE_OF_JOURNEY = (By.XPATH,f'//*[@title = "{test_data_load["Date_of_journey"]}"]')
    SUBMIT_BUTTON = (By.XPATH,'//*[@id= "gt-search"]')


    def from_to_select(self,test_data_load):
        from_ele = self.wait.until(EC.visibility_of_element_located(self.FROM_CITY))
        from_ele.click()
        from_ele.send_keys(test_data_load["from_loc"],Keys.RETURN)    
        print("from selected")


        to_ele = self.wait.until(EC.visibility_of_element_located(self.TO_CITY))
        to_ele.click()
        to_ele.send_keys(test_data_load["to_loc"],Keys.RETURN)
        print("to selected")


    def date_select(self,test_data_load):
        try:
            self.wait.until(EC.visibility_of_element_located(self.DOJ_SEL))
            print("calender found")
        except:
            print('cal not found')
            cal_frame = self.wait.until(EC.element_to_be_clickable(self.CALENDER_SEL))
            cal_frame.click()
            print('cal clicked')

        date_of_jour = self.wait.until(EC.visibility_of_element_located((By.XPATH,f'//*[@title = "{test_data_load["Date_of_journey"]}"]')))
        date_of_jour.click()
        print("calender selected")

    def submit_travel_details(self):
        submit_btn = self.wait.until(EC.visibility_of_element_located(self.SUBMIT_BUTTON))
        submit_btn.click()
        print("submit clicked")


    def seats_buses_count(self):
        print("seats page ")
        try:
            avb_buses_seats = self.wait.until(EC.visibility_of_element_located((By.XPATH,'//*[span[text() ="Total Services "]]/parent::div')))
            print(f"{avb_buses_seats.text}")

            from pages.bus_and_seat_page import Bus_and_Seat_Selection
            Bus_and_Seat_Selection(self.driver)
            
        except Exception as e:
            print(f"No Buses available for the Day! {e}")
            raise