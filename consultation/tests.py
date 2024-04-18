import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class LoginTest(unittest.TestCase):

    def setUp(self):
        # Get the current directory of the tests.py file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        chromedriver_path = os.path.join(current_directory, 'chromedriver.exe')

        # Initialize the Chrome WebDriver using the chromedriver path
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)

    def test_login(self):
        self.driver.get('http://127.0.0.1:8000/login_fun_page/')
        
        # Find the email, password input fields, and the login button by their IDs
        email_field = self.driver.find_element(By.ID, 'email')
        password_field = self.driver.find_element(By.ID, 'password')
        login_button = self.driver.find_element(By.ID, 'login-btn')

        # Input values for email and password fields
        email_field.send_keys('swathysaji793@gmail.com')
        password_field.send_keys('Swathy793!')

        # Perform a click on the login button
        login_button.click()

        # Optionally, add assertions to verify the login success or perform further actions after login

    def tearDown(self):
        # Close the browser window
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()




from selenium import webdriver

# Start a Chrome WebDriver session
driver = webdriver.Chrome()

# Load the page
driver.get("http://127.0.0.1:8000/view_slots/")  # Replace with the actual path to your HTML file

# Find all the appointment links and click one of them
appointment_links = driver.find_elements_by_xpath("//a[@class='btn btn-warning']")
if appointment_links:
    # Click the first appointment link (change index if you want to click a different link)
    appointment_links[0].click()
else:
    print("No appointment links found.")

# Assuming the link navigates to a new page for booking an appointment,
# you can continue interacting with the elements on the new page here.

# Example: Fill in a form for booking an appointment
# Find elements on the booking page and interact with them
# date_input = driver.find_element_by_name("date")
# time_from_input = driver.find_element_by_name("timefrom")
# time_to_input = driver.find_element_by_name("timeto")
# ... Fill in the form fields
# submit_button = driver.find_element_by_id("submit-button")
# submit_button.click()

# Close the browser session
driver.quit()
