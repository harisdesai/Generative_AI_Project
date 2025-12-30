import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
def scrape_modular_courses(URL, course_name, output_filename):
    # 1. Setup Browser
    options = Options()
    options.add_argument("--headless") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        url = URL   
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Data structure for this specific course
        course_data = {
            "course_name": course_name,
            "url": url,
            "general_info": {},
            "sections": [],
            "batch_schedule_table": []
        }

        # 2. Extract General Info (Course Summary)
        try:
            info_container = driver.find_element(By.CLASS_NAME, "course_info")
            course_data["general_info"] = {
                "summary": info_container.text.strip().replace('\n', ' | ')
            }
        except:
            course_data["general_info"] = {"summary": "Summary section not found"}

        # 3. Handle Accordions (Syllabus, Eligibility, Schedule)
        headers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "panel-heading")))
        
        for i in range(len(headers)):
            current_headers = driver.find_elements(By.CLASS_NAME, "panel-heading")
            header = current_headers[i]
            header_text = header.text.strip()
            
            # Click to expand
            link = header.find_element(By.TAG_NAME, "a")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", link)
            time.sleep(2) # Wait for content to render
            
            # Check for Batch Schedule Table
            if "Batch schedule" in header_text:
                try:
                    table = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in table")
                    
                    # Get Headers
                    th_elements = table.find_elements(By.TAG_NAME, "th")
                    table_headers = [th.text.strip() for th in th_elements]
                    
                    # If no TH tags, use the first row as headers
                    rows = table.find_elements(By.TAG_NAME, "tr")
                    if not table_headers and rows:
                        table_headers = [td.text.strip() for td in rows[0].find_elements(By.TAG_NAME, "td")]
                        data_rows = rows[1:]
                    else:
                        data_rows = rows[1:]

                    for row in data_rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if cells:
                            row_dict = {table_headers[j]: cells[j].text.strip() for j in range(len(cells)) if j < len(table_headers)}
                            course_data["batch_schedule_table"].append(row_dict)
                    print("Captured Batch Schedule Table.")
                except Exception as e:
                    print(f"Table error in {header_text}: {e}")
            
            else:
                # Capture Text Sections (Syllabus, etc.)
                try:
                    body = driver.find_element(By.CSS_SELECTOR, ".panel-collapse.collapse.in .panel-body")
                    course_data["sections"].append({
                        "title": header_text,
                        "content": body.get_attribute("textContent").strip()
                    })
                    print(f"Captured Section: {header_text}")
                except:
                    continue

        # 4. Save Final JSON
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(course_data, f, indent=4, ensure_ascii=False)
            
        print(f"\nSuccess! Data saved to {output_filename}")

    finally:
        driver.quit()