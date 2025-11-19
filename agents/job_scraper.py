"""
Job Scraper - Searches for jobs across multiple European job boards
"""

import asyncio
import requests
from datetime import datetime
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time


class JobScraper:
    """Main job scraper for European job boards"""

    def __init__(self, config: dict):
        """Initialize the job scraper with configuration"""
        self.config = config
        self.profile = config['profile']
        self.job_prefs = self.profile['job_preferences']

        # Setup browser options
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        self.jobs = []

    async def search_europe(self) -> List[Dict]:
        """Search for jobs across all European job boards"""
        print("🔍 Searching European job boards...")

        # Run all scrapers in parallel
        tasks = [
            self.scrape_linkedin(),
            self.scrape_indeed_europe(),
            self.scrape_glassdoor_europe(),
            self.scrape_eurojobs(),
            self.scrape_stepstone(),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine all results
        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)

        # Remove duplicates
        unique_jobs = self._remove_duplicates(all_jobs)

        return unique_jobs

    async def scrape_linkedin(self) -> List[Dict]:
        """Scrape jobs from LinkedIn"""
        print("  → Searching LinkedIn...")
        jobs = []

        try:
            # Build LinkedIn search URL
            titles = self.job_prefs['titles']
            locations = self.profile['location']['preferred_countries']

            for title in titles[:2]:  # Limit to 2 titles to avoid rate limiting
                for location in locations[:3]:  # Limit to 3 locations
                    url = self._build_linkedin_url(title, location)

                    driver = uc.Chrome(options=self.chrome_options)
                    driver.get(url)

                    time.sleep(3)  # Wait for page load

                    # Scrape job cards
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    job_cards = soup.find_all('div', class_='base-card')

                    for card in job_cards[:10]:  # Limit to 10 jobs per search
                        try:
                            job = self._parse_linkedin_job(card)
                            if job:
                                jobs.append(job)
                        except Exception as e:
                            print(f"    ⚠ Error parsing LinkedIn job: {str(e)}")
                            continue

                    driver.quit()
                    await asyncio.sleep(2)  # Rate limiting

            print(f"  ✓ Found {len(jobs)} jobs on LinkedIn")

        except Exception as e:
            print(f"  ✗ Error scraping LinkedIn: {str(e)}")

        return jobs

    async def scrape_indeed_europe(self) -> List[Dict]:
        """Scrape jobs from Indeed Europe"""
        print("  → Searching Indeed Europe...")
        jobs = []

        try:
            titles = self.job_prefs['titles']
            countries = self.profile['location']['preferred_countries']

            for title in titles[:2]:
                for country in countries[:3]:
                    # Indeed has country-specific sites
                    base_url = self._get_indeed_country_url(country)
                    url = f"{base_url}/jobs?q={title.replace(' ', '+')}&l={country}"

                    driver = uc.Chrome(options=self.chrome_options)
                    driver.get(url)

                    time.sleep(2)

                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    job_cards = soup.find_all('div', class_='job_seen_beacon')

                    for card in job_cards[:10]:
                        try:
                            job = self._parse_indeed_job(card, country)
                            if job:
                                jobs.append(job)
                        except Exception as e:
                            print(f"    ⚠ Error parsing Indeed job: {str(e)}")
                            continue

                    driver.quit()
                    await asyncio.sleep(2)

            print(f"  ✓ Found {len(jobs)} jobs on Indeed")

        except Exception as e:
            print(f"  ✗ Error scraping Indeed: {str(e)}")

        return jobs

    async def scrape_glassdoor_europe(self) -> List[Dict]:
        """Scrape jobs from Glassdoor Europe"""
        print("  → Searching Glassdoor Europe...")
        jobs = []

        try:
            titles = self.job_prefs['titles']
            locations = self.profile['location']['preferred_cities']

            for title in titles[:2]:
                for location in locations[:3]:
                    url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={title.replace(' ', '+')}&locT=C&locId=&jobType="

                    driver = uc.Chrome(options=self.chrome_options)
                    driver.get(url)

                    time.sleep(3)

                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    job_cards = soup.find_all('li', class_='react-job-listing')

                    for card in job_cards[:10]:
                        try:
                            job = self._parse_glassdoor_job(card)
                            if job:
                                jobs.append(job)
                        except Exception as e:
                            print(f"    ⚠ Error parsing Glassdoor job: {str(e)}")
                            continue

                    driver.quit()
                    await asyncio.sleep(2)

            print(f"  ✓ Found {len(jobs)} jobs on Glassdoor")

        except Exception as e:
            print(f"  ✗ Error scraping Glassdoor: {str(e)}")

        return jobs

    async def scrape_eurojobs(self) -> List[Dict]:
        """Scrape jobs from EuroJobs.com"""
        print("  → Searching EuroJobs...")
        jobs = []

        try:
            titles = self.job_prefs['titles']

            for title in titles[:2]:
                url = f"https://www.eurojobs.com/search-jobs?keywords={title.replace(' ', '+')}"

                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.content, 'html.parser')

                job_cards = soup.find_all('div', class_='job-item')

                for card in job_cards[:10]:
                    try:
                        job = self._parse_eurojobs_job(card)
                        if job:
                            jobs.append(job)
                    except Exception as e:
                        print(f"    ⚠ Error parsing EuroJobs job: {str(e)}")
                        continue

                await asyncio.sleep(2)

            print(f"  ✓ Found {len(jobs)} jobs on EuroJobs")

        except Exception as e:
            print(f"  ✗ Error scraping EuroJobs: {str(e)}")

        return jobs

    async def scrape_stepstone(self) -> List[Dict]:
        """Scrape jobs from StepStone (Germany)"""
        print("  → Searching StepStone...")
        jobs = []

        try:
            titles = self.job_prefs['titles']

            for title in titles[:2]:
                url = f"https://www.stepstone.de/5/ergebnisliste.html?ke={title.replace(' ', '+')}"

                driver = uc.Chrome(options=self.chrome_options)
                driver.get(url)

                time.sleep(2)

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                job_cards = soup.find_all('article', class_='res-1d6izly')

                for card in job_cards[:10]:
                    try:
                        job = self._parse_stepstone_job(card)
                        if job:
                            jobs.append(job)
                    except Exception as e:
                        print(f"    ⚠ Error parsing StepStone job: {str(e)}")
                        continue

                driver.quit()
                await asyncio.sleep(2)

            print(f"  ✓ Found {len(jobs)} jobs on StepStone")

        except Exception as e:
            print(f"  ✗ Error scraping StepStone: {str(e)}")

        return jobs

    def _build_linkedin_url(self, title: str, location: str) -> str:
        """Build LinkedIn job search URL"""
        base_url = "https://www.linkedin.com/jobs/search/"
        params = f"?keywords={title.replace(' ', '%20')}&location={location}"
        return base_url + params

    def _get_indeed_country_url(self, country: str) -> str:
        """Get Indeed URL for specific country"""
        country_urls = {
            "Switzerland": "https://ch.indeed.com",
            "Germany": "https://de.indeed.com",
            "Netherlands": "https://nl.indeed.com",
            "Austria": "https://at.indeed.com",
            "France": "https://fr.indeed.com",
        }
        return country_urls.get(country, "https://www.indeed.com")

    def _parse_linkedin_job(self, card) -> Dict:
        """Parse LinkedIn job card"""
        try:
            title_elem = card.find('h3', class_='base-search-card__title')
            company_elem = card.find('h4', class_='base-search-card__subtitle')
            location_elem = card.find('span', class_='job-search-card__location')
            link_elem = card.find('a', class_='base-card__full-link')

            if not all([title_elem, company_elem, location_elem, link_elem]):
                return None

            return {
                'title': title_elem.text.strip(),
                'company': company_elem.text.strip(),
                'location': location_elem.text.strip(),
                'url': link_elem['href'],
                'source': 'LinkedIn',
                'date_posted': datetime.now().isoformat(),
                'description': '',
                'salary': None,
                'remote': 'remote' in location_elem.text.lower(),
            }
        except Exception as e:
            return None

    def _parse_indeed_job(self, card, country: str) -> Dict:
        """Parse Indeed job card"""
        try:
            title_elem = card.find('h2', class_='jobTitle')
            company_elem = card.find('span', class_='companyName')
            location_elem = card.find('div', class_='companyLocation')

            if not all([title_elem, company_elem, location_elem]):
                return None

            # Extract job URL
            link = title_elem.find('a')
            job_url = f"https://www.indeed.com{link['href']}" if link else None

            return {
                'title': title_elem.text.strip(),
                'company': company_elem.text.strip(),
                'location': location_elem.text.strip(),
                'url': job_url,
                'source': 'Indeed',
                'country': country,
                'date_posted': datetime.now().isoformat(),
                'description': '',
                'salary': None,
                'remote': 'remote' in location_elem.text.lower(),
            }
        except Exception as e:
            return None

    def _parse_glassdoor_job(self, card) -> Dict:
        """Parse Glassdoor job card"""
        # Implementation similar to above
        return None

    def _parse_eurojobs_job(self, card) -> Dict:
        """Parse EuroJobs job card"""
        # Implementation similar to above
        return None

    def _parse_stepstone_job(self, card) -> Dict:
        """Parse StepStone job card"""
        # Implementation similar to above
        return None

    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on title and company"""
        seen = set()
        unique_jobs = []

        for job in jobs:
            key = (job.get('title', '').lower(), job.get('company', '').lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)

        return unique_jobs

    async def search_worldwide(self) -> List[Dict]:
        """Search for jobs worldwide (future implementation)"""
        # For now, just call Europe search
        return await self.search_europe()
