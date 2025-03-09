import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def scrape_website(
        website,
        scrolls: int = 0,
        settings_required: bool = False
        ) -> str:
    print("Launching chrome browser")

    chrome_driver_path = "../ai_webscraper/chromedriver"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page loaded...")

        if settings_required:
            # code to load webpage, automatically fill whatever can be entered
            x = input("Waiting for manual date to be entered. Enter YES when done.")
            # Enter the data on page manually. Then come back to terminal and type YES and then press enter.
            if x == 'YES':
                pass
            else:
                driver.quit
            
        body_content = extract_body_content(driver.page_source)
        first_cleaned_content = clean_body_content(body_content)
        html = first_cleaned_content

        if scrolls > 0:
            scroll_count = 1
            text = f"total scrolls: {scrolls}\n"
            with open("output/scroll_counter.txt", "a") as text_file:
                    text_file.write(text)
            # Simulate scroll events to load additional content
            while scroll_count <= int(scrolls):
                print(f"Now executing scrol number {scroll_count}")
            # Scroll down using JavaScript
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.implicitly_wait(10)
                time.sleep(2)

                with open("output/scroll_counter.txt", "a") as text_file:
                    text = f"\ncurrent scroll: {scroll_count}"
                    text_file.write(text)

                # html = html + cleaned_content
                scroll_count += 1

            body_content = extract_body_content(driver.page_source)
            cleaned_content = clean_body_content(body_content)

            return cleaned_content
        
        else:
            return html
        
    finally:
        driver.quit


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
        )

    return cleaned_content

def split_dom_content(dom_content, max_length = 6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
