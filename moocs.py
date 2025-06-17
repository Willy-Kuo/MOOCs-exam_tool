import time
from selenium.webdriver.common.by import By
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from io import BytesIO
from PIL import Image
import base64
from pathlib import Path
import PDF

def return_frontPage(driver: webdriver.Edge):
    driver.switch_to.parent_frame()
    wait_exists(driver, name="s_sysbar")
    driver.switch_to.frame("s_sysbar")
    driver.execute_script("goPersonal()")

def to_classListPage(driver: webdriver.Edge):
    driver.switch_to.parent_frame()
    wait_exists(driver, name="mooc_sysbar")
    driver.switch_to.frame("mooc_sysbar")
    driver.find_element(By.ID, "SYS_06_01_002")

def wait_exists(driver: webdriver.Edge, id: str=None, name:str=None, frame=None):
    while True:
        if id != None:
            element_exists = driver.execute_script(f"return document.getElementById('{id}') !== null;")
        else:
            element_exists = driver.execute_script(f"return document.getElementsByName('{name}').length > 0;")
        if element_exists == True:
            if frame != None:
                driver.switch_to.frame(frame)
            break
        time.sleep(2)

def get_course_names_and_course_elements(driver: webdriver.Edge):
    course_elements = [div_element.find_element(By.TAG_NAME, "a") for div_element in driver.find_elements(By.TAG_NAME, "div") if div_element.get_attribute("class")=="text-left"][1:]
    course_names = [element.get_attribute("text") for element in course_elements]
    return course_elements, course_names

class ClickSidebarElement():
    def __init__(self, driver: webdriver.Edge):
        self.driver = driver
        driver.switch_to.parent_frame()
    def to_exam(self):
        self.driver.switch_to.frame("mooc_sysbar")
        element = self.driver.find_element(By.ID, "SYS_04_02_002")
        element.click()


def auto_exam(driver: webdriver.Edge):
    # to exam list
    to_classListPage(driver)
    driver.switch_to.parent_frame()
    driver.switch_to.frame("s_main")
    course_elements, course_names = get_course_names_and_course_elements(driver)
    while True:
        try:
            os.system("cls")
            for n, name in enumerate(course_names):
                print(f"[{n}]{name}", end='  ')
            print()
            choose_course_index = int(input("Enter number:"))
            course_elements[choose_course_index].click()
            break
        except:
            continue
    ClickSidebarElement(driver).to_exam()

    # choose exam
    driver.implicitly_wait(2)
    driver.switch_to.parent_frame()
    driver.switch_to.frame("s_main")
    exam_titles = [element.find_element(By.TAG_NAME, "span").text for element in driver.find_elements(By.CSS_SELECTOR, ".element.title")]
    testing_botton = driver.find_elements(By.CSS_SELECTOR, ".process-btn.pay.active")
    while True:
        try:
            os.system("cls")
            for n, name in enumerate(exam_titles):
                print(f"[{n}]{name}", end='  ')
            print()
            choose_exam_index = int(input("Enter number:"))
            testing_botton[choose_exam_index].click()
            break
        except:
            continue











def download_handout(driver: webdriver.Edge):
    def get_chapters():
        driver.switch_to.parent_frame()
        wait_exists(driver, name="s_catalog")
        driver.switch_to.frame("s_catalog")
        wait = WebDriverWait(driver, 10)
        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        wait_exists(driver, "pathtree", frame=iframe)
        chapter_elements = []
        chapter_names = []
        for span_element in driver.find_elements(By.TAG_NAME, "span"):
            try:
                if span_element.find_element(By.TAG_NAME, "div").get_attribute("class") != None:
                    a_element = span_element.find_element(By.TAG_NAME, "a")
                    chapter_elements.append(a_element)
                    chapter_names.append(a_element.get_attribute("text"))
            except:
                continue
        return chapter_names, chapter_elements
    while True:
        to_classListPage(driver)
        driver.switch_to.parent_frame()
        driver.switch_to.frame("s_main")
        course_elements, course_names = get_course_names_and_course_elements(driver)
        time.sleep(2)
        try:
            os.system("cls")
            for n, name in enumerate(course_names):
                print(f"[{n}]{name}", end='  ')
            print()
            choose_course_index = int(input("Enter number:"))
            course_elements[choose_course_index].click()
        except:
            continue
        print("reading...")
        driver.implicitly_wait(10)
        time.sleep(5)

        chapter_names, chapter_elements = get_chapters()
        for n, name in enumerate(chapter_names):
            print(f"[{n}]{name}", end='  ')
        print()
        choose_chapter_index = int(input("Enter number:"))
        chapter_elements[choose_chapter_index].click()

        time.sleep(5)
        driver.switch_to.default_content()
        driver.switch_to.frame("s_main")
        wait_exists(driver, "page1")
        viewer_element = driver.find_element(By.ID, "viewer")
        

        next_button = driver.find_element(By.ID, "next")
        total_page = int(driver.find_element(By.ID, "pageNumber").get_attribute("max"))
        images = []
        
        for n in range(1, total_page+1):
            for element in viewer_element.find_elements(By.TAG_NAME, "div"):
                if element.get_attribute("class")=="page" and element.get_attribute("data-page-number")==str(n):
                    wait_exists(driver, id=f"page{n}")
                    canva_element = element.find_element(By.TAG_NAME, "div")
                    break
            # canva_element = [element for element in viewer_element.find_elements(By.TAG_NAME, "div") if element.get_attribute("class")=="page" and element.get_attribute("data-page-number")==str(n)][0].find_element(By.TAG_NAME, "div")
            
            canvas_base64 = driver.execute_script("""
                var canvas = arguments[0].querySelector("canvas");
                return canvas.toDataURL("image/png");
            """, canva_element)


            canvas_bytes = base64.b64decode(canvas_base64.split(",")[1])
            image = Image.open(BytesIO(canvas_bytes))
            save_path = f"output\image\{n}.png"
            image.save(save_path)
            images.append(save_path)
            if n != total_page:
                next_button.click()
                driver.implicitly_wait(10)
                time.sleep(2)
        # img_width, img_height = image.size
        # canva_scale = float(f"{img_width/img_height:.1f}")
        # print(canva_scale)
        # base_size = 13.33
        # if canva_scale >= 1:
        #     canva_size = (base_size, base_size / canva_scale)
        # elif canva_scale <= 1:
        #     canva_size = (base_size * canva_scale, base_size)
        PDF.createPDF(images, f"output\{chapter_names[choose_chapter_index]}.pdf")
        # pptx = PPT.createPPT(images, canva_size)
        # pptx.save(f"output\{chapter_names[choose_chapter_index]}.pptx")
        for image in Path("output\image").iterdir():
            image.unlink()

        print("[0]Continue  [1]Leave")
        Again = int(input("Enter number:"))
        if Again:
            break
        return_frontPage(driver)
        to_classListPage(driver)
        time.sleep(5)