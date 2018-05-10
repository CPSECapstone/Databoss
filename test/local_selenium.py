from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class TestHome(object):

    def setup(self):
        chromeOptions = Options()
        chromeOptions.binary_location = "/usr/local/bin/chromedriver"
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--disable-gpu")

        desiredCapabilities = DesiredCapabilities.CHROME
        desiredCapabilities.update(javascriptEnabled=True)

        self.driver = webdriver.Chrome(chrome_options=chromeOptions,
                                       desired_capabilities=desiredCapabilities)


    def testHomePage(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        #driver.get("http://ec2-54-183-41-251.us-west-1.compute.amazonaws.com:5000")
        assert "MyCRT" in driver.title
        homeLink = driver.find_element_by_link_text('HOME')
        captureLink = driver.find_element_by_link_text('CAPTURE')
        replayLink = driver.find_element_by_link_text('REPLAY')
        infoLink = driver.find_element_by_link_text('INFO')
        metricLink = driver.find_element_by_link_text('METRICS')
        contactLink = driver.find_element_by_link_text('CONTACT')

        driver.quit()

    def testIndex(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert driver.current_url == "http://127.0.0.1:5000/#!/"

        driver.execute_script("document.body.style.zoom='90%'")

        actions = ActionChains(driver)


        actions.click(driver.find_element_by_link_text('CAPTURE'))
        actions.pause(2)
        actions.perform()
        assert driver.current_url == "http://127.0.0.1:5000/#!/capture"
        actions.reset_actions()

        actions.click(driver.find_element_by_link_text('REPLAY'))
        actions.pause(2)
        actions.perform()
        assert driver.current_url == "http://127.0.0.1:5000/#!/replay"
        actions.reset_actions()

        actions.click(driver.find_element_by_link_text('INFO'))
        actions.pause(2)
        actions.perform()
        assert driver.current_url == "http://127.0.0.1:5000/#!/information"
        actions.reset_actions()

        actions.click(driver.find_element_by_link_text('METRICS'))
        actions.pause(2)
        actions.perform()
        assert driver.current_url == "http://127.0.0.1:5000/#!/metrics"
        actions.reset_actions()

        actions.click(driver.find_element_by_link_text('CONTACT'))
        actions.pause(2)
        actions.perform()
        assert driver.current_url == "http://127.0.0.1:5000/#!/help"
        actions.reset_actions()

        actions.click(driver.find_element_by_link_text('HOME'))
        actions.pause(2)
        actions.perform()
        assert driver.current_url == "http://127.0.0.1:5000/#!/"
        actions.reset_actions()

        driver.quit()


    def cleanup(self):
        self.driver.close()
