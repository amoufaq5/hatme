# scraping/scraper.py
import requests
from bs4 import BeautifulSoup
import logging
from database import get_db_connection

def scrape_pubmed():
    """
    Scrape recent articles from PubMed.
    Note: In production, use the official PubMed API.
    """
    url = "https://pubmed.ncbi.nlm.nih.gov/"
    articles = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for article_div in soup.find_all('div', class_='docsum-content'):
            title_tag = article_div.find('a', class_='docsum-title')
            if title_tag:
                title = title_tag.get_text(strip=True)
                articles.append({'title': title})
    except Exception as e:
        logging.exception("Error scraping PubMed")
    return articles

def scrape_clinical_trials():
    """
    Scrape data from ClinicalTrials.gov.
    Note: In production, use the official API when available.
    """
    url = "https://clinicaltrials.gov/ct2/results"
    trials = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # This is a placeholder; real extraction logic will depend on the page structure.
        for trial in soup.find_all('div', class_='trial'):
            title = trial.get_text(strip=True)
            trials.append({'title': title})
    except Exception as e:
        logging.exception("Error scraping ClinicalTrials.gov")
    return trials

def start_scraping():
    """
    Orchestrates scraping from multiple sources and stores data in the SQL database.
    """
    pubmed_data = scrape_pubmed()
    trials_data = scrape_clinical_trials()
    conn = get_db_connection()
    cursor = conn.cursor()
    for article in pubmed_data:
        cursor.execute("INSERT INTO articles (source, title) VALUES (?, ?)", ("pubmed", article['title']))
    for trial in trials_data:
        cursor.execute("INSERT INTO articles (source, title) VALUES (?, ?)", ("clinical_trials", trial['title']))
    conn.commit()
    conn.close()
