import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_to_booking_page import Base_to_Booking_page

def test_001_booking_page(driver:WebDriver):
    home = Base_to_Booking_page(driver)
    home.nav_to_booking()
    home.windows_count()

    home.window_handle()
    home.close_discount_pop_up()
    

    assert "TGSRTC Online Bus Ticket Booking| Fast & Easy Ticket Booking" in home.get_titile()