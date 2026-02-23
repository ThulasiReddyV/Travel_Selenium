import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.booking_page import Base_to_Booking_page
from pages.booking_page import Booking_page
from conftest import  load_test_data 
from datetime import datetime
import time
test_data = load_test_data()
@pytest.mark.parametrize("data", test_data,ids=[d["test_case_id"] for d in test_data])

def test_101_booking(driver:WebDriver,data):
    home = Base_to_Booking_page(driver)
    
    home.nav_to_booking()
    home.windows_count_and_handle()
    #time.sleep(5)
    home.close_discount_pop_up()
    
    assert "TGSRTC Online Bus Ticket Booking| Fast & Easy Ticket Booking" in home.get_titile(), "Wrong Page loaded"

    booking = Booking_page(driver)
    #time.sleep(2)
    booking.from_select(data["from_loc"])
    booking.to_select(data["to_loc"])
    booking.calender_check()

    selected_date = datetime.strptime(data["date_of_journey"],"%Y-%m-%d")
    today = datetime.today()
    if selected_date.date() < today.date():
        actual_msg = data["error_or_message"]
        expected_msg = booking.past_date()
        assert  expected_msg in actual_msg ,\
            f"Expected: {expected_msg} to be in {actual_msg}" 
    else:
        booking.in_month(data["date_of_journey"])
        booking.submit_travel_details()

        buses_data = booking.seats_buses_count()
        if data["error_or_message"] in buses_data:
            assert data["error_or_message"] in buses_data, \
                f"Expected:'{data["error_or_message"]}', not found in '{buses_data}'"
