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
    BOOK_BUTTON_NAME = (By.CLASS_NAME,"book-your-ticket_button__l2bvh")
    POP_UP_ID = (By.ID,"fade")
    POP_UP_CLOSE_XPATH = (By.XPATH,'//*[@id="close"]/div')
    FROM_TXT_XPATH = (By.XPATH,'//*[@id="rc_select_0"]')
    

    def nav_to_booking(self):

        book_now_btn = self.wait.until(EC.element_to_be_clickable(self.BOOK_BUTTON_NAME))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", book_now_btn)

        book_now_btn.click()

    def get_titile(self):
        return self.driver.title
    
    def windows_count_and_handle(self):
        self.wait.until(EC.number_of_windows_to_be(2))
        self.driver.switch_to.window(self.driver.window_handles[1])
        print("Switched to window")


    def close_discount_pop_up(self):
        #WebDriverWait(self.driver,30).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        try: 
            pop_up_ele = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located(self.POP_UP_ID))
            pop_up_close = self.wait.until(EC.visibility_of_element_located(self.POP_UP_CLOSE_XPATH))
            pop_up_close.click()
            print("Pop up closed")
            WebDriverWait(self.driver,3).until(EC.invisibility_of_element(self.POP_UP_ID))
            return True
        except TimeoutError:
            print("No pop up closed")
            return False
        
        
        
        