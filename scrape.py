import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def scrape_website(website, scrolls: int = 0):
    print("Launching chrome browser")

    chrome_driver_path = "../ai_webscraper/chromedriver"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("Page loaded...")
        body_content = extract_body_content(driver.page_source)
        cleaned_content = clean_body_content(body_content)
        html = cleaned_content
        

        if scrolls > 0:
            scroll_count = 0
            text = f"total scrolls: {scrolls}\n"
            with open("scroll_counter.txt", "a") as text_file:
                    text_file.write(text)
            # Simulate scroll events to load additional content
            while scroll_count <= int(scrolls):
            # Scroll down using JavaScript
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.implicitly_wait(5)

                body_content = extract_body_content(driver.page_source)
                cleaned_content = clean_body_content(body_content)

                with open("scroll_counter.txt", "a") as text_file:
                    text = f"\ncurrent scroll: {scroll_count}"
                    text_file.write(text)

                html = html + cleaned_content
                scroll_count += 1

            return html
        
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
