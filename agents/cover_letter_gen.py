"""
Cover Letter Generator - Uses AI to generate personalized cover letters
"""

import os
from typing import Dict
from groq import Groq
from openai import OpenAI


class CoverLetterGenerator:
    """Generate personalized cover letters using AI"""

    def __init__(self, config: dict):
        self.config = config
        self.profile = config['profile']

        # Initialize AI client (prioritize Groq for free tier)
        if os.getenv('GROQ_API_KEY'):
            self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
            self.model = "llama-3.3-70b-versatile"
            self.provider = "groq"
        elif os.getenv('OPENAI_API_KEY'):
            self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            self.model = "gpt-4-turbo-preview"
            self.provider = "openai"
        else:
            raise ValueError("No AI API key found. Please set GROQ_API_KEY or OPENAI_API_KEY")

    async def generate(self, job: Dict) -> str:
        """
        Generate a personalized cover letter for a specific job

        Args:
            job: Job dictionary with title, company, description, etc.

        Returns:
            str: Personalized cover letter
        """

        prompt = self._build_prompt(job)

        try:
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content

            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating cover letter: {str(e)}")
            return self._fallback_cover_letter(job)

    def _build_prompt(self, job: Dict) -> str:
        """Build the prompt for AI cover letter generation"""

        skills_str = ", ".join([lang['name'] for lang in self.profile['skills']['programming_languages']])
        frameworks_str = ", ".join(self.profile['skills']['frameworks'])

        prompt = f"""Generate a professional cover letter for the following job application:

Job Title: {job['title']}
Company: {job['company']}
Location: {job['location']}
Job Description: {job.get('description', 'Not provided')}

Candidate Information:
- Name: {self.profile['name']}
- Experience: {self.profile['experience_years']} years
- Skills: {skills_str}
- Frameworks: {frameworks_str}
- Education: {self.profile['education'][0]['degree']} from {self.profile['education'][0]['university']}

Requirements:
1. Keep it concise (250-300 words)
2. Highlight relevant skills that match the job
3. Show genuine interest in the company
4. Professional but personable tone
5. Include specific examples if possible
6. End with a call to action

Format as a proper cover letter with:
- Opening paragraph (why you're excited about this role)
- Middle paragraph (your relevant experience and skills)
- Closing paragraph (next steps and thank you)

Do NOT include placeholders like [Your Name] or [Date]. Generate a complete, ready-to-send cover letter."""

        return prompt

    def _fallback_cover_letter(self, job: Dict) -> str:
        """Generate a fallback cover letter if AI fails"""

        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job['title']} position at {job['company']}. With {self.profile['experience_years']} years of experience in software engineering and a passion for building innovative solutions, I am excited about the opportunity to contribute to your team.

Throughout my career, I have developed expertise in {', '.join(self.profile['job_preferences']['keywords'][:3])}, which aligns perfectly with the requirements of this role. My experience at {self.profile['education'][0]['university']} and subsequent professional work has equipped me with both the technical skills and collaborative mindset needed to excel in this position.

I am particularly drawn to {job['company']} because of its reputation for innovation and excellence. The {job['location']} location is ideal for me, and I am eager to bring my skills and enthusiasm to your team.

I would welcome the opportunity to discuss how my background and skills would benefit {job['company']}. Thank you for considering my application.

Sincerely,
{self.profile['name']}
"""
