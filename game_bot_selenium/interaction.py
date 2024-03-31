from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("http://secure-retreat-92358.herokuapp.com")

f_Name = driver.find_element(By.NAME, "fName")
f_Name.send_keys("Feniz")

l_Name = driver.find_element(By.NAME, "lName")
l_Name.send_keys("Nova")

email = driver.find_element(By.NAME, "email")
email.send_keys("email@email.com")

submit = driver.find_element(By.CLASS_NAME, "btn")
submit.click()

time.sleep(5)