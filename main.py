from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import base64
from io import BytesIO
from PIL import Image
import os
import login
from pathlib import Path
import json
import subprocess
import moocs

def login_school(num: int):
    if num == 0:
        login.CGU(driver, ACCOUNT, PASSWORD)
    elif num == 1:
        login.CLU(driver, ACCOUNT, PASSWORD)

schoool_list = ["長庚大學", "致理科技大學"]
PROFILE_PATH = Path("dependence\Profile")
driver = webdriver.Edge()
driver.set_window_size(1900, 1080)


SCHOOL_NUM = 0


ACCOUNT, PASSWORD = "", ""


login_school(SCHOOL_NUM)

driver.implicitly_wait(10)

moocs.auto_exam(driver)