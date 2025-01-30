from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
from datetime import datetime

# Chrome options setup
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# WebDriver setup
webdriver_path = r"C:\\Users\\Hp\\Downloads\\chromedriver-win64 (2)\\chromedriver-win64\\chromedriver.exe"
service = Service(webdriver_path)

# Base URL for pagination
base_url = "https://www.propertyfinder.ae/en/commercial-rent/properties-for-rent.html?page={page}"

def start_driver():
    return webdriver.Chrome(service=service, options=chrome_options)

def extract_property_details(card):
    try:
        # Extract verification and agent details based on specific classes
        verification = 'N/A'
        agent = 'N/A'

        verification_tag = card.find_elements(By.CSS_SELECTOR, '.tag-module_tag--verified__q3T28')
        if verification_tag:
            verification = verification_tag[0].text

        agent_tag = card.find_elements(By.CSS_SELECTOR, '.tag-module_tag--super-agent__zoolh')
        if agent_tag:
            agent = agent_tag[0].text

        return {
            'Verification': verification,
            'Agent': agent,
            'Type': card.find_element(By.CSS_SELECTOR, '[data-testid="property-card-type"]').text,
            'Rent': card.find_element(By.CSS_SELECTOR, '[data-testid="property-card-price"]').text,
            'Location': card.find_element(By.CSS_SELECTOR, '[data-testid="property-card-location"]').text,
            'Bedroom': card.find_element(By.CSS_SELECTOR, '[data-testid="property-card-spec-bedroom"]').text if card.find_elements(By.CSS_SELECTOR, '[data-testid="property-card-spec-bedroom"]') else 'N/A',
            'Bathroom': card.find_element(By.CSS_SELECTOR, '[data-testid="property-card-spec-bathroom"]').text if card.find_elements(By.CSS_SELECTOR, '[data-testid="property-card-spec-bathroom"]') else 'N/A',
            'Area': card.find_element(By.CSS_SELECTOR, '[data-testid="property-card-spec-area"]').text if card.find_elements(By.CSS_SELECTOR, '[data-testid="property-card-spec-area"]') else 'N/A'
        }
    except Exception as e:
        print(f"Error extracting property: {e}")
        return None

def save_to_csv(data, filename_prefix="property_data"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'{filename_prefix}_{timestamp}.csv'

    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'Verification', 'Agent', 'Type', 'Rent', 
            'Location', 'Bedroom', 'Bathroom', 'Area'
        ])
        writer.writeheader()
        writer.writerows(data)

    print(f"Successfully saved {len(data)} properties to {filename}")

def scrape_properties(num_pages_to_scrape=100, chunk_size=20):
    properties = []
    driver = start_driver()

    try:
        for page in range(1, num_pages_to_scrape + 1):
            try:
                print(f"Scraping page {page}...")
                driver.get(base_url.format(page=page))

                WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.property-card-module_property-card__body__pTwgB'))
                )

                property_cards = driver.find_elements(By.CSS_SELECTOR, '.property-card-module_property-card__body__pTwgB')
                for card in property_cards:
                    if details := extract_property_details(card):
                        properties.append(details)

            except Exception as e:
                print(f"Error on page {page}: {e}")
                if "invalid session id" in str(e):
                    print("Restarting browser due to invalid session...")
                    driver.quit()
                    driver = start_driver()

            # Restart driver periodically to avoid session issues
            if page % chunk_size == 0:
                print(f"Restarting browser after {chunk_size} pages...")
                driver.quit()
                save_to_csv(properties, filename_prefix="property_data_partial")
                driver = start_driver()

    except Exception as e:
        print(f"Session error encountered: {e}")

    finally:
        driver.quit()

    return properties

# Run the scraper
all_properties = scrape_properties(num_pages_to_scrape=100, chunk_size=20)
save_to_csv(all_properties)
