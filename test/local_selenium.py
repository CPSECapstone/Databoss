from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

class TestLocal(object):

    seleniumFile = open("selenium.json", "r")
    credentials = json.load(seleniumFile)
    dbUser = credentials['dbUser']
    dbPass = credentials['dbPass']
    captureBucket = credentials['captureBucket']
    metricBucket = credentials['metricBucket']
    captureName = credentials['captureName']
    dbName = credentials['dbName']
    rdsInstance = credentials['rdsInstance']

    def setup(self):
        chromeOptions = Options()
        #chromeOptions.add_argument("--headless")
        #chromeOptions.add_argument("--disable-gpu")

        desiredCapabilities = DesiredCapabilities.CHROME
        desiredCapabilities.update(javascriptEnabled=True)

        self.driver = webdriver.Chrome(chrome_options=chromeOptions,
                                       desired_capabilities=desiredCapabilities)


    def testHomePage(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")

        try:
            assert "MyCRT" in driver.title

            #actions = ActionChains(driver)

            #actions.click(driver.find_element_by_name('capture-name'))
            #assert "PROGRESS FOR" in driver.find_element_by_tag_name("h1")

        finally:
            driver.quit()

    def testIndex(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")

        try:
            assert driver.current_url == "http://127.0.0.1:5000/#!/"

            actions = ActionChains(driver)

            actions.click(driver.find_element_by_link_text('CAPTURE'))
            actions.pause(2)
            actions.perform()
            assert driver.find_element_by_tag_name("h1").text == "CAPTURE"
            actions.reset_actions()

            actions.click(driver.find_element_by_link_text('REPLAY'))
            actions.pause(2)
            actions.perform()
            assert driver.find_element_by_tag_name("h1").text == "REPLAY"
            actions.reset_actions()

            actions.click(driver.find_element_by_link_text('METRICS'))
            actions.pause(2)
            actions.perform()
            assert driver.find_element_by_tag_name("h1").text == "METRICS"
            actions.reset_actions()

            actions.click(driver.find_element_by_link_text('CONTACT'))
            actions.pause(2)
            actions.perform()
            assert driver.find_element_by_tag_name("h1") == "CONTACT US"
            actions.reset_actions()

            actions.click(driver.find_element_by_link_text('HOME'))
            actions.pause(2)
            actions.perform()
            assert driver.find_element_by_tag_name("h3").text == "SCHEDULED"
            actions.reset_actions()

        finally:
            driver.quit()

    def testInteractiveCapture(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/#!/capture")

        try:
            element = driver.find_element_by_xpath("//input[@id='captureName']")
            element.send_keys(self.captureName)

            try:
                wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "option[value=self.captureBucket]")))
            except TimeoutException:
                print("Too much time passed for select field")

            select = Select(driver.find_element_by_xpath("//select[@id='crBucket']"))
            select.select_by_value(self.captureBucket)

            select = Select(driver.find_element_by_xpath("//select[@id='metricsBucket']"))
            select.select_by_value(self.metricBucket)

            select = Select(driver.find_element_by_xpath("//select[@id='rdsInstance']"))
            select.select_by_visible_text(self.rdsInstance)

            try:
                wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "id[value=self.dbUser]")))
            except TimeoutException:
                print("Too much time passed for username")

            element = driver.find_element_by_xpath("//input[@id='username']")
            element.send_keys(self.dbUser)
            element = driver.find_element_by_xpath("//input[@id='password']")
            element.send_keys(self.dbPass)
            element.find_element_by_xpath("//button[@id='authenticate']").click()

            try:
                wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "id[value=self.dbName]")))
            except TimeoutException:
                print("Too much time passed for databases")

            select = Select(driver.find_element_by_xpath("//select[@id='dbName']"))
            select.select_by_value(self.dbName)

            try:
                wait = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[@ng-model='button']")))
            except TimeoutException:
                print("Too much time passed for start capture button")

            element.find_element_by_xpath("//button[@ng-model='button']").click()

            try:
                wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, "//button[@id='fake']")))
            except TimeoutException:
                print("Too much time passed for change to page progress")

            assert self.captureName.upper() in driver.find_element_by_tag_name("h1").text

            element = driver.find_element_by_xpath("//button[@id='endCaptureButton']")
            element.click()

            try:
                wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, "//canvas[@id='cpuChart']")))
            except TimeoutException:
                print("Too much time passed for change to page progress")

            assert "METRICS" in driver.find_element_by_tag_name("h1").text

        finally:
            driver.quit()


    def cleanup(self):
        self.driver.close()
