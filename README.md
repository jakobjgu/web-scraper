# web-scraper
A compact web-scraping tool for local machines written in Python with Selenium and Streamlit

# Disclaimer:

I did not come up with this project. I was asked by a friend to look into scraping data from a website with dynamically loaded content, and API based scraping didn't seem to be the way to go (as far as I could see with my very limited experience). So I followed various tutorials and cobbled together this little project, which in the end did what I set out to do.

But I want to make it very clear that I am not taking credit for this, as it is largely based on the work of other people, mainly Tim from [TechWithTim](https://www.techwithtim.net/) (this is his YouTube [video](https://www.youtube.com/watch?v=Oo8-nEuDBkk&t=2082s) that is responsible for the main body of this project), and a [Medium Article](https://medium.com/@writerbricks/scraping-dynamic-data-that-loads-on-scroll-with-python-c4c4970a54d1) by [Writer Bricks](https://medium.com/@writerbricks), which helped me with the dynamic scrolling part.

# Instructions
This code is largely self-contained, but in order to run it, two external elements need to be installed locally:
1. Chromedriver
2. Ollama LLM

### Chromedriver
The Chromedriver that needs to be installed has to match the version of Chrome that is installed on ytour system. The latest stable chromedriver release can be found [here](https://googlechromelabs.github.io/chrome-for-testing/#stable).

### Ollama LLM
The use of an LLM is not needed for the scraping part of the code, but represents an optional element to parse the scraped content. You first need to install Ollama (from [here](https://ollama.com/download)). Then you can check out which model you want to use (depending on system limitations like space and ram). Details can be found in this [list](https://github.com/ollama/ollama)(scroll down to "Model Library"). Once you picked a model, you can install it using the Ollama CLI (for example llama3.2) ```ollama pull llama3.2```. You then need to add the appropriate model name in the model definition of the ```parse.py``` file.

# Data Cleaning
Instead of using the LLM for data parsing, you can also store the scraped content locally (this option can be set in the Streamlit UI before scraping starts) and then clean/analyze the data locally yourself. For my particular project I used the funtions defined in  ```process_cleaned_text.py```, but that is highly specific to the structure of the text data scraped from a specific site for my project.