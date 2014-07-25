import unittest, time, re
import netrc


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

class Downloadpaystubs(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.paycheckrecords.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_downloadpaystubs(self):
        user, _ , password = netrc.netrc().authenticators("paycheckrecords.com")
        driver = self.driver
        driver.get(self.base_url + "/login.jsp")
        driver.find_element_by_id("userStrId").clear()
        driver.find_element_by_id("userStrId").send_keys(user)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("Login").click()
        Select(driver.find_element_by_name("shortCut")).select_by_visible_text("This Year")
        driver.find_element_by_id("updateReportSubmit").click()
        driver.find_element_by_link_text("01/15/2014").click()
        driver.find_element_by_link_text("Printer-Friendly Version").click()
        driver.find_element_by_link_text("Back to paystub list").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
