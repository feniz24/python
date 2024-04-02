from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

PROMISED_DOWN = 150
PROMISED_UP = 10

TWITTER_USERNAME = "feniz_24"
TWITTER_PASSWORD = "12345Tho"


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.down = PROMISED_DOWN
        self.up = PROMISED_UP

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net")
        time.sleep(40)
        go_button = self.driver.find_element(By.CLASS_NAME, "start-text")
        go_button.click()
        time.sleep(180)

        cross_icon = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/a/svg')
        cross_icon.click()

        down_speed = self.driver.find_element(By.CLASS_NAME, "download-speed").text
        up_speed = self.driver.find_element(By.CLASS_NAME, "upload-speed").text

        speed = {
            "down_speed": down_speed,
            "up_speed": up_speed
        }

        return speed

    def tweet_at_provider(self, speed):
        if speed["down_speed"] < self.down:
            self.driver.get("https://twitter.com")

            time.sleep(5)
            sign_in = self.driver.find_element(By.XPATH,
                                               '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div')
            sign_in.click()

            time.sleep(5)
            username = self.driver.find_element(By.NAME, "text")
            username.send_keys(TWITTER_USERNAME)
            username.send_keys(Keys.ENTER)

            time.sleep(2)
            password = self.driver.find_element(By.NAME, "password")
            password.send_keys(TWITTER_PASSWORD)
            password.send_keys(Keys.ENTER)

            time.sleep(5)

            text_box = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div')
            text_box.send_keys(f"Hello, ISP, Currently, I have only {speed['down_speed']}/{speed['up_speed']}")

            post_button = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/span/span')
            post_button.click()

            time.sleep(10)
