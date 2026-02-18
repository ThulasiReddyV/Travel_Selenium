from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

import pytest
import json
import os
from datetime import datetime
from conftest import *



def timestamp():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return timestamp



def take_screenshot(driver:WebDriver,screenshot_name):
    base_dir = os.getcwd()   
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = os.path.join(base_dir,"screenshots",timestamp)
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir,screenshot_name)
    driver.save_screenshot(f"{screenshot_path}.png")
    