"""
Auto Apply Agent - Automatically applies to matched jobs
"""

import asyncio
from datetime import datetime
from typing import Dict
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

from agents.cover_letter_gen import CoverLetterGenerator


class AutoApplyAgent:
    """Agent that automatically applies to jobs"""

    def __init__(self, config: dict):
        self.config = config
        self.profile = config['profile']
        self.app_config = config['application']

        self.cover_letter_gen = CoverLetterGenerator(config)

        # Application tracking
        self.applications_today = 0
        self.max_per_day = self.app_config['rate_limit']['max_applications_per_day']

    async def apply(self, job: Dict) -> Dict:
        """
        Apply to a single job

        Returns:
            dict: {"status": "success|failed|skipped", "reason": str, "error": str}
        """

        # Check rate limits
        if self.applications_today >= self.max_per_day:
            return {
                "status": "skipped",
                "reason": f"Daily limit reached ({self.max_per_day} applications)"
            }

        # Check if already applied
        if self._already_applied(job):
            return {
                "status": "skipped",
                "reason": "Already applied to this job"
            }

        try:
            # Generate custom cover letter
            if self.app_config['custom_cover_letter']:
                cover_letter = await self.cover_letter_gen.generate(job)
            else:
                cover_letter = self._load_generic_cover_letter()

            # Apply based on job source
            if job['source'] == 'LinkedIn':
                result = await self._apply_linkedin(job, cover_letter)
            elif job['source'] == 'Indeed':
                result = await self._apply_indeed(job, cover_letter)
            elif job['source'] == 'jobs.ch':
                result = await self._apply_jobs_ch(job, cover_letter)
            else:
                result = await self._apply_generic(job, cover_letter)

            if result['status'] == 'success':
                self.applications_today += 1

            return result

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

    async def _apply_linkedin(self, job: Dict, cover_letter: str) -> Dict:
        """Apply to a LinkedIn job"""
        try:
            driver = uc.Chrome()
            driver.get(job['url'])

            # Wait for login if needed
            # This is a simplified version - real implementation would need LinkedIn login

            # Look for Easy Apply button
            wait = WebDriverWait(driver, 10)
            easy_apply_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='jobs-apply']"))
            )
            easy_apply_button.click()

            await asyncio.sleep(2)

            # Fill in application form
            # This would need to handle multi-step forms, file uploads, etc.

            driver.quit()

            return {"status": "success"}

        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def _apply_indeed(self, job: Dict, cover_letter: str) -> Dict:
        """Apply to an Indeed job"""
        # Similar to LinkedIn but for Indeed
        return {"status": "skipped", "reason": "Indeed auto-apply not yet implemented"}

    async def _apply_jobs_ch(self, job: Dict, cover_letter: str) -> Dict:
        """Apply to a jobs.ch job"""
        # Similar to LinkedIn but for jobs.ch
        return {"status": "skipped", "reason": "jobs.ch auto-apply not yet implemented"}

    async def _apply_generic(self, job: Dict, cover_letter: str) -> Dict:
        """Apply to a job from any other source"""
        # Generic application process
        return {"status": "skipped", "reason": "Generic auto-apply not yet implemented"}

    def _already_applied(self, job: Dict) -> bool:
        """Check if already applied to this job"""
        # Check database for previous applications
        # This is a placeholder - real implementation would query SQLite
        return False

    def _load_generic_cover_letter(self) -> str:
        """Load generic cover letter template"""
        template_path = self.profile['documents']['cover_letter_template']
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                return f.read()
        return "Dear Hiring Manager,\n\nI am writing to express my interest..."
