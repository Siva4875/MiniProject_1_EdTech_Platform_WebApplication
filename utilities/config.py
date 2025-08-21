class Config:
    """
    Central configuration class for test automation framework.
    Stores all environment-specific settings, URLs, and test data.
    
    Security Warning:
    - Never commit real credentials to version control
    - For production use, replace hardcoded credentials with environment variables
    - Consider using a secrets management service for enterprise environments
    """

    # Application Base URLs
    BASE_URL = "https://www.guvi.in"  # Root URL of the application under test
    LOGIN_URL = "https://www.guvi.in/sign-in/"  # Login page endpoint
    REGISTER_URL = "https://www.guvi.in/register/"  # Registration page endpoint

    # Expected Page Titles
    EXPECTED_TITLE = "GUVI | Learn to code in your native language"  # Expected homepage title

    # Test Credentials
    # TODO: Replace with environment variables in CI/CD pipeline
    VALID_EMAIL = "Sivadsk14@gmail.com"  # Valid test account username/email
    VALID_PASSWORD = "SivaHari@48"  # Valid test account password
    INVALID_EMAIL = "invalid@example.com"  # Generic invalid email format
    INVALID_PASSWORD = "wrongpassword"  # Generic invalid password

    # Wait Time Configurations (in seconds)
    IMPLICIT_WAIT = 10  # Global implicit wait time for element presence
    EXPLICIT_WAIT = 20  # Maximum explicit wait time for element interactions

    # Security Configuration
    CREDENTIAL_MASKING = True  # When True, prevents logging of sensitive credentials

    @classmethod
    def get_sensitive_data(cls, data_type):
        """
        Safely retrieves sensitive configuration data with optional masking.
        
        Args:
            data_type (str): Type of data to retrieve ('email' or 'password')
            
        Returns:
            str: Masked or actual value based on security settings
            
        Raises:
            ValueError: If invalid data_type is requested
        """
        if data_type not in ['email', 'password']:
            raise ValueError("Invalid data type requested")

        value = getattr(cls, f"VALID_{data_type.upper()}")
        
        if cls.CREDENTIAL_MASKING:
            if data_type == 'email':
                return '***@***.***'
            return '********'
        return value