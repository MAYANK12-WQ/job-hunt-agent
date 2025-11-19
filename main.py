#!/usr/bin/env python3
"""
Job Hunt Agent - Main Entry Point
Automatically searches for jobs in Europe and internships in Switzerland
"""

import argparse
import asyncio
import sys
from pathlib import Path
from datetime import datetime
import yaml
from dotenv import load_dotenv
import colorama
from colorama import Fore, Style

# Initialize colorama for colored terminal output
colorama.init(autoreset=True)

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from agents.job_scraper import JobScraper
from agents.switzerland_scraper import SwitzerlandScraper
from agents.auto_apply import AutoApplyAgent
from utils.tracker import ApplicationTracker
from utils.notifications import NotificationManager
from utils.matching import JobMatcher

# Load environment variables
load_dotenv()


class JobHuntAgent:
    """Main Job Hunt Agent orchestrator"""

    def __init__(self, config_path: str = "config/profile.yaml"):
        """Initialize the job hunt agent"""
        print(f"{Fore.CYAN}🤖 Initializing Job Hunt Agent...{Style.RESET_ALL}\n")

        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Initialize components
        self.job_scraper = JobScraper(self.config)
        self.switzerland_scraper = SwitzerlandScraper(self.config)
        self.auto_apply = AutoApplyAgent(self.config)
        self.tracker = ApplicationTracker()
        self.notifications = NotificationManager(self.config)
        self.matcher = JobMatcher(self.config)

        print(f"{Fore.GREEN}✓ Job Hunt Agent initialized successfully!{Style.RESET_ALL}\n")

    async def search_jobs(self, region: str = "europe", mode: str = "jobs"):
        """
        Search for jobs based on region and mode

        Args:
            region: "europe", "switzerland", or "worldwide"
            mode: "jobs" or "internships"
        """
        print(f"{Fore.YELLOW}🔍 Searching for {mode} in {region.upper()}...{Style.RESET_ALL}\n")

        jobs = []

        if region == "switzerland" or mode == "internships":
            # Use Switzerland-specific scraper
            jobs = await self.switzerland_scraper.search(mode=mode)
        elif region == "europe":
            # Use general European job scraper
            jobs = await self.job_scraper.search_europe()
        else:
            # Worldwide search
            jobs = await self.job_scraper.search_worldwide()

        print(f"{Fore.GREEN}✓ Found {len(jobs)} {mode}{Style.RESET_ALL}\n")
        return jobs

    async def match_jobs(self, jobs: list):
        """
        Match jobs against user profile and assign scores

        Returns:
            dict: {
                "high": list of jobs with ≥80% match,
                "medium": list of jobs with 60-79% match,
                "low": list of jobs with <60% match
            }
        """
        print(f"{Fore.YELLOW}🎯 Matching jobs to your profile...{Style.RESET_ALL}\n")

        matched_jobs = {
            "high": [],
            "medium": [],
            "low": []
        }

        for job in jobs:
            score = self.matcher.calculate_match_score(job)
            job['match_score'] = score

            if score >= 80:
                matched_jobs["high"].append(job)
            elif score >= 60:
                matched_jobs["medium"].append(job)
            else:
                matched_jobs["low"].append(job)

        # Sort by match score
        for category in matched_jobs:
            matched_jobs[category].sort(key=lambda x: x['match_score'], reverse=True)

        print(f"{Fore.GREEN}✓ {len(matched_jobs['high'])} high-match jobs (≥80%){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}✓ {len(matched_jobs['medium'])} medium-match jobs (60-79%){Style.RESET_ALL}")
        print(f"{Fore.RED}✓ {len(matched_jobs['low'])} low-match jobs (<60%){Style.RESET_ALL}\n")

        return matched_jobs

    async def auto_apply_to_jobs(self, jobs: list, match_threshold: int = 75):
        """
        Automatically apply to jobs that meet the match threshold

        Args:
            jobs: List of jobs to apply to
            match_threshold: Minimum match score to apply (default: 75)
        """
        eligible_jobs = [
            job for job in jobs
            if job.get('match_score', 0) >= match_threshold
        ]

        if not eligible_jobs:
            print(f"{Fore.YELLOW}⚠ No jobs meet the match threshold of {match_threshold}%{Style.RESET_ALL}\n")
            return

        print(f"{Fore.CYAN}🤖 Auto-applying to {len(eligible_jobs)} jobs...{Style.RESET_ALL}\n")

        results = {
            "success": 0,
            "failed": 0,
            "skipped": 0
        }

        for job in eligible_jobs:
            try:
                result = await self.auto_apply.apply(job)

                if result["status"] == "success":
                    results["success"] += 1
                    self.tracker.log_application(job, status="applied")
                    print(f"{Fore.GREEN}✓ Applied to \"{job['title']}\" at {job['company']} ({job['match_score']}% match){Style.RESET_ALL}")
                elif result["status"] == "skipped":
                    results["skipped"] += 1
                    print(f"{Fore.YELLOW}⊘ Skipped \"{job['title']}\" at {job['company']} - {result['reason']}{Style.RESET_ALL}")
                else:
                    results["failed"] += 1
                    print(f"{Fore.RED}✗ Failed to apply to \"{job['title']}\" at {job['company']} - {result['error']}{Style.RESET_ALL}")

            except Exception as e:
                results["failed"] += 1
                print(f"{Fore.RED}✗ Error applying to \"{job['title']}\": {str(e)}{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}📊 Application Summary:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  ✓ Successful: {results['success']}{Style.RESET_ALL}")
        print(f"{Fore.RED}  ✗ Failed: {results['failed']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  ⊘ Skipped: {results['skipped']}{Style.RESET_ALL}\n")

        return results

    async def run(self, mode: str = "jobs", region: str = "europe", auto_apply: bool = False, match_threshold: int = 75):
        """
        Run the complete job hunt process

        Args:
            mode: "jobs" or "internships"
            region: "europe", "switzerland", or "worldwide"
            auto_apply: Whether to automatically apply to matched jobs
            match_threshold: Minimum match score for auto-apply
        """
        start_time = datetime.now()

        try:
            # Step 1: Search for jobs
            jobs = await self.search_jobs(region=region, mode=mode)

            if not jobs:
                print(f"{Fore.RED}No jobs found. Try adjusting your search criteria.{Style.RESET_ALL}\n")
                return

            # Step 2: Match jobs to profile
            matched_jobs = await self.match_jobs(jobs)

            # Step 3: Save results
            self.tracker.save_jobs(matched_jobs)

            # Step 4: Auto-apply if enabled
            if auto_apply:
                all_jobs = matched_jobs["high"] + matched_jobs["medium"] + matched_jobs["low"]
                await self.auto_apply_to_jobs(all_jobs, match_threshold=match_threshold)

            # Step 5: Send notifications
            await self.notifications.send_daily_digest(matched_jobs)
            print(f"{Fore.GREEN}📧 Sending daily digest email...{Style.RESET_ALL}")

            # Calculate duration
            duration = datetime.now() - start_time
            print(f"\n{Fore.GREEN}✅ Job hunt agent completed successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}⏱️  Duration: {duration.seconds} seconds{Style.RESET_ALL}\n")

        except Exception as e:
            print(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")
            raise


def main():
    """Main entry point with CLI arguments"""
    parser = argparse.ArgumentParser(
        description="🎯 Job Hunt Agent - AI-powered job search and auto-apply"
    )

    parser.add_argument(
        "--mode",
        choices=["jobs", "internships"],
        default="jobs",
        help="Search mode: jobs or internships (default: jobs)"
    )

    parser.add_argument(
        "--region",
        choices=["europe", "switzerland", "worldwide"],
        default="europe",
        help="Search region (default: europe)"
    )

    parser.add_argument(
        "--auto-apply",
        action="store_true",
        help="Automatically apply to matched jobs"
    )

    parser.add_argument(
        "--match-threshold",
        type=int,
        default=75,
        help="Minimum match score for auto-apply (default: 75)"
    )

    parser.add_argument(
        "--config",
        default="config/profile.yaml",
        help="Path to profile configuration file"
    )

    args = parser.parse_args()

    # Print welcome banner
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{'='*60}")
    print(f"       🎯 JOB HUNT AGENT - AI JOB SEARCH & AUTO-APPLY")
    print(f"{'='*60}")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}Mode: {args.mode.upper()}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Region: {args.region.upper()}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Auto-Apply: {'ENABLED' if args.auto_apply else 'DISABLED'}{Style.RESET_ALL}")
    if args.auto_apply:
        print(f"{Fore.YELLOW}Match Threshold: {args.match_threshold}%{Style.RESET_ALL}")
    print()

    # Initialize and run agent
    agent = JobHuntAgent(config_path=args.config)

    # Run async main function
    asyncio.run(
        agent.run(
            mode=args.mode,
            region=args.region,
            auto_apply=args.auto_apply,
            match_threshold=args.match_threshold
        )
    )


if __name__ == "__main__":
    main()
