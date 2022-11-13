from PIL import Image
from selenium import webdriver
import warnings
import random
import string
import csv
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# proxy_ip_port = "134.122.58.174:80"
# proxy_ip_port = "117.251.103.186:8080"
# proxy_ip_port = "157.100.12.138:999"
# proxy_ip_port = "31.129.163.70:78"
# proxy_ip_port = "94.45.137.34:8080"
# proxy_ip_port = "195.138.90.226:3128"
# proxy_ip_port = "94.45.137.34:8080"
# proxy_ip_port = "14.140.131.82:3128"
proxy_ip_port = ""


class RegistrationLinkedIn:
    """Class for registration LinkedIn account."""

    def __init__(self, path, data_file):
        self._path = path
        self._data_file = data_file
        self._driver = None
        self._wait = None

    def set_driver(self, proxy=None):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        if proxy:
            chrome_options.add_argument(f"--proxy-server={proxy}")
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        self._driver = webdriver.Chrome(executable_path='driver/chromedriver', chrome_options=chrome_options)

    def set_wait_time(self, wait_seconds=10):
        self._wait = WebDriverWait(self._driver, wait_seconds)

    def get_method_from_url(self):
        self._driver.get(self._path)

    @staticmethod
    def random_string(string_length=13):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(string_length)).title()

    def get_username_password(self):
        try:
            with open(self._data_file) as data:
                return next(csv.reader(data), None)
        except FileNotFoundError as ex:
            print(ex)

    def close_driver(self):
        print("Goodbye!!!")
        self._driver.close()
        return False

    def fill_main_form(self, email, password):
        # self._wait.until(EC.presence_of_element_located((By.ID, "email-or-phone"))).send_keys(email)
        self._wait.until(EC.presence_of_element_located((By.ID, "email-address"))).send_keys(email)
        self._wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
        self._wait.until(EC.element_to_be_clickable((By.ID, "join-form-submit"))).click()

    def fill_first_fast_names(self, first_name, last_name):
        self._wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys(first_name)
        self._wait.until(EC.presence_of_element_located((By.ID, "last-name"))).send_keys(last_name)
        self._wait.until(EC.element_to_be_clickable((By.ID, "join-form-submit"))).click()

    def get_capture(self):
        self._wait.until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "challenge-dialog__iframe")))
        self._wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "captcha-internal")))
        self._wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "arkoseframe")))
        self._wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "fc-iframe-wrap")))
        self._wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "CaptchaFrame")))
        self._wait.until(EC.element_to_be_clickable((By.ID, "home_children_button"))).click()
        self._wait.until(EC.visibility_of_element_located((By.ID, "game")))
        self._wait.until(lambda d: d.save_screenshot("./static/puzzle.png"))
        screenshot = Image.open("./static/puzzle.png")
        screenshot.show()
        print(
            """Input the image number‚ which is correctly positioned using schema!
               _______________________
              |       |       |       |
              |   1   |   2   |   3   |
              |_______|_______|_______|
              |       |       |       |
              |   4   |   5   |   6   |
              |_______|_______|_______|
            """
        )
        image_number = input("Input the image number: ")

    def create(self):
        data = self.get_username_password()
        if data:
            first_name = self.random_string()
            last_name = self.random_string()
            self.set_driver(proxy_ip_port)
            self.set_wait_time(20)
            self.get_method_from_url()
            self.fill_main_form(*data)
            self.fill_first_fast_names(first_name, last_name)
            self.get_capture()
        else:
            print("Problem with the data file or it is without email and password!")


if __name__ == "__main__":
    url = "https://www.linkedin.com/signup/cold-join?trk=guest_homepage-basic_nav-header-join"
    new_account = RegistrationLinkedIn(url, "list.csv")
    new_account.create()
