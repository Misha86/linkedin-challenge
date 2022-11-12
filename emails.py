from selenium import webdriver
import warnings
import random
import string
import csv

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class EmailAccount:
    """Class for create new email account."""

    def __init__(self, path):
        self._path = path
        self._username = self.random_string_digits()
        self._password = self.random_string_digits(string_length=15)
        self._driver = None
        self._wait = None
        self._verify_email = None

    def set_driver(self, proxy=None):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        if proxy:
            chrome_options.add_argument(f"--proxy-server={proxy}")
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        self._driver = webdriver.Chrome(executable_path='driver/chromedriver', chrome_options=chrome_options)

    def set_wait_time(self, wait_seconds=20):
        self._wait = WebDriverWait(self._driver, wait_seconds)

    def set_verify_email(self):
        self._verify_email = input("Enter Email Address for Verification: ")
        return self._verify_email

    def get_method_from_url(self):
        self._driver.get(self._path)

    @staticmethod
    def random_string_digits(string_length=13):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(string_length))

    def fill_main_form(self):
        self._wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[ @ title = 'Username']")))
        self._wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(self._username)
        self._driver.switch_to.default_content()
        self._wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(self._password)
        self._wait.until(EC.presence_of_element_located((By.ID, "repeat-password"))).send_keys(self._password)
        self._wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Create account']"))).click()

    def fill_verify_email_form(self):
        try:
            self._wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(self._verify_email)
        except TimeoutException:
            self._wait.until(EC.element_to_be_clickable((By.ID, "label_1"))).click()
            self._wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(self._verify_email)

        self._wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Get verification code']"))).click()

    def fill_verify_code_form(self):
        while True:
            verify_code = input("Input verification code from email message: ")

            if len(verify_code) != 6:
                print("Verification code should be 6 characters!")
                continue

            self._driver.find_element_by_xpath("// *[ @ id = 'verification']").send_keys(verify_code)

            self._wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Verify']"))).click()

            try:
                self._wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Request new code']"))).click()
                print("You inputted invalid verification code")
                complete_q = input("Do you want to try again? y/n: ")
                if complete_q == "n":
                    self._driver.close()
                    print("Goodbye!!!")
                    break
                else:
                    print('Please try again')
                    continue
            except TimeoutException:
                self._wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))).click()
                self._wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Save selected']"))).click()
                self._driver.close()
                self.save_data()
                break

    def save_data(self):
        print("Your New Email Address is: ", self._username, "@proton.me", sep='')
        print("Your New Email Password is: ", self._password)
        csv_data = [[self._username + '@proton.me', self._password]]
        with open('list.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_data)
        print('Great! We added you account details to the table.')

    def create(self):
        self.set_verify_email()
        self.set_driver()
        self.set_wait_time()
        self.get_method_from_url()
        self.fill_main_form()
        self.fill_verify_email_form()
        self.fill_verify_code_form()


if __name__ == "__main__":
    url = 'https://account.proton.me/signup?plan=free&billing=12&minimumCycle=12&currency=EUR&language=en'
    print("Auto Account Creator Script")
    new_account = EmailAccount(url)
    new_account.create()
