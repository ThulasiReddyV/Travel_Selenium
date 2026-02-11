from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Base_to_Booking_page:

    def __init__(self,driver : WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)

    #Navigate to Booking page from Base page
    BOOK_BUTTON = (By.CLASS_NAME,"book-your-ticket_button__l2bvh")
    POP_UP = (By.XPATH,'//*[@id="close"]/div')
    FROM_ELE = (By.XPATH,'//*[@id="rc_select_0"]')
    

    def nav_to_booking(self):
        book_now_btn = self.wait.until(EC.element_to_be_clickable(self.BOOK_BUTTON))
        book_now_btn.click()

    def get_titile(self):
        return self.driver.title
    
    def windows_count_and_handle(self):
        self.wait.until(EC.number_of_windows_to_be(2))
        self.driver.switch_to.window(self.driver.window_handles[1])
        print("move to window")


    def close_discount_pop_up(self):
        try: 
            pop_up_btn = WebDriverWait(self.driver,30).until(EC.element_to_be_clickable(self.POP_UP))
            pop_up_btn.click()
            print("pop up closed")

            from pages.booking_page import Booking_page
            return Booking_page(self.driver)
        except TimeoutError:
            return False
        
        
        