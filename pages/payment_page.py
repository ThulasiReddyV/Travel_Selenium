from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from pages.passenger_details_page import Passenger_Details
from datetime import datetime
from conftest import *
from utilities import *
import time

class Payments_page(Passenger_Details):

    JOURNEY_DETAILS_VERIFY_XPATH = (By.XPATH,"//h4[text()='Journey Details']/following::table[1]//tr")
    PASS_DETAILS_VERIFY_XPATH = (By.XPATH,"//h4[text()='Passengers']/following::table[1]//tbody/tr")
    PASS_EMAIL_MOBILE_VERIFY_XPATH = (By.XPATH,"//h4[text()='Passengers']/following::div[contains(@class,'ant-col')]")
    PAYMENT_OPTION_XPATH = (By.XPATH,'//span[contains(@class,"ant-radio") and .//*[@value="26"]]')
    PROCEED_TO_PAYMENT_XPATH = (By.XPATH,'//*[span[text()="Proceed to Payment"]]')
    CNF_DETAILS_XPATH = (By.XPATH,"//*[span[text()='OK']]")
    PAYMENT_POP_XPATH = (By.XPATH,'//span[contains(@class,"ptm-overlay-container")]')
    PAYMENT_POP_CLOSE_XPATH = (By.XPATH,'//span[contains(@class,"ptm-cross")]')
    QR_CLASS = (By.CLASS_NAME,"ptm-qr-img-container")

    
    
    def get_booking_summary(self):

        journey_details = self.driver.find_elements(*self.JOURNEY_DETAILS_VERIFY_XPATH)
        journey_ui = {}
    
        for ele in journey_details:
            header = ele.find_element(By.TAG_NAME,"th").text.strip().lower()
            value = ele.find_element(By.TAG_NAME,"td").text.strip()

            if header == "journey":
                from_to = value.split()
                journey_ui["from_loc"] = from_to[0].strip()
                journey_ui["to_loc"] = from_to[1].strip()

            elif header == "date":
                journey_ui["date_of_journey"] = value

            elif header == "service no":
                journey_ui["bus_ser_no"] = value

            elif header == "boarding":
                parts = value.split("-")
                value = parts[1].strip()
                journey_ui["boarding_pt"] = value

            elif header == "dropping":
                parts = value.split("-")
                value = parts[1].strip()
                journey_ui["dropping_pt"] = value


        passenger_row = self.driver.find_element(*self.PASS_DETAILS_VERIFY_XPATH)
        cols = passenger_row.find_elements(By.TAG_NAME, "td")

        journey_ui["seat_no"] = cols[0].text.strip()

        name_text = cols[1].text.strip().split()
        title = name_text[0].strip().lower().replace(".", "")

        gender_map = {
            "mr": "Male",
            "mrs": "Female",
            "miss": "Female"
        }

        journey_ui["pass_gender"] = gender_map.get(title, "")
        journey_ui["pass_name"] = " ".join(name_text[1:])
        journey_ui["pass_age"] = cols[2].text.strip()

        # Email & Mobile
        pass_email = ""
        pass_mobile = ""

        email_mobile_divs = self.driver.find_elements(*self.PASS_EMAIL_MOBILE_VERIFY_XPATH)

        for div in email_mobile_divs:
            text = div.text.strip()
            if "@" in text:
                pass_email = text
            elif text.isdigit():
                pass_mobile = text

        journey_ui["pass_email"] = pass_email
        journey_ui["pass_mobile"] = pass_mobile

    
        #print(journey_ui)
        return journey_ui

    def merge_journey_and_booking_summary(self):

        booking = self.verify_journey_details()
        journey = self.get_booking_summary()
        print(f"Booking->{booking}")
        print(f"Journey->{journey}")
        ui_dict = {}
        mismatches = []

        all_keys = set(booking.keys()).union(set(journey.keys()))

        for key in all_keys:

            if key in booking and key in journey:
                if booking[key] == journey[key]:
                    ui_dict[key] = booking[key]
                else:
                    print(f"Value mismatch for key '{key}' -> Expected: {booking[key]} | Actual: {journey[key]}")
                    mismatches.append(f"{key}: Expected={booking[key]} | Actual={journey[key]}"
                )

            elif key in booking:
                ui_dict[key] = booking[key]

            elif key in journey:
                ui_dict[key] = journey[key]
        
        if mismatches:
            raise AssertionError("Mismatches found:\n" + "\n".join(mismatches))
        
        return ui_dict
    
    def comp_test_case_and_ui(self,testcase):
        print(f"Test-{testcase}")
        ignore_keys =["test_case_id","error_or_message" ]

        filter_dict = {k:v for k,v in testcase.items() if k not in ignore_keys }
        print(f"Filterd-{filter_dict}")

        ui_dict = self.merge_journey_and_booking_summary()
        print(f"UI->{ui_dict}")

        if filter_dict == ui_dict:
            return True
        else:
            return False
    



    def confirm_booking_summary(self):
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