from selenium import webdriver


class TestHome(object):

    def setup(self):
        self.driver = webdriver.Safari()

    def testHomePage(self):
        driver = self.driver
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
