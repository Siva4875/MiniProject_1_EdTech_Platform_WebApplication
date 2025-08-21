import pytest
from utilities.config import Config
from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("driver_init")
class TestGUVI:
    """
    Test suite for GUVI website functionality
    Contains end-to-end tests for:
    - Page loading and navigation
    - User authentication flows
    - UI element validation
    - Session management
    """
    
    # Test Case 1: Verify whether the URL https://www.guvi.in is valid or not
    def test_url_loading(self):
        """Verify the base URL loads correctly"""
        self.logger.info("Executing Test Case 1: Verify URL loading")
        home_page = HomePage(self.driver)
        assert home_page.get_current_url() == Config.BASE_URL + "/", "URL mismatch"
        self.logger.info("Test Case 1 passed: URL loaded successfully")
    
    # Test Case 2: Verify whether the title of the webpage is correct
    def test_page_title(self):
        """Validate the page title matches expected value"""
        self.logger.info("Executing Test Case 2: Verify page title")
        home_page = HomePage(self.driver)
        assert home_page.get_page_title() == Config.EXPECTED_TITLE, "Title mismatch"
        self.logger.info("Test Case 2 passed: Page title matches expected value")
    
    # Test Case 3: Verify visibility and clickability of the Login button
    def test_login_button(self):
        """
        Test login button functionality:
        1. Verify button visibility
        2. Test click navigation
        """
        self.logger.info("Executing Test Case 3: Verify Login button")
        home_page = HomePage(self.driver)
        
        # Check visibility
        assert home_page.is_login_visible(), "Login button not visible"
        
        # Check clickability and navigation
        home_page.click_login()
        assert self.driver.current_url == Config.LOGIN_URL, "Did not navigate to login page"
        self.logger.info("Test Case 3 passed: Login button is visible and clickable")
    
    # Test Case 4: Verify visibility and clickability of the Sign-Up button
    def test_signup_button(self):
        """
        Test sign-up button functionality:
        1. Verify button visibility
        2. Test basic click action
        """
        self.logger.info("Executing Test Case 4: Verify Sign-Up button")
        home_page = HomePage(self.driver)
        
        assert home_page.is_signup_visible(), "Sign-Up button not visible"
        home_page.click_signup()
        self.logger.info("Test Case 4 passed: Sign-Up button is visible and clickable")
    
    # Test Case 5: Verify navigation to the Sign-In page via the Sign-Up button
    def test_signup_navigation(self):
        """Validate proper navigation to registration page"""
        self.logger.info("Executing Test Case 5: Verify Sign-Up navigation")
        home_page = HomePage(self.driver)
        home_page.click_signup()
        
        register_page = RegisterPage(self.driver)
        assert self.driver.current_url == Config.REGISTER_URL, "Wrong registration URL"
        assert register_page.is_register_page_loaded(), "Registration page not loaded"
        self.logger.info("Test Case 5 passed: Navigation to Sign-Up page successful")
    
    # Test Case 6: Verify login with invalid credentials
    def test_invalid_login(self):
        """
        Test authentication system:
        1. Attempt login with bad credentials
        2. Verify proper error handling
        """
        self.logger.info("Executing Test Case 6: Verify invalid login")
        home_page = HomePage(self.driver)
        home_page.click_login()
        
        login_page = LoginPage(self.driver)
        login_page.login(Config.INVALID_EMAIL, Config.INVALID_PASSWORD)
        
        assert login_page.is_error_message_displayed(), "No error shown for invalid login"
        error_message = login_page.get_error_message()
        assert "invalid" in error_message.lower() or "incorrect" in error_message.lower()
        self.logger.info("Test Case 6 passed: Invalid login handled correctly")

    
    # # Test Case 7: Verify login functionality with valid credentials
    def test_valid_login(self):
        """
        Test end-to-end session management:
        1. Login with valid credentials
        2. Verify successful logout
        3. Confirm post-logout state
        """
        self.logger.info("Executing Test Case 7: Verify login functionality with valid credentials")

        # Login sequence
        home_page = HomePage(self.driver)
        home_page.click_login()
        login_page = LoginPage(self.driver)
        login_page.login(Config.VALID_EMAIL, Config.VALID_PASSWORD)

        # Logout sequence with enhanced verification
        login_page.click_profile_icon()
        
        # Wait for dropdown to fully expand
        wait = WebDriverWait(self.driver, 20)
        
        try:
            # More robust logout button identification
            logout_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//li[@id='dropdown_contents']//div[contains(text(),'Sign Out')]"))
            )
            logout_button.click()
            
            # Wait for logout to complete - verify URL change or login button appearance
            wait.until(
                lambda driver: Config.BASE_URL in driver.current_url or 
                home_page.is_login_visible()
            )
            
            # Verify logout state
            assert home_page.is_login_visible(), "Login button should be visible after logout"
            assert Config.BASE_URL in self.driver.current_url, "Should be on homepage after logout"
            
            self.logger.info("Test Case 7 passed: Valid login successful")
            
        except Exception as e:
            self.logger.error(f"Logout failed: {str(e)}")
            self.driver.save_screenshot("logout_failure.png")
            raise

    # Test Case 8: Verify that menu items are displayed
    def test_menu_items_visibility(self):
        """Validate visibility of all main navigation menu items"""
        self.logger.info("Executing Test Case 8: Verify menu items visibility")
        home_page = HomePage(self.driver)
        
        assert home_page.is_courses_visible(), "Courses menu not visible"
        assert home_page.is_live_classes_visible(), "LIVE Classes menu not visible"
        assert home_page.is_practice_visible(), "Practice menu not visible"
        self.logger.info("Test Case 8 passed: All menu items are visible")
    
    # Test Case 9: Validate that the Dobby Guvi Assistant is present on the page
    def test_dobby_assistant(self):
        """Verify the Dobby assistant chatbot is available"""
        self.logger.info("Executing Test Case 9: Verify Dobby Assistant")
        dobbie_locator = (By.XPATH, "//img[@id='chateleon-container-gif-0']")
        
        # Added delay to account for potential lazy loading
        is_visible = BasePage.is_element_visible(
            self, 
            dobbie_locator, 
            delay_before=2,  # Wait 2 seconds before checking
            timeout=15       # Max 15 second wait
        )
        assert is_visible, "Dobby Assistant icon not visible"
        self.logger.info("Test Case 9 passed: Dobby Assistant is visible")

    # # Test Case 10: Validate logout functionality
    def test_logout_functionality(self):
        """
        Test end-to-end session management:
        1. Login with valid credentials
        2. Verify successful logout
        3. Confirm post-logout state
        """
        self.logger.info("Executing Test Case 10: Verify logout functionality")

        # Login sequence
        home_page = HomePage(self.driver)
        home_page.click_login()
        login_page = LoginPage(self.driver)
        login_page.login(Config.VALID_EMAIL, Config.VALID_PASSWORD)

        # Logout sequence with enhanced verification
        login_page.click_profile_icon()
        
        # Wait for dropdown to fully expand
        wait = WebDriverWait(self.driver, 20)
        
        try:
            # More robust logout button identification
            logout_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//li[@id='dropdown_contents']//div[contains(text(),'Sign Out')]"))
            )
            logout_button.click()
            
            # Wait for logout to complete - verify URL change or login button appearance
            wait.until(
                lambda driver: Config.BASE_URL in driver.current_url or 
                home_page.is_login_visible()
            )
            
            # Verify logout state
            assert home_page.is_login_visible(), "Login button should be visible after logout"
            assert Config.BASE_URL in self.driver.current_url, "Should be on homepage after logout"
            
            self.logger.info("Test Case 10 passed: Logout functionality works correctly")
            
        except Exception as e:
            self.logger.error(f"Logout failed: {str(e)}")
            self.driver.save_screenshot("logout_failure.png")
            raise