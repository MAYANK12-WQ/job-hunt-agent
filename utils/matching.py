"""
Job Matching Algorithm - Calculates match score between profile and job
"""

from typing import Dict


class JobMatcher:
    """Matches jobs to user profile"""

    def __init__(self, config: dict):
        self.config = config
        self.profile = config['profile']
        self.prefs = self.profile['job_preferences']

    def calculate_match_score(self, job: Dict) -> int:
        """
        Calculate match score (0-100) for a job

        Scoring criteria:
        - Skills match: 40%
        - Experience level: 30%
        - Location: 15%
        - Salary: 10%
        - Company: 5%
        """

        scores = {
            'skills': self._score_skills(job),
            'experience': self._score_experience(job),
            'location': self._score_location(job),
            'salary': self._score_salary(job),
            'company': self._score_company(job)
        }

        weights = {
            'skills': 0.40,
            'experience': 0.30,
            'location': 0.15,
            'salary': 0.10,
            'company': 0.05
        }

        total_score = sum(scores[key] * weights[key] for key in scores)

        return int(total_score)

    def _score_skills(self, job: Dict) -> int:
        """Score based on skills match (0-100)"""
        job_title = job.get('title', '').lower()
        job_desc = job.get('description', '').lower()

        # Get user's keywords
        keywords = [kw.lower() for kw in self.prefs.get('keywords', [])]

        # Count matches
        matches = sum(1 for kw in keywords if kw in job_title or kw in job_desc)

        if not keywords:
            return 50  # Neutral score if no keywords

        return min(100, int((matches / len(keywords)) * 100))

    def _score_experience(self, job: Dict) -> int:
        """Score based on experience level match (0-100)"""
        job_title = job.get('title', '').lower()
        user_level = self.prefs.get('experience_level', 'Mid-Level').lower()

        # Simple heuristic
        if 'senior' in job_title and 'senior' in user_level:
            return 100
        elif 'junior' in job_title and 'entry' in user_level:
            return 100
        elif ('mid' in user_level or 'intermediate' in user_level) and \
             'senior' not in job_title and 'junior' not in job_title:
            return 100
        else:
            return 60  # Partial match

    def _score_location(self, job: Dict) -> int:
        """Score based on location preference (0-100)"""
        job_location = job.get('location', '').lower()

        preferred_cities = [city.lower() for city in self.profile['location']['preferred_cities']]
        preferred_countries = [country.lower() for country in self.profile['location']['preferred_countries']]

        # Check if remote
        if job.get('remote', False) and 'remote' in self.prefs.get('work_arrangement', []):
            return 100

        # Check preferred cities
        if any(city in job_location for city in preferred_cities):
            return 100

        # Check preferred countries
        if any(country in job_location for country in preferred_countries):
            return 75

        return 30  # Location not preferred

    def _score_salary(self, job: Dict) -> int:
        """Score based on salary range (0-100)"""
        job_salary = job.get('salary', None)

        if not job_salary:
            return 50  # Neutral if not specified

        # This is a simplified version - would need better salary parsing
        return 50

    def _score_company(self, job: Dict) -> int:
        """Score based on company reputation (0-100)"""
        # This would integrate with company review APIs
        # For now, return neutral score
        return 50
