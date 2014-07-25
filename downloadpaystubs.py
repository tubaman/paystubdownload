import netrc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Firefox()
driver.implicitly_wait(30)
base_url = "https://www.paycheckrecords.com/"

user, _ , password = netrc.netrc().authenticators("paycheckrecords.com")
driver.get(base_url + "/login.jsp")
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
