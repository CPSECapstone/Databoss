from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

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
