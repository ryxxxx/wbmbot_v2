from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import stat
import glob


class ChromeDriverConfigurator:
    """
    Class to create the WebDriver with ChromeOptions
    """

    def __init__(self, headless: bool, test: bool):
        """
        Create a ChromeDriver with default options
        """
        self.headless = headless
        self.test = test
        self.chrome_options = Options()
        self.configure_options()
        self.driver = self.create_driver()

    def configure_options(self):
        """
        Add ChromeOption defaults
        """
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-logging")
        self.chrome_options.add_argument("--log-level=3")
        if self.headless:
            self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument("--no-sandbox")
        if self.test:
            self.chrome_options.add_argument("--log-level=0")

    def create_driver(self):
        """
        Creates the driver with the specified ChromeOptions
        """

        self.fix_chromedriver_permissions()
                # Get the ChromeDriver path
        driver_path = ChromeDriverManager().install()
        
        # Fix the path if it points to wrong file
        if driver_path.endswith('THIRD_PARTY_NOTICES.chromedriver'):
            driver_path = driver_path.replace('THIRD_PARTY_NOTICES.chromedriver', 'chromedriver')
        
        if os.path.exists(driver_path):
            current_perms = os.stat(driver_path).st_mode
            os.chmod(driver_path, current_perms | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        self.driver = webdriver.Chrome(
            service=Service(driver_path),
            options=self.chrome_options,
        )
        # Wait 5 seconds before doing stuff
        self.driver.implicitly_wait(5)
        return self.driver

    def get_driver(self):
        return self.driver
    
    def fix_chromedriver_permissions(self):
        """Fix permissions for all chromedriver files in .wdm cache"""
        try:
            # Find all chromedriver files
            pattern = "/root/.wdm/**/chromedriver"
            chromedriver_files = glob.glob(pattern, recursive=True)
            
            for file_path in chromedriver_files:
                if os.path.isfile(file_path):
                    # Make executable
                    current_perms = os.stat(file_path).st_mode
                    os.chmod(file_path, current_perms | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                    print(f"Fixed permissions for: {file_path}")
        except Exception as e:
            print(f"Error fixing permissions: {e}")
