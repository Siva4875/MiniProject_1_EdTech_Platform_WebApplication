# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utilities.logger import logger
from utilities.logger import setup_logger

class BasePage:
    def __init__(self, driver):
        """
        Initialize BasePage with WebDriver instance.
        Args:
            driver: Selenium WebDriver instance.
        """
        self.driver = driver
        self.logger = setup_logger(self.__class__.__name__)  # Logger specific to the child class
        self.wait = WebDriverWait(driver, 10)  # Default explicit wait of 10 seconds

    def find_element(self, locator):
        """
        Find and return a single web element after waiting for its presence.
        Args:
            locator: Tuple (By, selector) e.g., (By.XPATH, "//button").
        Raises:
            TimeoutException: If element is not found.
        """
        try:
            self.logger.info(f"Attempting to find element: {locator}")
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f"Element not found within timeout: {locator}")
            raise

    def click_element(self, locator):
        """
        Click an element after ensuring it's clickable.
        Args:
            locator: Tuple (By, selector).
        Raises:
            TimeoutException: If element is not clickable.
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Successfully clicked element: {locator}")
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            raise

    def get_element_text(self, locator):
        """
        Get text content of an element.
        Args:
            locator: Tuple (By, selector).
        Returns:
            str: Text of the element.
        Raises:
            TimeoutException: If element is not found.
        """
        try:
            element = self.find_element(locator)
            text = element.text
            self.logger.info(f"Retrieved text '{text}' from element: {locator}")
            return text
        except TimeoutException:
            self.logger.error(f"Failed to get text from element: {locator}")
            raise

    def is_element_visible(self, locator, delay_before=1, timeout=15):
        """
        Check if an element is visible after an optional delay.
        Args:
            locator: Tuple (By, selector).
            delay_before: Seconds to wait before checking (default: 1).
            timeout: Max wait time in seconds (default: 15).
        Returns:
            bool: True if visible, False otherwise.
        """
        try:
            time.sleep(delay_before)  # Optional delay for dynamic content
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f"Element is visible: {locator}")
            return element.is_displayed()
        except TimeoutException:
            self.logger.warning(f"Element not visible within {timeout}s: {locator}")
            return False

    def navigate_to(self, url):
        """
        Navigate to a URL.
        Args:
            url: Target URL.
        """
        self.driver.get(url)
        self.logger.info(f"Navigated to URL: {url}")

    def get_current_url(self):
        """Get the current page URL."""
        url = self.driver.current_url
        self.logger.info(f"Current URL: {url}")
        return url

    def get_page_title(self):
        """Get the current page title."""
        title = self.driver.title
        self.logger.info(f"Page title: {title}")
        return title

    def click_sign_out(self):
        """
        Click the sign-out button in a user dropdown.
        Handles edge cases with JavaScript fallback.
        Raises:
            Exception: If sign-out fails.
        """
        try:
            self.logger.info("Attempting sign-out...")
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".user-dropdown"))
            )
            dropdown.click()
            self.logger.debug("User dropdown clicked.")

            sign_out = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[text()='Sign Out']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", sign_out)

            try:
                sign_out.click()
            except Exception:
                self.logger.warning("Normal click failed. Using JS click fallback.")
                self.driver.execute_script("arguments[0].click();", sign_out)

            self.logger.info("Successfully signed out.")
        except Exception as e:
            self.logger.error(f"Sign-out failed: {str(e)}")
            raise

    def is_element_clickable(self, locator, timeout=20):
        """
        Check if an element is clickable.
        Args:
            locator: Tuple (By, selector).
            timeout: Max wait time (default: 20s).
        Returns:
            bool: True if clickable, False otherwise.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            self.logger.info(f"Element is clickable: {locator}")
            return True
        except NoSuchElementException:
            self.logger.warning(f"Element not present: {locator}")
            return False

    def wait_until_visible(self, by_locator, delay_before=1, timeout=15):
        """
        Wait for an element to become visible.
        Args:
            by_locator: Tuple (By, selector).
            timeout: Max wait time (default: 15s).
        Returns:
            WebElement: The visible element, or None if timeout.
        """
        try:
            time.sleep(delay_before)
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(by_locator)
            )
            self.logger.info(f"Element is now visible: {by_locator}")
            return element
        except TimeoutException:
            self.logger.warning(f"Element not visible within {timeout}s: {by_locator}")
            return None