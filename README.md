# Capstone Project - Web Scraping & Data Visualization

## Project Overview
This project involves web scraping commercial rental property listings from **PropertyFinder.ae** using **Selenium**. The extracted data is then cleaned using **Jupyter Notebook** and visualized in **Tableau**.

## Contents
1. **Web Scraping Code**
   - The script is written in Python using **Selenium**.
   - It extracts property details such as type, rent, location, number of bedrooms, bathrooms, area, verification status, and agent type.
   - The extracted data is saved as a CSV file.
   
2. **Website Scraped**
   - **PropertyFinder URL:** [https://www.propertyfinder.ae/](https://www.propertyfinder.ae/)
   - The script scrapes multiple pages of property listings dynamically.

3. **Data Cleaning**
   - Data cleaning was performed using **Jupyter Notebook**.
   - The cleaning script is located at:
     - `CapstoneProjectDataCleaning.ipynb`

4. **Tableau Dashboard**
   - The cleaned data was visualized using **Tableau Public**.
   - **Tableau Dashboard URL:** [View Dashboard](https://public.tableau.com/views/capstone_project-01/Dashboard2?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

5. **Useful Links**
   - The **PropertyFinder URL** and **Tableau Dashboard URL** are stored in `usefulurl.txt`.

## How to Run the Web Scraper
### Prerequisites
- Install Python (>=3.7)
- Install required libraries:
  ```sh
  pip install selenium
  ```
- Download and install **ChromeDriver** (Ensure compatibility with your Chrome version)

### Steps to Run
1. Update the `webdriver_path` in the script to match your **ChromeDriver** location.
2. Run the script using:
   ```sh
   python your_script.py
   ```
3. The extracted data will be saved as a CSV file with a timestamp.

## File Structure
```
CapstoneProject/
│-- CapstoneProjectDataCleaning.ipynb  # Data cleaning script
│-- usefulurl.txt                       # Contains PropertyFinder & Tableau links
│-- your_script.py                      # Web Scraping script
│-- scraped_data/                        
│   ├── property_data_YYYYMMDD_HHMMSS.csv  # Scraped data
```

## Notes
- The script includes error handling and session restarts to avoid timeouts.
- **Tableau Dashboard** provides interactive visualization of property listings.

## Author
- **Nurul Bashar**

