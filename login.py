from selenium.webdriver.common.by import By
from selenium import webdriver
from PIL import Image
import base64
from io import BytesIO
import pytesseract
import numpy as np
def CGU(driver: webdriver.Edge, ACCOUNT, PASSWORD):
    URL = "https://ids.cgu.edu.tw/nidp/idff/sso?id=3&sid=1&option=credential&sid=1&target=https%3A%2F%2Fel.cgu.edu.tw%2F%3F"
    driver.get(URL)
    driver.implicitly_wait(10)
    account_form = driver.find_element(By.ID, "exampleInputEmail1")
    account_form.clear()
    account_form.send_keys(ACCOUNT)
    password_form = driver.find_element(By.ID, "exampleInputPassword1")
    password_form.clear()
    password_form.send_keys(PASSWORD)
    driver.execute_script("imageSubmit()")
    driver.implicitly_wait(10)
    myCourse_form = driver.find_element(By.PARTIAL_LINK_TEXT, "我的課程")
    myCourse_form.click()

def CLU(driver: webdriver.Edge, ACCOUNT, PASSWORD):
    while True:
        URL = "https://dlc.chihlee.edu.tw/mooc/login.php"
        driver.get(URL)
        driver.implicitly_wait(10)
        account_form = driver.find_element(By.ID, "username")
        account_form.clear()
        account_form.send_keys(ACCOUNT)
        password_form = driver.find_element(By.ID, "password")
        password_form.clear()
        password_form.send_keys(PASSWORD)
        image_element = driver.find_element(By.ID, "captcha-picture").find_element(By.TAG_NAME, "img")
        base64_script = """
    var img = arguments[0];
    var canvas = document.createElement('canvas');
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    return canvas.toDataURL('image/png').substring(22);
    """
        base64_data = driver.execute_script(base64_script, image_element)
        image_bytes = base64.b64decode(base64_data)
        image = Image.open(BytesIO(image_bytes))
        img_pixel = np.array(image)
        for y, column in enumerate(img_pixel):
            for x, pixel in enumerate(column):
                rgb = pixel[0:3]
                if rgb.max() - rgb.min() <= 30 and (float(rgb[0])+float(rgb[1])+float(rgb[2]))/3 < 200:
                    pass
                else:img_pixel[y][x] = [255, 255, 255, 255]
        pytesseract.pytesseract.tesseract_cmd = r"dependence\Tesseract-OCR\tesseract.exe"
        verify_code = str(pytesseract.image_to_string(img_pixel)).replace(' ', '')
        verify_form = driver.find_element(By.ID, "captcha")
        verify_form.send_keys(verify_code)
        driver.implicitly_wait(10)
        try:
            driver.find_element(By.ID, "SYS_06_01_003")
            break
        except:
            continue