from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.config import Config

class HomePage(BasePage):
    """Page Object Model for the Home Page of the application."""
    
    # Locators (Private constants for better maintainability)
    LOGIN_BUTTON = (By.XPATH, "(//a[contains(text(),'Login')])[2]")
    SIGNUP_BUTTON = (By.XPATH, "//a[contains(text(),'Sign up')]")
    COURSES_MENU = (By.XPATH, "(//a[contains(text(),'Courses')])[2]")
    LIVE_CLASSES_MENU = (By.XPATH, "//p[@id='liveclasseslink']")    
    PRACTICE_MENU = (By.XPATH, "//p[@id='practiceslink']")
    DOBBY_ASSISTANT = (By.XPATH, "(//img[@alt='Dobby bot icon'])[1]")
    LOGIN_BUTTON_ALT = (By.XPATH, "//a[@id='login-btn']")  # Renamed to avoid conflict
    
    def __init__(self, driver):
        """
        Initialize HomePage and navigate to BASE_URL.
        Args:
            driver: Selenium WebDriver instance.
        """
        super().__init__(driver)
        self.logger.info(f"Initializing HomePage and navigating to {Config.BASE_URL}")
        self.navigate_to(Config.BASE_URL)
        
    def click_login(self):
        """Click the Login button."""
        self.logger.info("Attempting to click Login button")
        self.click_element(self.LOGIN_BUTTON)
        self.logger.info("Login button clicked successfully")
        
    def click_signup(self):
        """Click the Sign Up button."""
        self.logger.info("Attempting to click Sign Up button")
        self.click_element(self.SIGNUP_BUTTON)
        self.logger.info("Sign Up button clicked successfully")
        
    def is_login_visible(self):
        """Check if Login button is visible."""
        visible = self.is_element_visible(self.LOGIN_BUTTON)
        self.logger.debug(f"Login button visibility: {visible}")
        return visible
        
    def is_signup_visible(self):
        """Check if Sign Up button is visible."""
        visible = self.is_element_visible(self.SIGNUP_BUTTON)
        self.logger.debug(f"Sign Up button visibility: {visible}")
        return visible
        
    def is_courses_visible(self):
        """Check if Courses menu is visible."""
        visible = self.is_element_visible(self.COURSES_MENU)
        self.logger.debug(f"Courses menu visibility: {visible}")
        return visible
        
    def is_live_classes_visible(self):
        """Check if Live Classes menu is visible."""
        visible = self.is_element_visible(self.LIVE_CLASSES_MENU)
        self.logger.debug(f"Live Classes menu visibility: {visible}")
        return visible
        
    def is_practice_visible(self):
        """Check if Practice menu is visible."""
        visible = self.is_element_visible(self.PRACTICE_MENU)
        self.logger.debug(f"Practice menu visibility: {visible}")
        return visible
        
    def is_dobby_assistant_visible(self):
        """Check if Dobby Assistant icon is visible."""
        visible = self.is_element_visible(self.DOBBY_ASSISTANT)
        self.logger.debug(f"Dobby Assistant visibility: {visible}")
        return visible
    
    def is_element_clickable(self, locator, timeout=20):
        """
        Check if an element is clickable (overrides parent method for HomePage-specific logging).
        Args:
            locator: Tuple (By, selector)
            timeout: Maximum wait time in seconds (default: 20)
        Returns:
            bool: True if clickable, False otherwise
        """
        self.logger.info(f"Checking clickability of element: {locator}")
        return super().is_element_clickable(locator, timeout)