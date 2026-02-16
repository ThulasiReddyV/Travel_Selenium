import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.booking_page import Base_to_Booking_page
from pages.booking_page import Booking_page
from pages.bus_and_seat_page import Bus_and_Seat_Selection
from conftest import  test_data_load 
from datetime import datetime
import time

@pytest.mark.parametrize("data",test_data_load())
def test_201_bus_and_seat_select(driver:WebDriver,data):
    home = Base_to_Booking_page(driver)
    
    home.nav_to_booking()
    home.windows_count_and_handle()
    time.sleep(5)

    booking = home.close_discount_pop_up()
    time.sleep(2)
    booking.from_select(data["from_loc"])
    booking.to_select(data["to_loc"])
    booking.calender_check()

    selected_date = datetime.strptime(data["Date_of_journey"],"%Y-%m-%d")
    today = datetime.today()
    if selected_date.date() < today.date():
        assert data["error_message"] in booking.past_date()
    else:
        booking.in_month(data["Date_of_journey"])
        booking.submit_travel_details()

        buses_data = booking.seats_buses_count()
        if data["error_message"] in buses_data.text:
            assert False, buses_data.text
        else:
            bus_seat = buses_data

            bus_avi = bus_seat.bus_search(data["bus_ser_no"])
            if bus_avi is False:
                assert bus_avi,data["error_message"]
            else:

                bus_seat.boarding_point_select(data["boarding_pt"])
                bus_seat.dropping_point_select(data["dropping_pt"])
                bus_seat.bp_dp_submit()
                seat_check = bus_seat.seat_check(data["seat_no"])
                if "not available" in seat_check:
                    assert data["error_message"] in seat_check
                """else:"""



