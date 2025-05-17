import pytz
import time
import yaml
import requests
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parse import parse_announcements

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
tz = pytz.timezone(config["timezone"])
url = config["url"]


def get_announcements(cookie: str):
    url = "https://www.binance.com/en/support/announcement"

    headers = {
        "authority": "www.binance.com",
        "method": "GET",
        "path": "/en/support/announcement",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": cookie,
        "if-none-match": "6695cee054a1238e4d822b62afed51ba6faa8fafc3d88d459d1ef17f4afb6cb2",
        "priority": "u=0, i",
        "sec-ch-ua": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    return response

def get_and_save(cookie: str):
    output_dir = "output"
    start_time = time.time()
    response = get_announcements(cookie)
    elapsed = time.time() - start_time
    if response.status_code == 200:
        timestamp = datetime.now(tz).strftime('%Y%m%d_%H%M%S')
        # Save to html file
        print(f"Starting process at {timestamp}")
        output_file = f"{output_dir}/announcements.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        # Parse html to get announcements csv
        parsed_output_file = f"{output_dir}/{timestamp}_announcements.csv"
        parse_announcements(output_file, parsed_output_file)
        print(f"Parsed announcements to {parsed_output_file}")
        print(f"Elapsed time: {elapsed:.2f} seconds")
    else:
        print(f"Request failed with status code: {response.status_code}")

def main(refresh_rate: int):
    # Set up the Chrome driver (ensure chromedriver is in your PATH)
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        proceed_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "binance_hk_compliance_popup_proceed"))
        )
        proceed_button.click()
        time.sleep(2)
        selenium_cookies = driver.get_cookies()
        cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
        cookie_str = "; ".join([f"{name}={value}" for name, value in cookies.items()])

        # Checks for announcements periodically
        while True:
            get_and_save(cookie_str)
            time.sleep(refresh_rate)

    except Exception as e:
        print(f"Error clicking button: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh_rate", type=str, help="Refresh rate in seconds")
    args = parser.parse_args()

    refresh_rate = int(args.refresh_rate) if args.refresh_rate else 60
    print(f"Running with refresh rate: {refresh_rate} seconds")

    main(refresh_rate)