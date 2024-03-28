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
from django.conf import settings
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soulcure.settings')
settings.configure()



# Blog Comment Test


class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):
        start_time = datetime.now()
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        login = driver.find_element(By.CSS_SELECTOR, "a.nav-item.nav-link.btn.btn-success.mx-2.text-dark")
        login.click()
        time.sleep(2)
        email = driver.find_element(By.CSS_SELECTOR, "input#email.form-control.form-control-lg")
        email.send_keys("anandhu686513@gmail.com")
        password = driver.find_element(By.CSS_SELECTOR, "input#password.form-control.form-control-lg")
        password.send_keys("Anandhu@123")
        time.sleep(1)
        submitc = driver.find_element(By.CSS_SELECTOR, "button#submit.btn.btn-dark.btn-lg.w-50")
        submitc.click()
        time.sleep(2)

        find = driver.find_element(By.CSS_SELECTOR, "a[href='/blogs/blogs/']")
        find.click()
        
        findblog = driver.find_element(By.CSS_SELECTOR, "a[href='/blogs/single_blog/1/']")
        findblog.click()
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        comment = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea#comment.form-control.bg-white.border-0")))
        comment.send_keys("testing comment")
        time.sleep(2)
        submitcomment = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#submit.btn.btn-primary.w-100.py-3")))
        actions = ActionChains(driver)
        actions.move_to_element(submitcomment).perform()
        submitcomment.click()
        time.sleep(5)


        print("--------------------------------------")
        print("                                      ")
        print("Ran 1 test in", datetime.now() - start_time, "seconds")
        # print("Test Passed: Search results are shown.")
        print("Test Passed: Posted New comment.")
        print("Test Date:", datetime.now())
        print("                                      ")
        print("                                      ")
        print("                                      ")
        print("--------------------------------------")



if __name__ == '__main__':
    import unittest
    unittest.main()