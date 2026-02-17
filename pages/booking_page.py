from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from pages.base_to_booking_page import Base_to_Booking_page
#import pytest
import datetime
import time
#from conftest import  test_data_load 


class Booking_page(Base_to_Booking_page):
    
    FROM_TXT_XPATH = (By.XPATH,'//*[@id="rc_select_0"]')
    TO_TXT_XPATH = (By.XPATH,'//*[@id="rc_select_1"]')
    DOJ_SEL_FRAME_XPATH = (By.XPATH,'//*[@id="depart"]/div[1]')
    DEPART_SEL_XPATH = (By.XPATH,'/html/body/div[4]/div/div/div')
    NEXT_MONTH_BUTTON_XPATH = (By.XPATH,'//*[span[@class="ant-picker-next-icon"]]')
    NO_BUS_DISPLAY= (By.XPATH,'//*[text()="No Buses available for the Day!"]')
    #DATE_OF_JOURNEY = (By.XPATH,f'//*[@title = "{test_data_load["Date_of_journey"]}"]')
    SUBMIT_BUTTON_XPATH = (By.XPATH,'//*[@id= "gt-search"]')
    SERVICES_INFO_XPATH = (By.XPATH,'//*[span[text() ="Total Services "]]/parent::div')
    SERVICES_INFO_XPATH_2 = (By.XPATH,'//*[span[text() ="Total Services "]]')
    NO_SERVICES_INFO_XPATH = (By.XPATH,'//*[h1]')
    

    def from_select(self,data):
        #from_ele = self.wait.until(EC.visibility_of_element_located(self.FROM_TXT_XPATH))
        from_ele = self.wait.until(EC.visibility_of_element_located(self.FROM_TXT_XPATH))
        from_ele.click()
        from_ele.clear()
        from_ele.send_keys(data)
        self.wait.until(EC.visibility_of_element_located((By.XPATH,f'//*[@title="{data.upper()}"]'))).click()
        print(f"From {data.upper()} selected")

    def to_select(self,data):
        #to_ele = self.wait.until(EC.visibility_of_element_located(self.TO_TXT_XPATH))
        to_ele = self.wait.until(EC.visibility_of_element_located(self.TO_TXT_XPATH))
        to_ele.click()
        to_ele.send_keys(data)
        self.wait.until(EC.visibility_of_element_located((By.XPATH,f'//*[@title="{data.upper()}"]'))).click()
        print(f"TO {data.upper()} selected")



    def calender_check(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.DOJ_SEL_FRAME_XPATH))
            print("calender found")
        except:
            print('cal not found')
            cal_frame = self.wait.until(EC.visibility_of_element_located(self.DEPART_SEL_XPATH))
            cal_frame.click()
            print('cal clicked')


    def past_date(self):
        print("Past date")
        past_date_msg = "Past Date is selected"
        return past_date_msg
    
     
    def in_month(self,data):
        try:
            date_of_jour = WebDriverWait(self.driver,2).until(EC.visibility_of_element_located((By.XPATH,f'//*[@title = "{data}"]')))
            date_of_jour.click()
            print(f"Date {data} is selected")
            return True
        except:
            self.next_month(data)

    def next_month(self,data):
        nxt_month_btn = self.driver.find_element(*self.NEXT_MONTH_BUTTON_XPATH)
        nxt_month_btn.click()
        self.in_month(data)

    def submit_travel_details(self):
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON_XPATH))
        submit_btn.click()
        print("submit clicked")    

    def seats_buses_count(self):
        print("seats page ")
        #WebDriverWait(self.driver,30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        #time.sleep(10)
        prev_text = "Nothing"
        
        try:
            self.driver.find_element(*self.SERVICES_INFO_XPATH)
            #self.wait.until(EC.visibility_of_element_located(self.SERVICES_INFO_XPATH))

            while True:
                avb_buses_seats = self.driver.find_element(*self.SERVICES_INFO_XPATH_2)
                current_text = avb_buses_seats.text
                #print(f"{avb_buses_seats.text}")
                
                if current_text == prev_text and current_text !="Nothing":
                    break
                prev_text = current_text
                time.sleep(1.5)

            print(f"{avb_buses_seats.text}")
            return avb_buses_seats

        except NoSuchElementException:
            no_srv_msg = self.driver.find_element(*self.NO_SERVICES_INFO_XPATH)
            return no_srv_msg

        
        
        
            
        