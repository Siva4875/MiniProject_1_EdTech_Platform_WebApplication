from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """
    Page Object Model for the Login Page.
    Handles authentication workflows and error message validation.
    """
    
    # Locators
    EMAIL_INPUT = (By.ID, "email")  # Email input field
    PASSWORD_INPUT = (By.ID, "password")  # Password input field
    LOGIN_BUTTON = (By.XPATH, "//a[@id='login-btn']")  # Main login button
    ERROR_MESSAGE = (By.XPATH, "(//div[contains(@class,'invalid-feedback')])[2]")  # Auth error message
    LOGOUT_BUTTON = (By.XPATH, "//li[@id='dropdown_contents']//div[contains(text(),'Sign Out')]")  # Logout option
    PROFILE_ICON = (By.XPATH, "//div[@id='dropdown_title']//img[@id='dropdown_contents']")  # Profile dropdown
    
    def __init__(self, driver):
        """
        Initialize LoginPage.
        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.logger.info("LoginPage initialized")

    def enter_email(self, email):
        """
        Enter email into the email field.
        Args:
            email: String to input
        """
        self.logger.info(f"Entering email: {email}")
        self.find_element(self.EMAIL_INPUT).send_keys(email)
        self.logger.debug("Email entered successfully")

    def enter_password(self, password):
        """
        Enter password into the password field.
        Args:
            password: String to input
        """
        self.logger.info("Entering password (masked for security)")
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
        self.logger.debug("Password entered successfully")

    def click_login_button(self):
        """Click the login button to submit credentials."""
        self.logger.info("Attempting to click login button")
        self.click_element(self.LOGIN_BUTTON)
        self.logger.info("Login button clicked")

    def login(self, email, password):
        """
        Complete login workflow.
        Args:
            email: User email
            password: User password
        """
        self.logger.info(f"Attempting login for user: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        self.logger.info("Login sequence completed")

    def is_error_message_displayed(self):
        """Check if authentication error message is visible."""
        is_visible = self.is_element_visible(self.ERROR_MESSAGE)
        self.logger.debug(f"Error message visibility: {is_visible}")
        return is_visible

    def get_error_message(self):
        """
        Retrieve authentication error message text.
        Returns:
            str: Error message content
        """
        try:
            message = self.get_element_text(self.ERROR_MESSAGE)
            self.logger.info(f"Retrieved error message: '{message}'")
            return message
        except Exception as e:
            self.logger.error(f"Failed to get error message: {str(e)}")
            raise

    def click_profile_icon(self):
        """Click the profile dropdown icon."""
        self.logger.info("Clicking profile icon")
        self.click_element(self.PROFILE_ICON)
        self.logger.debug("Profile icon clicked")

    def click_logout(self):
        """Click logout option in profile dropdown."""
        self.logger.info("Attempting logout")
        self.click_element(self.LOGOUT_BUTTON)
        self.logger.info("Logout successful")