from selenium import webdriver
import warnings
import random
import string
import csv

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


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

    def set_wait_time(self, wait_seconds=20):
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

    def fill_main_form(self, email, password):
        # self._wait.until(EC.presence_of_element_located((By.ID, "email-or-phone"))).send_keys(email)
        self._wait.until(EC.presence_of_element_located((By.ID, "email-address"))).send_keys(email)
        self._wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
        self._wait.until(EC.element_to_be_clickable((By.ID, "join-form-submit"))).click()

    def fill_first_fast_names(self, first_name, last_name):
        self._wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys(first_name)
        self._wait.until(EC.presence_of_element_located((By.ID, "last-name"))).send_keys(last_name)
        self._wait.until(EC.element_to_be_clickable((By.ID, "join-form-submit"))).click()

    def fill_phone_number_form(self):
        while True:
            self._wait.until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "challenge-dialog__iframe")))
            phone_number = input("Input phone number in such format '967478911': ")
            if (len(phone_number) != 9) or (not phone_number.isdigit()):
                print("Inputted invalid phone number. Try again.")
                continue
            self._wait.until(EC.visibility_of_element_located(
                (By.ID, "register-verification-phone-number"))).send_keys(phone_number)
            self._wait.until(EC.element_to_be_clickable((By.ID, "register-phone-submit-button"))).click()
            break

    def fill_verify_code_form(self):
        while True:
            verify_code = input("Input verification code from sms message: ")

            if len(verify_code) != 6:
                print("Verification code should be 6 characters!")
                complete_q = input("Do you want to try again? y/n: ")
                if complete_q == "n":
                    self._driver.close()
                    print("Goodbye!!!")
                    break
                continue

            self._wait.until(EC.visibility_of_element_located((By.ID, "verify_code"))).send_keys(verify_code)
            self._wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Verify']"))).click()
            break

    def create(self):
        self.set_driver()
        self.set_wait_time()
        data = self.get_username_password()
        if data:
            first_name = self.random_string()
            last_name = self.random_string()

            self.get_method_from_url()
            self.fill_main_form(*data)
            self.fill_first_fast_names(first_name, last_name)
            self.fill_phone_number_form()
            self.fill_verify_code_form()
            self._driver.close()
        else:
            print("Problem with the data file or it is without email and password!")


if __name__ == "__main__":
    url = "https://www.linkedin.com/signup/cold-join?trk=guest_homepage-basic_nav-header-join"
    new_account = RegistrationLinkedIn(url, "list.csv")
    new_account.create()

