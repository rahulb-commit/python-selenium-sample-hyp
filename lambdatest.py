import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

class FirstSampleTest(unittest.TestCase):
    def setUp(self):
        # Using getenv to pull from PowerShell environment variables
        username = os.getenv("LT_USERNAME")
        access_key = os.getenv("LT_ACCESS_KEY")

        options = ChromeOptions()
        options.browser_version = "latest"
        options.platform_name = "Linux" # Must be Linux for the HyperExecute runner 
        
        lt_options = {
            "username": username,
            "accessKey": access_key,
            "video": True,
            "network": True,
            "build": "Local Test Build",
            "project": "TestMu Certification",
            "smartUI.project": "web-assignment-project-v1", # UNIQUE NAME
            "name": "Local Selenium Python Test",
            "w3c": True,
            "plugin": "python-python"
        }
        options.set_capability("LT:Options", lt_options)

        # Standard Hub URL for Web Automation
        self.driver = webdriver.Remote(
            command_executor="http://{}:{}@hub.lambdatest.com/wd/hub".format(
                username, access_key
            ),
            options=options,
        )

    def test_demo_site(self):
        driver = self.driver
        print("Loading URL")
        driver.get("https://lambdatest.github.io/sample-todo-app/")

        driver.find_element(By.NAME, "li1").click()
        driver.find_element(By.NAME, "li2").click()
        print("Clicked on checkboxes")

        # Add a new item
        driver.find_element(By.ID, "sampletodotext").send_keys("Local Test Working")
        driver.find_element(By.ID, "addbutton").click()
        
        # Verify
        heading = driver.find_element(By.XPATH, "//h1")
        if heading.is_displayed():
            print("Test passed: Heading is visible")
            driver.execute_script("lambda-status=passed")
        else:
            driver.execute_script("lambda-status=failed")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()