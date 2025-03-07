import requests
from bs4 import BeautifulSoup
import spacy
import streamlit as st

def get_website_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ')
    except requests.RequestException as e:
        return f"Error fetching website: {e}"

def analyze_subscription(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())
    
    subscription_keywords = {"subscribe", "membership", "premium", "paywall", "pricing", "unlimited access", "trial"}
    found_keywords = {token.text for token in doc if token.text in subscription_keywords}
    
    if found_keywords:
        if "free trial" in text.lower() or "limited access" in text.lower():
            return "Freemium Model: Some content is free, but full access requires a subscription."
        return "Paid Subscription Required: This website seems to require a membership."
    
    return "Free Access: This website appears to be free to use."

def main():
    st.title("Subscriptify - Website Subscription Checker")
    st.write("Enter a website URL to check its subscription model.")
    
    url = st.text_input("Website URL:")
    if st.button("Check Subscription"):
        if url.strip():
            text = get_website_text(url.strip())
            if text and not text.startswith("Error"):
                result = analyze_subscription(text)
                st.success(result)
            else:
                st.error("Unable to fetch website content. The website may block scraping.")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
