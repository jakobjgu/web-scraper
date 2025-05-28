# web-scraper

A compact web-scraping tool for local machines written in Python with Selenium and Streamlit. Includes optional AI-assisted parsing via Ollama LLM.

---

## Table of Contents

1. [Setup](#setup)  
2. [External Requirements](#external-requirements)  
3. [Usage](#usage)  
4. [Data Cleaning](#data-cleaning)  
5. [Disclaimer](#disclaimer)

---

## Setup

1. **Clone the repo**  
   ```bash
   git clone https://github.com/jakobjgu/web-scraper.git
   cd web-scraper
   ```

2. **Create & activate a virtual environment**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install Python dependencies**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

## External Requirements
1. **Chromedriver**
- Must match your installed Chrome version.
- Download the latest stable release [here](https://googlechromelabs.github.io/chrome-for-testing/#stable).
- On macOS, remove the quarantine flag if needed:
```xattr -d com.apple.quarantine ~/path/to/chromedriver```

2. **Ollama LLM (Optional)**
- Install Ollama from [ollama.com/download](https://ollama.com/download).
- Choose and pull a model (e.g. llama3.2):
```ollama pull llama3.2```
- Edit parse.py to reference your chosen model name for AI-assisted parsing.
- for testing or local use you can also invoke your model in the terminal:
```ollama run llama3.2```

## Usage
1. **Run the Streamlit app**
```streamlit run main.py```

2. **Configure options in the UI:**
- Toggle saving raw scraped content locally.
- Select an Ollama LLM model if using AI parsing.
Start scraping

3. **Enter your target URL.**
- Click “Scrape Site” to collect data from dynamically-loaded pages.
- View the results in your browser or download as CSV.

## Data Cleaning
If you saved raw output locally, you can write project-specific cleaning scripts, or refactor the ones in ```process_cleaned_text.py``` based on your data format and cleaning needs.

## Disclaimer
This implementation builds on techniques from public tutorials and articles:<br> 
[TechWithTim](https://www.techwithtim.net/) – YouTube scraping [tutorial](https://www.youtube.com/watch?v=Oo8-nEuDBkk&t=2082s)<br> 
[Writer Bricks](https://medium.com/@writerbricks) – [Medium article](https://medium.com/@writerbricks/scraping-dynamic-data-that-loads-on-scroll-with-python-c4c4970a54d1) on dynamic-scroll scraping<br> 
The core scraping and data-cleaning logic beyond basic examples was developed in-house for this project.<br>
