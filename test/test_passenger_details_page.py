import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.booking_page import Base_to_Booking_page
from pages.booking_page import Booking_page
from pages.bus_and_seat_page import Bus_and_Seat_Selection
from pages.passenger_details_page import Passenger_Details

from utilities import *
from datetime import datetime
import time



@pytest.mark.parametrize("data",load_test_data(),ids=[d["test_case_id"] for d in load_test_data()])
def test_301_passenger_details(driver:WebDriver,data):
    home = Base_to_Booking_page(driver)
    
    home.nav_to_booking()
    home.windows_count_and_handle()
    #time.sleep(5)
    home.close_discount_pop_up()
    
    booking = Booking_page(driver)
    #time.sleep(2)
    booking.from_select(data["from_loc"])
    booking.to_select(data["to_loc"])
    booking.calender_check()

    selected_date = datetime.strptime(data["Date_of_journey"],"%Y-%m-%d")
    today = datetime.today()
    if selected_date.date() < today.date():
        assert data["error_or_message"] in booking.past_date()
    else:
        booking.in_month(data["Date_of_journey"])
        booking.submit_travel_details()

        buses_data = booking.seats_buses_count()
        if data["error_or_message"] in buses_data:
            assert True
        else:
            bus_seat = Bus_and_Seat_Selection(driver)
            bus_avail = bus_seat.bus_search(data["bus_ser_no"])
            if bus_avail is False:
                assert True,data["error_or_message"]
            else:

                bus_seat.boarding_point_select(data["boarding_pt"])
                bus_seat.dropping_point_select(data["dropping_pt"])
                bus_seat.bp_dp_submit()
                seat_check = bus_seat.seat_check(data["seat_no"])
                if "unavailable" in seat_check:
                    assert True, data["error_or_message"] 
                else:
                    passenger = Passenger_Details(driver)
                    passenger.gender(data["pass_gender"])
                    passenger.enter_pass_name(data["pass_name"])
                    passenger.enter_pass_age(data["pass_age"])
                    passenger.enter_pass_email(data["pass_email"])
                    passenger.enter_pass_mobile_no(data["pass_mobile"])
                    

