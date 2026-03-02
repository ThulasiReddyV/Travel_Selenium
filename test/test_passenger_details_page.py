import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.booking_page import Base_to_Booking_page
from pages.booking_page import Booking_page
from pages.bus_and_seat_page import Bus_and_Seat_Selection
from pages.passenger_details_page import Passenger_Details

from utilities import *
from datetime import datetime
import time


test_data = load_test_data()
@pytest.mark.parametrize("data", test_data,ids=[d["test_case_id"] for d in test_data])

def test_301_passenger_details(driver:WebDriver,data):
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
        assert  expected_msg.lower() in actual_msg.lower() ,\
            f"Expected: {expected_msg} to be in {actual_msg}" 
    else:
        booking.in_month(data["date_of_journey"])
        booking.submit_travel_details()

        buses_data = booking.seats_buses_count()
        if data["error_or_message"].lower() in buses_data.lower():
            assert data["error_or_message"].lower() in buses_data.lower(), \
                f"Expected:'{data["error_or_message"]}', not found in '{buses_data}'"
        else:
            bus_seat = Bus_and_Seat_Selection(driver)
            bus_avail = bus_seat.bus_search(data["bus_ser_no"])
            if "unavaialble" in bus_avail:
                assert data["error_or_message"].lower() in bus_avail.lower(), \
                    f"Expected:'{data["error_or_message"]}', not found in '{bus_avail}'"
            else:

                bus_seat.boarding_point_select(data["boarding_pt"])
                bus_seat.dropping_point_select(data["dropping_pt"])
                bus_seat.bp_dp_submit()
                seat_check = bus_seat.seat_check(data["seat_no"])
                if "e_ticketing_seat" in seat_check or "onhld" in seat_check: 
                    assert "unavailable" in data["error_or_message"].lower() and "unavailable" in seat_check.lower(), \
                        f"'unavailable' not found in '{data["error_or_message"]}', '{seat_check}'"
                else: 
                    passenger = Passenger_Details(driver)
                    passenger.select_gender(data["pass_gender"])
                    passenger.enter_pass_name(data["pass_name"])
                    passenger.enter_pass_age(data["pass_age"])
                    passenger.enter_pass_email(data["pass_email"])
                    passenger.enter_pass_mobile_no(data["pass_mobile"])
                    passenger.verify_journey_details()
                    passenger.payment_option_select()
                    
                    assert passenger.error_check(),\
                        "Passenger Data Not entered"

