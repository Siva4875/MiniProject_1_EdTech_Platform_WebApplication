GUVI Web Application Automated Testing

Title: Automated Testing of the Web Application https://www.guvi.in

Project Overview: The overview of this project is to automate the testing of the web application https://www.guvi.in by simulating user actions and validating key UI functionalities. This includes verifying page behavior, accessibility of critical elements, navigation flows, and login functionalities.

The automation framework follows Page Object Model (POM) and integrates with pytest and Selenium for execution and HTML Report generation for result visualization.

Scope: The automation will be designed to perform cross-browser validation across commonly used web browsers (e.g., Chrome). The system will interact with the web elements and execute test cases covering both positive and negative scenarios.

Objectives
- Validate the stability of GUVI’s web application.
- Ensure critical UI flows Login, Sign-Up, Logout work correctly.
- Support positive and negative test scenarios.
- Provided detailed reports for every test execution.


Features

- Cross-browser testing (Chrome, Firefox)
- Page Object Model design pattern
- Comprehensive test suite covering:
  - URL validation
  - Page title verification
  - Button visibility and clickability
  - Navigation flows
  - Login functionality (valid and invalid credentials)
  - Menu items verification
  - Dobby Assistant presence check
  - Logout functionality
- Detailed logging
- Proper exception handling

Prerequisites

- Python 3.8+
- Chrome and/or Firefox browsers
- Internet connection

This Project is:

Page Object Model, Data Driven Framework, Selenium, Pytest, OOPS concepts, Explicit and Fluent waits, try-except-finally blocks, Exception handling, configuration and utility files are deployed.

Conftest file using pytest fixtures for setup and teardown are used at Scope - Function - To open and close the browser after each test case

Test cases are created as functions and are grouped according to their functionality

HTML report generation, log file generation, capturing screenshots upon failure, use of conditional statements, assertion statements etc are deployed in this project.