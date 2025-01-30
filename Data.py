from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless")

chrome_service = Service(r"C:\Users\Hp\Downloads\chromedriver-win64 (2)\chromedriver-win64\chromedriver.exe")

def extract_text(element, selectors):
    """Generic text extraction with multiple fallback selectors"""
    for method, selector in selectors:
        try:
            if method == 'css':
                return element.find_element(By.CSS_SELECTOR, selector).text.strip()
            elif method == 'xpath':
                return element.find_element(By.XPATH, selector).text.strip()
        except:
            continue
    return None

def extract_price(element):
    """Improved price extraction with currency handling"""
    price_selectors = [
        ('css', 'span[class*="Price"]'),
        ('css', 'div[class*="price"]'),
        ('xpath', './/*[contains(text(), "BDT") or contains(text(), "৳")]')
    ]
    
    price_text = extract_text(element, price_selectors)
    if price_text:
        # Extract numbers and format
        numbers = re.findall(r'[\d,]+', price_text)
        return numbers[0].replace(',', '') if numbers else None
    return None

def extract_feature(element, feature_name):
    """Enhanced feature extraction with unit handling"""
    feature_selectors = [
        ('xpath', f'.//div[contains(@class, "attribute") or contains(@class, "stribute")]//span[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{feature_name}")]/preceding-sibling::div'),
        ('xpath', f'.//div[contains(@class, "attribute") or contains(@class, "stribute")]//span[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{feature_name}")]/following-sibling::div')
    ]
    
    for method, selector in feature_selectors:
        try:
            element = element.find_element(By.XPATH, selector)
            value = element.text.strip()
            # Clean numerical values
            return re.sub(r'\D', '', value) if value and value != '-' else None
        except:
            continue
    return None

def is_valid_listing(entry):
    """Validate listings to filter out duplicates and incomplete entries"""
    required_fields = ['Location', 'Price', 'Bedrooms']
    return all(entry.get(field) for field in required_fields)

def main():
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    seen = set()  # Track unique listings
    
    try:
        driver.get("https://www.bproperty.com/buy/residential/")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='ListingCell']"))
        )

        listings = driver.find_elements(
            By.CSS_SELECTOR, 
            "div[class*='ListingCell']:not(.Advertisement)"
        )

        data = []
        for idx, listing in enumerate(listings, 1):
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", listing)
                time.sleep(0.5)

                entry = {
                    'Location': extract_text(listing, [
                        ('css', 'span.ListingCell-keyInfo-address-text'),
                        ('css', 'span.ListingCell-keyInfo-address-test'),
                        ('xpath', './/span[contains(@class, "address")]')
                    ]),
                    'Price': extract_price(listing),
                    'Bedrooms': extract_feature(listing, 'bedroom'),
                    'Bathrooms': extract_feature(listing, 'bathroom'),
                    'Area': extract_feature(listing, 'floor area')
                }

                # Create unique identifier for duplicate check
                entry_hash = hash(frozenset(entry.items()))
                if is_valid_listing(entry) and entry_hash not in seen:
                    seen.add(entry_hash)
                    data.append(entry)
                    print(f"✅ Valid listing {idx}: {entry['Location']}")
                else:
                    print(f"🚫 Skipped listing {idx} (duplicate/invalid)")

            except Exception as e:
                print(f"⚠️ Error listing {idx}: {str(e)[:80]}")
                continue

        # Create and clean DataFrame
        df = pd.DataFrame(data)
        df.replace([None], pd.NA, inplace=True)
        df.dropna(subset=['Location', 'Price'], how='all', inplace=True)
        
        if not df.empty:
            df.to_csv('Data_property_listings.csv', index=False)
            print(f"\n🎉 Success! Saved {len(df)} unique listings")
            print(df.head(10))
        else:
            print("\n❌ No valid data collected")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()