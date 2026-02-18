from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


import json
import os
from datetime import datetime

TIMESTAMP = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

def read_json(filename):
    path = os.path.join(os.path.dirname(__file__),"config",filename)
    with open(path) as f:
        data = json.load(f)
        return data
    
def load_test_data():
    return read_json("test_data.json")

def timestamp():
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return timestamp

def take_screenshot(driver:WebDriver,screenshot_name):
    base_dir = os.getcwd()   
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = os.path.join(base_dir,"screenshots",TIMESTAMP)
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir,screenshot_name)
    driver.save_screenshot(f"{screenshot_path}.png")
    