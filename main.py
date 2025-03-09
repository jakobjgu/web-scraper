import streamlit as st
import sys
sys.path.append('../ai_webscraper')
from scrape import (
    scrape_website,
    split_dom_content
    )
from parse import parse_with_ollama

st.title("AI Web Scraper")
url = st.text_input("Enter a URL")
scrolls = st.number_input("Enter the number of simulated scrolls:")

left, right = st.columns(2, vertical_alignment="bottom")
option1 = left.selectbox(
    "Does the website you want to scrape require user input or settings before the scraping starts?",
    ("No", "Yes")
)
option2 = right.selectbox(
    "Do you want to save the scraped content for local cleaning and analysis later?",
    ("No", "Yes")
)

settings_required = False
save_locally = False
if option1 == "Yes":
    settings_required = True
if option2 == "Yes":
    save_locally = True

if st.button("Scrape Site"):

    st.write("Scraping the website")
    result = scrape_website(url, scrolls, settings_required)
    print("Done Scraping.")
    st.session_state.dom_content = result

    with st.expander("View DOM Content"):
        st.text_area("DOM Content", result, height=300)

    if save_locally:
        with open("output/scraped_content.txt", "w") as text_file:
            text_file.write(result)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe how you want the scraped content to be parsed.")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the scraped content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(
                dom_chunks=dom_chunks,
                parsing_description=parse_description
                )
            st.write(result)
            
    