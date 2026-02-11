import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.booking_page import Base_to_Booking_page
from pages.booking_page import Booking_page

def test_002_booking(driver:WebDriver,test_data_load):
    home = Base_to_Booking_page(driver)
    home.nav_to_booking()
    home.windows_count_and_handle()
    
    booking = home.close_discount_pop_up()
    booking.from_to_select(test_data_load)
    booking.date_select(test_data_load)
    booking.submit_travel_details()

    assert "results" in driver.current_url,"Did not to seats page"
