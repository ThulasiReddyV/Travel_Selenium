import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.booking_page import Base_to_Booking_page
from pages.booking_page import Booking_page
from conftest import  test_data_load 
from datetime import datetime

@pytest.mark.parametrize("data",test_data_load())
def test_101_booking(driver:WebDriver,data):
    home = Base_to_Booking_page(driver)
    
    home.nav_to_booking()
    home.windows_count_and_handle()

    booking = home.close_discount_pop_up()
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
        if booking.no_of_buses_check() == False:
            assert "No Buses" in booking.above_2_months_no_route_error()
        else:

            booking.seats_buses_count()

            
        assert "results" in driver.current_url,"Did not to seats page"
