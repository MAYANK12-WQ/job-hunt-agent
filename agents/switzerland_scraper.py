"""
Switzerland Scraper - Specialized scraper for Swiss jobs and internships
Focuses on jobs.ch, JobScout24, ETH/EPFL boards, and Swiss startups
"""

import asyncio
import requests
from datetime import datetime
from typing import List, Dict
from selenium import webdriver
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time


class SwitzerlandScraper:
    """Specialized scraper for Switzerland jobs and internships"""

    def __init__(self, config: dict):
        self.config = config
        self.profile = config['profile']
        self.internship_prefs = self.profile.get('internship_preferences', {})

    async def search(self, mode: str = "jobs") -> List[Dict]:
        """
        Search for jobs or internships in Switzerland

        Args:
            mode: "jobs" or "internships"
        """
        print(f"🇨🇭 Searching Swiss {mode}...")

        if mode == "internships":
            return await self._search_internships()
        else:
            return await self._search_jobs()

    async def _search_jobs(self) -> List[Dict]:
        """Search for full-time jobs in Switzerland"""
        tasks = [
            self.scrape_jobs_ch(),
            self.scrape_jobscout24(),
            self.scrape_swissdevjobs(),
            self.scrape_linkedin_switzerland(),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)

        return self._remove_duplicates(all_jobs)

    async def _search_internships(self) -> List[Dict]:
        """Search for internships in Switzerland"""
        tasks = [
            self.scrape_eth_zurich_internships(),
            self.scrape_epfl_internships(),
            self.scrape_uzh_internships(),
            self.scrape_jobs_ch_internships(),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_internships = []
        for result in results:
            if isinstance(result, list):
                all_internships.extend(result)

        return self._remove_duplicates(all_internships)

    async def scrape_jobs_ch(self) -> List[Dict]:
        """Scrape jobs from jobs.ch (largest Swiss job board)"""
        print("  → Searching jobs.ch...")
        jobs = []

        try:
            titles = self.profile['job_preferences']['titles']
            cities = self.profile['location']['preferred_cities']

            for title in titles[:2]:
                for city in [c for c in cities if c in ['Zurich', 'Geneva', 'Basel', 'Lausanne']][:2]:
                    url = f"https://www.jobs.ch/en/vacancies/?term={title.replace(' ', '+')}&location={city}"

                    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                    soup = BeautifulSoup(response.content, 'html.parser')

                    job_cards = soup.find_all('div', class_='job-item')

                    for card in job_cards[:10]:
                        job = self._parse_jobs_ch_card(card)
                        if job:
                            jobs.append(job)

                    await asyncio.sleep(2)

            print(f"  ✓ Found {len(jobs)} jobs on jobs.ch")

        except Exception as e:
            print(f"  ✗ Error scraping jobs.ch: {str(e)}")

        return jobs

    async def scrape_jobscout24(self) -> List[Dict]:
        """Scrape jobs from JobScout24 Switzerland"""
        print("  → Searching JobScout24...")
        # Implementation similar to jobs.ch
        return []

    async def scrape_swissdevjobs(self) -> List[Dict]:
        """Scrape tech jobs from SwissDevJobs.ch"""
        print("  → Searching SwissDevJobs...")
        # SwissDevJobs is great for tech positions in Switzerland
        return []

    async def scrape_linkedin_switzerland(self) -> List[Dict]:
        """Scrape LinkedIn jobs specifically in Switzerland"""
        print("  → Searching LinkedIn Switzerland...")
        # Similar to main scraper but Switzerland-focused
        return []

    async def scrape_eth_zurich_internships(self) -> List[Dict]:
        """Scrape internships from ETH Zurich career portal"""
        print("  → Searching ETH Zurich internships...")
        internships = []

        try:
            url = "https://www.eth-gethired.ch/en/jobs/?category=internship"

            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.content, 'html.parser')

            job_cards = soup.find_all('div', class_='job-listing')

            for card in job_cards:
                internship = {
                    'title': card.find('h3').text.strip() if card.find('h3') else '',
                    'company': 'ETH Zurich',
                    'location': 'Zurich, Switzerland',
                    'url': 'https://www.eth-gethired.ch' + card.find('a')['href'] if card.find('a') else '',
                    'source': 'ETH Zurich',
                    'type': 'Internship',
                    'date_posted': datetime.now().isoformat(),
                }
                if internship['title']:
                    internships.append(internship)

            print(f"  ✓ Found {len(internships)} internships at ETH Zurich")

        except Exception as e:
            print(f"  ✗ Error scraping ETH Zurich: {str(e)}")

        return internships

    async def scrape_epfl_internships(self) -> List[Dict]:
        """Scrape internships from EPFL career services"""
        print("  → Searching EPFL internships...")
        # EPFL (École polytechnique fédérale de Lausanne)
        return []

    async def scrape_uzh_internships(self) -> List[Dict]:
        """Scrape internships from University of Zurich"""
        print("  → Searching UZH internships...")
        return []

    async def scrape_jobs_ch_internships(self) -> List[Dict]:
        """Scrape internships from jobs.ch"""
        print("  → Searching jobs.ch internships...")
        # Filter jobs.ch specifically for internships
        return []

    def _parse_jobs_ch_card(self, card) -> Dict:
        """Parse jobs.ch job card"""
        try:
            title = card.find('h2').text.strip() if card.find('h2') else ''
            company = card.find('span', class_='company').text.strip() if card.find('span', class_='company') else ''
            location = card.find('span', class_='location').text.strip() if card.find('span', class_='location') else ''

            link = card.find('a')
            url = f"https://www.jobs.ch{link['href']}" if link else ''

            if title and company:
                return {
                    'title': title,
                    'company': company,
                    'location': location,
                    'url': url,
                    'source': 'jobs.ch',
                    'country': 'Switzerland',
                    'date_posted': datetime.now().isoformat(),
                }

        except Exception as e:
            return None

        return None

    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs"""
        seen = set()
        unique = []

        for job in jobs:
            key = (job.get('title', '').lower(), job.get('company', '').lower())
            if key not in seen:
                seen.add(key)
                unique.append(job)

        return unique
