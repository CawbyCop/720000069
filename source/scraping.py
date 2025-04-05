"""
Reed.co.uk data analyst job skills scraper in UK

This script scrapes job listings for data analyst positions from Reed.co.uk,
extracting technical skills mentioned in job descriptions. 
The results are saved to a CSV file.
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re

BASE_URL = "https://www.reed.co.uk"
SEARCH_URL_TEMPLATE = "/jobs/data-analyst-jobs-in-united-kingdom?pageno={page}"
MAX_PAGES = 1
OUTPUT_CSV = 'data/reed_uk_data_analyst_skills.csv' 

# List of technical skills to search for in job descriptions
SKILLS_TO_FIND = [
    'python', 'r', 'sql', 'java', 'julia', 'scala', 'c', 'c++', 'javascript', 'swift', 'go', 'matlab', 'sas',
    'excel', 'powerbi', 'power bi', 'tableau', 'spark', 'datalab', 'qlik'
]

# Track processed URLs to avoid duplicates
processed_urls = set()

############################# Helper functions ##############################

def get_soup(url):
    """
    Fetches and parses a webpage using beautifulsoup
    """
    try:
        response = requests.get(url, timeout=25)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}")
        return None

def extract_skills(text, skills_list):
    """
    Extracts mentioned skills from text using regex pattern matching
    """
    found_skills = set()
    if text:
        text = text.lower()
        # Remove common punctuation that might interfere with word boundaries
        text = re.sub(r'[(),/:;]', ' ', text)
        for skill in skills_list:
            # Use word boundaries to avoid partial matches
            if re.search(r'\b' + re.escape(skill) + r'\b', text):
                found_skills.add(skill)
    return list(found_skills)

############################# Main scraping logic ##########################################

all_job_data = []
print("Starting scrape...")

for page_num in range(1, MAX_PAGES + 1):
    search_url = BASE_URL + SEARCH_URL_TEMPLATE.format(page=page_num)
    print(f"\nScraping page {page_num}")
    
    # Get the search results page
    search_soup = get_soup(search_url)
    if not search_soup:
        continue

    # Find all job cards, handling different possible HTML structures
    job_cards = search_soup.find_all('article', {'data-card': 'job'})
    if not job_cards:
        job_cards = search_soup.find_all('article', class_=re.compile(r'job-card_jobCard__\w+'))
    
    print(f"Found {len(job_cards)} jobs on page {page_num}")

    for card in job_cards:
        # Job link and title
        job_link_tag = card.find('a', attrs={'data-qa': 'job-card-title'})
        if not (job_link_tag and 'href' in job_link_tag.attrs):
            continue

        job_url = job_link_tag['href']
        if not job_url.startswith('http'):
            job_url = BASE_URL + job_url
            
        # Duplicate check
        if job_url in processed_urls:
            print(f"Skipping card: Already processed URL {job_url}")
            continue
        processed_urls.add(job_url)

        job_title = job_link_tag.text.strip()
        print(f"Processing: {job_title[:60]}...")
        
        # Individual job page
        job_soup = get_soup(job_url)
        if not job_soup:
            continue

        # Try different possible selectors for job description
        description_area = job_soup.find('div', {'class': 'description'})
        if not description_area:
            for selector in ['jobdescription', 'job-description']:
                description_area = job_soup.find(['div', 'section'], {'class': selector}) or job_soup.find(['div', 'section'], {'id': selector})
                if description_area:
                    break

        if description_area:
            # Combine all text parts and clean up whitespace
            job_description = ' '.join(part.strip() for part in description_area.stripped_strings)
            found_skills = extract_skills(job_description, SKILLS_TO_FIND)
            if found_skills:
                print(f"Found skills: {', '.join(found_skills)}")
                all_job_data.append({
                    'job_title': job_title,
                    'job_url': job_url,
                    'skills': ', '.join(sorted(found_skills))
                })

        time.sleep(2)  # Basic rate limiting between job pages
    
    print(f"Completed page {page_num}. Total jobs with skills found: {len(all_job_data)}")
    time.sleep(5)  # Pause between search result pages




############################# Save results to CSV ##############################
if all_job_data:
    print(f"\nScraping finished. Saving {len(all_job_data)} jobs to {OUTPUT_CSV}")
    try:
        import os
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['job_title', 'job_url', 'skills'])
            writer.writeheader()
            writer.writerows(all_job_data)
        print("Successfully saved to CSV")
    except Exception as e:
        print(f"Error saving data: {e}")
else:
    print("No jobs with matching skills found")