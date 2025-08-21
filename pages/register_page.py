from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegisterPage(BasePage):
    """
    Page Object Model for the User Registration Page.
    Handles user registration flow and page validation.
    """

    # Locators
    REGISTER_HEADER = (By.XPATH, "//h2[contains(text(),'Sign Up')]")  # Main header element indicating registration page
    
    def __init__(self, driver):
        """
        Initialize RegisterPage with WebDriver instance.
        
        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.logger.info("RegisterPage initialized - ready for user registration")

    def is_register_page_loaded(self):
        """
        Verify if the registration page is successfully loaded.
        
        Returns:
            bool: True if registration header is visible, False otherwise
            
        Example:
            >>> register_page = RegisterPage(driver)
            >>> register_page.is_register_page_loaded()
            True
        """
        try:
            is_loaded = self.is_element_visible(self.REGISTER_HEADER)
            if is_loaded:
                self.logger.info("Registration page loaded successfully")
            else:
                self.logger.warning("Registration page header not found")
            return is_loaded
        except Exception as e:
            self.logger.error(f"Error verifying page load: {str(e)}")
            raise