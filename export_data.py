import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def export_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    download_path = "/path/to/downloads"  # Adjust as needed

    try:
        logger.info("Opening the login page.")
        driver.get("https://identity.hcssapps.com/Account/Login")
        
        logger.info("Entering username.")
        driver.find_element(By.XPATH, '//*[@id="username-formgroup"]/input').send_keys(os.environ['HCSS_USERNAME'])
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div[3]/div[1]/div[2]/div[1]/form/button').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password-formgroup"]/input')))
        logger.info("Entering password.")
        driver.find_element(By.XPATH, '//*[@id="password-formgroup"]/input').send_keys(os.environ['HCSS_PASSWORD'])
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div[3]/div[1]/div[2]/div[1]/form/button').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Safety"]/div[1]/div[2]/div[3]/a/b')))
        logger.info("Navigating to Safety section.")
        driver.find_element(By.XPATH, '//*[@id="Safety"]/div[1]/div[2]/div[3]/a/b').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sidebar-container"]/div/nav/ul/li[4]/a/span')))
        logger.info("Navigating to Inspections.")
        driver.find_element(By.XPATH, '//*[@id="sidebar-container"]/div/nav/ul/li[4]/a/span').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dateRangeSelect"]')))
        logger.info("Setting date filter to ALL.")
        driver.find_element(By.XPATH, '//*[@id="dateRangeSelect"]').click()
        driver.find_element(By.XPATH, '//*[@id="dateRangeSelect"]/option[6]').click()
        driver.find_element(By.XPATH, '//*[@id="applyButton"]/i').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="InspectionHistoryResultsGrid"]/div[1]/span/button')))
        logger.info("Clicking export button.")
        driver.find_element(By.XPATH, '//*[@id="InspectionHistoryResultsGrid"]/div[1]/span/button').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="createDetailsExcel"]/a')))
        driver.find_element(By.XPATH, '//*[@id="createDetailsExcel"]/a').click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="divInspOnlySelectAll"]/label/span')))
        logger.info("Selecting all inspections.")
        driver.find_element(By.XPATH, '//*[@id="divInspOnlySelectAll"]/label/span').click()
        driver.find_element(By.XPATH, '//*[@id="btnDetailsExport"]').click()

        logger.info("Waiting for the download to complete.")
        time.sleep(20)

        files = [f for f in os.listdir(download_path) if f.endswith('.xlsx')]
        if not files:
            logger.error("No Excel file downloaded")
            raise FileNotFoundError("No Excel file downloaded")

        file_path = os.path.join(download_path, files[0])
        logger.info(f"Downloaded file: {file_path}")
        return file_path

    finally:
        driver.quit()
