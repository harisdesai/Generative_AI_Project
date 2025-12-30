import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. Setup Browser
options = Options()
options.add_argument("--headless") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_aboutUS(url, filename):
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    
    # Final data structure
    page_data = {
        "url": url,
        "main_content": [],
        "accordion_data": []
    }

    try:
        # A. Extract the main descriptive paragraphs (About Us style)
        # We target the main content area by looking for paragraph tags
        main_paragraphs = driver.find_elements(By.TAG_NAME, "p")
        page_data["main_content"] = [p.text.strip() for p in main_paragraphs if len(p.text) > 20]

        # B. Extract Interactive Accordions (Course Details/Branches)
        # Sunbeam uses 'panel-heading' for clickable sections across different pages
        headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
        
        for i in range(len(headers)):
            current_headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
            header = current_headers[i]
            title = header.text.strip()
            
            # Click to reveal hidden content
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header)
            time.sleep(1)
            try:
                link = header.find_element(By.TAG_NAME, "a")
                driver.execute_script("arguments[0].click();", link)
                time.sleep(2) # Wait for expansion
            except:
                continue

            # Identify the revealed panel body
            panel_body = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in .panel-body")
            
            # CHECK FOR TABLES: If found, process row-by-row into dictionaries
            tables = panel_body.find_elements(By.TAG_NAME, "table")
            if tables:
                table_list = []
                table = tables[0]
                headers_list = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
                rows = table.find_elements(By.TAG_NAME, "tr")[1:] # Skip header
                
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if cells:
                        row_dict = {headers_list[j]: cells[j].text.strip() for j in range(len(cells))}
                        table_list.append(row_dict)
                
                page_data["accordion_data"].append({"title": title, "type": "table", "content": table_list})
            else:
                # Regular text content for non-table sections
                page_data["accordion_data"].append({"title": title, "type": "text", "content": panel_body.text.strip()})

        # 3. Save to JSON
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(page_data, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved {url} to {filename}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Run for both pages
scrape_aboutUS("https://sunbeaminfo.in/about-us", "sunbeam_about_us.json")
driver.quit()