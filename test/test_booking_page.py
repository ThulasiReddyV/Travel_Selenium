import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.booking_page import Base_to_Booking_page
from pages.booking_page import Booking_page
from conftest import  test_data_load 
import datetime

@pytest.mark.parametrize("data",test_data_load())
def test_101_booking(driver:WebDriver,data):
    home = Base_to_Booking_page(driver)
    
    home.nav_to_booking()
    home.windows_count_and_handle()

    booking = home.close_discount_pop_up()
    booking.from_select(data["from_loc"])
    booking.to_select(data["to_loc"])
    booking.calender_check()

    selected_date = datetime.strptime(data,"%Y-%m-%d")
    today = datetime.today()
    if selected_date.date() < today.date():
        assert booking.past_date_error(),"Past Date is selected"
    else:
        in_month(data)
    booking.date_selection(data["Date_of_journey"])
    #booking.submit_travel_details()

        
    booking.seats_buses_count()

    assert "results" in driver.current_url,"Did not to seats page"
