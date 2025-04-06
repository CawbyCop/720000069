"""
This script scrapes job listings for data analyst positions from Reed.co.uk in the UK,
extracting job title, skills, job types and locations mentioned. 
The results are saved to a CSV file in data/ directory.
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import os

BASE_URL = "https://www.reed.co.uk"
SEARCH_URL_TEMPLATE = "/jobs/data-analyst-jobs-in-united-kingdom?pageno={page}"
MAX_PAGES = 1
OUTPUT_CSV = 'data/reed_uk_data_analyst_skills.csv' 

# Technical skills to search for
SKILLS_TO_FIND = [
    'python', 'r', 'sql', 'java', 'julia', 'scala', 'c', 'javascript', 'swift', 'go', 'matlab', 'sas',
    'excel', 'powerbi', 'power bi', 'tableau', 'spark', 'datalab', 'qlik', 'cpp'
]

# Avoid duplicates
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
        # Convert c++ to cpp
        text = re.sub(r'C\+\+', 'CPP', text, flags=re.IGNORECASE)
        text = text.lower()
        
        # Replace grade references with empty string for grade (c) example which detects it as c programming language
        text = re.sub(r'grade\s*\d+\s*\(c\)', '', text, flags=re.IGNORECASE)
        
        # Remove common punctuation
        text = re.sub(r'[(),/:;]', ' ', text)
        
        # Handle all skills
        for skill in skills_list:
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

    # Find all job cards
    job_cards = search_soup.find_all('article', {'data-card': 'job'})
    if not job_cards:
        job_cards = search_soup.find_all('article', class_=re.compile(r'job-card_jobCard__\w+'))
    
    print(f"Found {len(job_cards)} jobs on page {page_num}")

    for card in job_cards:
        # Job title
        job_link_tag = card.find('a', attrs={'data-qa': 'job-card-title'})
        if not (job_link_tag and 'href' in job_link_tag.attrs):
            continue
        # Job link
        job_url = job_link_tag['href']
        if not job_url.startswith('http'):
            job_url = BASE_URL + job_url
            
        # Duplicate check
        if job_url in processed_urls:
            print(f"\nSkipping card: Already processed URL {job_url}")
            continue
        processed_urls.add(job_url)

        job_title = job_link_tag.text.strip()
        print(f"\nProcessing: {job_title}")

        # Extract salary
        salary = "Not specified"
        salary_tag = None
        # Search for list items containing salary information
        for li in card.find_all('li'):
            if li.text and re.search(r'£|\bper\b|salary|annum|hour|day|week|month|year', li.text.lower()):
                salary_tag = li
                break
        
        if salary_tag:
            salary = salary_tag.text.strip()
        print(f"Salary: {salary}")
        
        # Extract location
        location = "Not specified"
        location_tag = card.find('li', attrs={'data-qa': 'job-card-location'})
        if location_tag:
            location = location_tag.text.strip()
        print(f"Location: {location}")
            
        # Extract job type
        job_type = "Not specified"
        metadata_list = card.find_all('li', class_=re.compile(r'job-card_jobMetadata__\w+'))
        for item in metadata_list:
            if item.text and "permanent" in item.text.lower() or "contract" in item.text.lower() or "temporary" in item.text.lower():
                job_type = item.text.strip()
                break
        print(f"Job type: {job_type}")

        # Individual job page
        job_soup = get_soup(job_url)
        if not job_soup:
            continue

        # Extract job description
        description_area = job_soup.find('div', {'class': 'description'})

        found_skills = []
        if description_area:
            # Combine all text parts and clean up whitespace
            job_description = ' '.join(part.strip() for part in description_area.stripped_strings)
            found_skills = extract_skills(job_description, SKILLS_TO_FIND)
            
        if found_skills:
            print(f"Found skills: {', '.join(found_skills)}")
            all_job_data.append({
                'job_title': job_title,
                'job_url': job_url,
                'location': location,
                'job_type': job_type,
                'salary': salary,
                'skills': ', '.join(sorted(found_skills))
            })
        else:
            print("No relevant skills found")

        time.sleep(2)  # Basic rate limiting between job pages
    
    print(f"\nCompleted page {page_num}. Total jobs with skills found: {len(all_job_data)}")
    time.sleep(3)  # Pause between search result pages




############################# Save results to CSV ##############################
if all_job_data:
    print(f"\nScraping finished. Saving {len(all_job_data)} jobs to {OUTPUT_CSV}")
    try:
        
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['job_title', 'job_url', 'location', 'job_type', 'salary', 'skills'])
            writer.writeheader()
            writer.writerows(all_job_data)
        print("Successfully saved to CSV")
    except Exception as e:
        print(f"Error saving data: {e}")
else:
    print("No jobs with matching skills found")