from selenium import webdriver
import pytest
import json
import os
from datetime import datetime

def read_json(filename):
    path = os.path.join(os.path.dirname(__file__),"config",filename)
    with open(path) as f:
        return json.load(f)

@pytest.fixture(scope="session")
def config_load():
    return read_json("config.json")
    
#@pytest.fixture(scope="session")
def testcases_data_load():
    return read_json("test_data.json")

@pytest.fixture(scope="function")
def driver(config_load):
    driver= webdriver.Chrome()
    driver.get(config_load["base_url"])
    driver.maximize_window()
    yield driver
    driver.quit()

