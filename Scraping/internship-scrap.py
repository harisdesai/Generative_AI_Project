import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_full_internship_data(url, output_filename):
    options = Options()
    # options.add_argument("--headless") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Main data structure to hold EVERYTHING
        full_data = {
            "program_name": "Internship Program",
            "url": url,
            "general_sections": [],     # Standard text from page accordions
            "technology_matrix": [],    # Table 1: Course offerings
            "batch_schedule": []        # Table 2: Dates and Fees
        }

        # --- 1. CAPTURE ALL GENERAL ACCORDIONS & TECHNOLOGY MATRIX ---
        print("Scraping page sections and technology matrix...")
        headers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "panel-heading")))
        
        for i in range(len(headers)):
            # Re-fetch to avoid stale elements
            current_headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
            header = current_headers[i]
            title_text = header.text.strip()
            
            # Click to expand
            link = header.find_element(By.TAG_NAME, "a")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", link)
            time.sleep(2)

            panel_body = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in .panel-body")
            
            # Check if this specific section contains the Technology Matrix Table
            tables = panel_body.find_elements(By.TAG_NAME, "table")
            if tables and ("Available" in title_text or "Technology" in title_text):
                table = tables[0]
                rows = table.find_elements(By.TAG_NAME, "tr")
                # Using the first row as headers (Technology, Aim, Prerequisite, etc.)
                matrix_keys = [td.text.strip() for td in rows[0].find_elements(By.TAG_NAME, "td")]
                
                for row in rows[1:]:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) == len(matrix_keys):
                        row_data = {matrix_keys[j]: cells[j].text.strip() for j in range(len(cells))}
                        full_data["technology_matrix"].append(row_data)
                print(f"Captured Technology Matrix from section: {title_text}")
            else:
                # Store as regular text section
                full_data["general_sections"].append({
                    "title": title_text,
                    "content": panel_body.text.strip()
                })

        # --- 2. CAPTURE STANDALONE BATCH SCHEDULE (Bottom Table) ---
        print("Scraping Batch Schedule...")
        try:
            schedule_wrapper = driver.find_element(By.CLASS_NAME, "table-responsive")
            table = schedule_wrapper.find_element(By.TAG_NAME, "table")
            
            # Headers: Sr.No, Batch, Start Date, etc.
            headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
            
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= len(headers):
                    row_data = {headers[j]: cells[j].text.strip() for j in range(len(headers))}
                    full_data["batch_schedule"].append(row_data)
            print("Captured Batch Schedule Table.")
        except Exception as e:
            print(f"Schedule table not found or error: {e}")

        # 3. SAVE TO ONE FILE
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(full_data, f, indent=4, ensure_ascii=False)
            
        print(f"\nSUCCESS! All data combined into {output_filename}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_full_internship_data("https://sunbeaminfo.in/internship", "sunbeam_internship_full.json")