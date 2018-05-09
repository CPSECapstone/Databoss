from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

class TestHome(object):

    def setup(self):
        chromeOptions = Options()
        chromeOptions.binary_location = "/usr/bin/chromium-browser"
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--disable-gpu")
        chromeOptions.add_argument("--no-sandbox")  # This make Chromium reachable
        chromeOptions.add_argument("--no-default-browser-check")  # Overrides default choices
        chromeOptions.add_argument("--no-first-run")
        chromeOptions.add_argument("--disable-default-apps")

        self.driver = webdriver.Chrome('/home/travis/virtualenv/python2.7.9/chromedriver', chrome_options=chromeOptions)


    def testHomePage(self):
        driver = self.driver
        #driver.get("http://127.0.0.1:5000/")
        driver.get("http://ec2-54-183-41-251.us-west-1.compute.amazonaws.com:5000")
        assert "MyCRT" in driver.title
        homeLink = driver.find_element_by_link_text('HOME').value_of_css_property('HOME')
        captureLink = driver.find_element_by_link_text('CAPTURE')
        replayLink = driver.find_element_by_link_text('REPLAY')
        infoLink = driver.find_element_by_link_text('INFO')
        metricLink = driver.find_element_by_link_text('METRICS')
        contactLink = driver.find_element_by_link_text('CONTACT')

    def cleanup(self):
        self.driver.close()
