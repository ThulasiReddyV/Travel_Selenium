import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_to_booking_page import Base_to_Booking_page
from conftest import load_test_data 


@pytest.mark.parametrize("data",load_test_data(),ids=[d["test_case_id"] for d in load_test_data()])
def test_001_booking_page(driver:WebDriver):
    home = Base_to_Booking_page(driver)
    home.nav_to_booking()
    
    home.windows_count_and_handle()
    home.close_discount_pop_up()
    

    assert "TGSRTC Online Bus Ticket Booking| Fast & Easy Ticket Booking" in home.get_titile()