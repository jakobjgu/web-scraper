import streamlit as st
import sys
sys.path.append('../ai_webscraper')
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content
    )

st.title("AI Web Scraper")
url = st.text_input("Enter a URL")
scrolls = st.number_input("Enter the number of simulated scrolls:")

if (st.button("Scrape Site")) and (scrolls > 0):

    st.write("Scraping the website")
    result = scrape_website(url, scrolls)

    # body_content = extract_body_content(result)
    # cleaned_content = clean_body_content(body_content)

    # st.session_state.dom_content = cleaned_content

    # with st.expander("View DOM Content"):
    #     st.text_area("DOM Content", cleaned_content, height=300)

    with open("cleaned_content.txt", "w") as text_file:
        text_file.write(result)

    