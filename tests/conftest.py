import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utilities.config import Config
from utilities.logger import setup_logger
import logging

@pytest.fixture(scope="class")
def driver_init(request):
    """
    Pytest fixture to initialize and manage WebDriver instance for test classes.
    Provides:
    - Configured Chrome browser instance
    - Class-level logger
    - Automatic cleanup
    
    Args:
        request: Pytest request object providing test context
    
    Features:
    - Runs once per test class
    - Incognito mode browsing
    - Automatic window maximization
    - Comprehensive logging
    - Graceful error handling
    - Proper resource cleanup
    """
    
    # Get the test class name dynamically (handles cases where request.cls might not exist)
    test_class_name = request.cls.__name__ if hasattr(request, 'cls') else "TestClass"
    
    # Initialize class-specific logger
    logger = setup_logger(test_class_name)
    logger.info(f"Initializing WebDriver for {test_class_name}")
    
    try:
        # Configure Chrome browser options
        chrome_options = Options()
        chrome_options.add_argument("--incognito")  # Private browsing mode
        chrome_options.add_argument("--disable-infobars")  # Hide info bars
        chrome_options.add_argument("--disable-extensions")  # Disable extensions
        
        logger.info("Launching Chrome browser with configured options")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to base URL and maximize window
        logger.info(f"Navigating to application URL: {Config.BASE_URL}")
        driver.get(Config.BASE_URL)
        driver.maximize_window()  # Ensure consistent viewport size
        
        # Make driver and logger available to test class
        request.cls.driver = driver
        request.cls.logger = logger
        
        # Fixture pause point - execution returns here after test class completes
        yield driver
        
    except Exception as e:
        logger.error(f"WebDriver initialization failed: {str(e)}")
        pytest.fail(f"Browser setup failed: {str(e)}")
        raise
        
    finally:
        # Teardown block - runs regardless of test success/failure
        logger.info("Initiating WebDriver cleanup")
        if 'driver' in locals():  # Safely check if driver exists
            driver.quit()  # Properly close browser session
        
        # Clean up logger handlers to prevent memory leaks
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

@pytest.fixture(scope="function")
def test_logger(request):
    """
    Pytest fixture to provide test-specific logging.
    Provides:
    - Individual test case logging
    - Test start/end markers
    - Automatic handler cleanup
    
    Args:
        request: Pytest request object with test context
    
    Features:
    - Runs for each test function
    - Isolated logging per test
    - Clean handler management
    """
    
    # Get current test name
    test_name = request.node.name
    logger = setup_logger(test_name)
    
    # Attach logger to test instance if available
    if hasattr(request, 'instance'):
        request.instance.logger = logger
    
    # Log test start
    logger.info(f"===== Starting test: {test_name} =====")
    
    # Fixture pause point - execution returns here after test completes
    yield logger
    
    # Log test completion
    logger.info(f"===== Completed test: {test_name} =====")
    
    # Clean up handlers to prevent log duplication
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)