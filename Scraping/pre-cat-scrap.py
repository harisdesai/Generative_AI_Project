import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. Setup Browser Options
options = Options()
# options.add_argument("--headless") # Uncomment to run without opening a window
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_sunbeam_page(url):
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    
    # Dictionary to hold the final complete data
    full_data = {
        "page_url": url,
        "general_info": {},
        "accordion_sections": []
    }

    try:
        # A. Extract Static Top Content (Course Name, Fees, etc.)
        # Based on your image, capturing the course title and basic info
        full_data["general_info"]["course_title"] = driver.find_element(By.TAG_NAME, "h3").text
        
        # B. Handle Accordion Sections (Course Contents, Eligibility, Schedule)
        # Find all clickable headers (panel-heading class from your DevTools image)
        headers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "panel-heading")))
        
        for i in range(len(headers)):
            # Re-fetch headers to avoid stale element exceptions after DOM changes
            current_headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
            header = current_headers[i]
            section_title = header.text.strip()
            
            # Click to expand section
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header)
            time.sleep(0.5)
            link = header.find_element(By.TAG_NAME, "a")
            driver.execute_script("arguments[0].click();", link)
            time.sleep(1.5) # Wait for animation to finish
            
            section_data = {"title": section_title}
            
            # Find the expanded body
            panel_body = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in .panel-body")
            
            # Check if this section contains a Table (Batch Schedule)
            tables = panel_body.find_elements(By.TAG_NAME, "table")
            if tables:
                table_data = []
                table = tables[0]
                
                # Extract Table Headers
                th_elements = table.find_elements(By.TAG_NAME, "th")
                table_headers = [th.text.strip() for th in th_elements]
                
                # Extract Table Rows
                rows = table.find_elements(By.TAG_NAME, "tr")[1:] # Skip header row
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if cells:
                        # Map headers to cell values in a dictionary
                        row_dict = {table_headers[j]: cells[j].text.strip() for j in range(len(cells))}
                        table_data.append(row_dict)
                section_data["type"] = "table"
                section_data["content"] = table_data
            else:
                # Regular text content
                section_data["type"] = "text"
                section_data["content"] = panel_body.text.strip()
            
            full_data["accordion_sections"].append(section_data)
            print(f"Scraped section: {section_title}")

        # 3. Save the final object to JSON
        with open("Pre-CAT.json", "w", encoding="utf-8") as f:
            json.dump(full_data, f, indent=4, ensure_ascii=False)
        print("\nSuccess! Data saved to Pre-CAT.json")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# Run the scraper
scrape_sunbeam_page("https://sunbeaminfo.in/pre-cat")