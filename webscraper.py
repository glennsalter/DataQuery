import csv
import pytz
import time
import yaml
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_time = time.time()
output_dir = "output"

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
tz = pytz.timezone(config["timezone"])
url = config["url"]

# Set up the Chrome driver (ensure chromedriver is in your PATH)
service = Service()
driver = webdriver.Chrome(service=service)

# Open a web page
driver.get("https://www.binance.com/en/support/announcement")

try:
    # Wait up to 10 seconds for the button to be clickable
    proceed_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "binance_hk_compliance_popup_proceed"))
    )
    proceed_button.click()
    time.sleep(2)  # Optional: wait to see the result

    # Wait for the announcements container to be present
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div/div/div[3]/div/div"))
    )

    # Find all announcement divs inside the container
    announcement_divs = container.find_elements(By.XPATH, ".//div[contains(@class, 'bn-flex')]")

    messages = []
    for div in announcement_divs:
        a_tag = div.find_element(By.TAG_NAME, "a")
        messages.append(a_tag.text)

    timestamp = datetime.now(tz).strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{timestamp}_announcements.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['title'])
        for message in messages:
            writer.writerow([message])

    elapsed = time.time() - start_time
    print(f"Number of titles: {len(messages)}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()