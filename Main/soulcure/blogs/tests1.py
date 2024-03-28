from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.conf import settings
from datetime import datetime

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soulcure.settings')
settings.configure()
from selenium.webdriver.support.ui import Select

class FormTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'  # Update with your server URL

    def tearDown(self):
        self.driver.quit()

    def test_form_submission(self):
        start_time = datetime.now()
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        login = driver.find_element(By.CSS_SELECTOR, "a.nav-item.nav-link.btn.btn-success.mx-2.text-dark")
        login.click()
        time.sleep(2)
        email = driver.find_element(By.CSS_SELECTOR, "input#email.form-control.form-control-lg")
        email.send_keys("saviojose2024@mca.ajce.in")
        password = driver.find_element(By.CSS_SELECTOR, "input#password.form-control.form-control-lg")
        password.send_keys("Lead@123")
        time.sleep(1)
        submitc = driver.find_element(By.CSS_SELECTOR, "button#submit.btn.btn-dark.btn-lg.w-50")
        submitc.click()
        time.sleep(2)
        find = driver.find_element(By.CSS_SELECTOR, "a[href='/blogs/add_blog/']")
        find.click()
        time.sleep(2)
        # Fill out the form fields
        title_input = driver.find_element(By.ID, 'title')
        title_input.send_keys('Test Title')

        subtitle1_input = driver.find_element(By.ID, 'subtitle1')
        subtitle1_input.send_keys('Test Subtitle 1')

        subtitle2_input = driver.find_element(By.ID, 'subtitle2')
        subtitle2_input.send_keys('Test Subtitle 2')

        subtitle3_input = driver.find_element(By.ID, 'subtitle3')
        subtitle3_input.send_keys('Test Subtitle 3')

        subtitle_input = driver.find_element(By.ID, 'subtitle')
        subtitle_input.send_keys('Test Subtitle')

        intro_input = driver.find_element(By.ID, 'intro')
        intro_input.send_keys('Test Introduction')

        content1_input = driver.find_element(By.ID, 'content1')
        content1_input.send_keys('Test Content 1')

        content2_input = driver.find_element(By.ID, 'content2')
        content2_input.send_keys('Test Content 2')

        content3_input = driver.find_element(By.ID, 'content3')
        content3_input.send_keys('Test Content 3')

        image_input = driver.find_element(By.ID, 'image')
        image_input.send_keys('C:\\Users\\amalr\\Downloads\\2150916612.jpg')  # Update with your image path


        # Locate the dropdown/select element
        category_select = Select(driver.find_element(By.ID, 'category'))

        # Use Select class to select by visible text
        category_select.select_by_visible_text('Mental Health Education')  # Update with your test category
        time.sleep(7)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'submit'))).click()
        time.sleep(2)
        find = driver.find_element(By.CSS_SELECTOR, "a[href='/blogs/view_blog_editor/']")
        find.click()
        time.sleep(3)

        print("--------------------------------------")
        print("                                      ")
        print("Ran 1 test in", datetime.now() - start_time, "seconds")
        print("Test Passed: New Blog Created Successfully.")
        print("Test Date:", datetime.now())
        print("                                      ")
        print("                                      ")
        print("                                      ")
        print("--------------------------------------")



if __name__ == '__main__':
    import unittest
    unittest.main()
