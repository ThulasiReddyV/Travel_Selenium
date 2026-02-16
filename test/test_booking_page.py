import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.booking_page import Base_to_Booking_page
from pages.booking_page import Booking_page
from conftest import  test_data_load 
from datetime import datetime
import time

@pytest.mark.parametrize("data",test_data_load())
def test_101_booking(driver:WebDriver,data):
    home = Base_to_Booking_page(driver)
    
    home.nav_to_booking()
    home.windows_count_and_handle()
    time.sleep(2)

    booking = home.close_discount_pop_up()
    time.sleep(2)
    booking.from_select(data["from_loc"])
    booking.to_select(data["to_loc"])
    booking.calender_check()

    selected_date = datetime.strptime(data["Date_of_journey"],"%Y-%m-%d")
    today = datetime.today()
    if selected_date.date() < today.date():
        assert "Past Date" in booking.past_date()
    else:
        booking.in_month(data["Date_of_journey"])
        booking.submit_travel_details()
        buses_data = booking.seats_buses_count()
        if type(buses_data) == 'str':
            assert "No Buses" in buses_data
        """else:
            assert "Total" in buses_data"""


            
        #assert "results" in driver.current_url,"Did not to seats page"
