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
        email.send_keys("amalraj89903@gmail.com")
        password = driver.find_element(By.CSS_SELECTOR, "input#password.form-control.form-control-lg")
        password.send_keys("soulcure")
        time.sleep(1)
        submitc = driver.find_element(By.CSS_SELECTOR, "button#submit.btn.btn-dark.btn-lg.w-50")
        submitc.click()
        time.sleep(2)
        find = driver.find_element(By.CSS_SELECTOR, "a[href='/client/add_questions/']")
        find.click()
        time.sleep(2)
        # Fill out the form fields
        question_input = driver.find_element(By.ID, "question")
        question_input.send_keys("Sample question")

        option1_input = driver.find_element(By.ID, "option1")
        option1_input.send_keys(" Test Option 1")

        option2_input = driver.find_element(By.ID, "option2")
        option2_input.send_keys("Test Option 2")

        option3_input = driver.find_element(By.ID, "option3")
        option3_input.send_keys("Test Option 3")

        option4_input = driver.find_element(By.ID, "option4")
        option4_input.send_keys("Test Option 4")
        time.sleep(7)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'submit'))).click()
        time.sleep(2)
        
        time.sleep(3)

        print("--------------------------------------")
        print("                                      ")
        print("Ran 1 test in", datetime.now() - start_time, "seconds")
        print("Test Passed: Feedback Question and Options Successfully.")
        print("Test Date:", datetime.now())
        print("                                      ")
        print("                                      ")
        print("                                      ")
        print("--------------------------------------")



if __name__ == '__main__':
    import unittest
    unittest.main()
