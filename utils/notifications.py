"""
Notification Manager - Sends email/telegram notifications
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List


class NotificationManager:
    """Manage notifications for job hunting"""

    def __init__(self, config: dict):
        self.config = config
        self.notification_config = config.get('notifications', {})

    async def send_daily_digest(self, matched_jobs: Dict):
        """Send daily digest email with job matches"""

        if not self.notification_config.get('email', {}).get('daily_digest', False):
            return

        # Build email content
        subject = f"Job Hunt Digest - {len(matched_jobs['high'])} High Matches Found"
        body = self._build_digest_email(matched_jobs)

        # Send email
        await self._send_email(subject, body)

    async def notify_high_match(self, job: Dict):
        """Send immediate notification for high-match job"""

        if not self.notification_config.get('telegram', {}).get('notify_on_high_match', False):
            return

        # Send Telegram notification
        message = f"🎯 High Match Job Found!\n\n{job['title']} at {job['company']}\nMatch Score: {job['match_score']}%\n\n{job['url']}"

        await self._send_telegram(message)

    def _build_digest_email(self, matched_jobs: Dict) -> str:
        """Build HTML email for daily digest"""

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #2c3e50;">Job Hunt Daily Digest</h2>

            <h3 style="color: #27ae60;">High Match Jobs (≥80%)</h3>
            <ul>
        """

        for job in matched_jobs['high'][:10]:
            html += f"""
                <li>
                    <strong>{job['title']}</strong> at {job['company']}<br>
                    Location: {job['location']}<br>
                    Match Score: {job['match_score']}%<br>
                    <a href="{job['url']}">View Job</a>
                </li><br>
            """

        html += """
            </ul>

            <h3 style="color: #f39c12;">Medium Match Jobs (60-79%)</h3>
            <p>Found """ + str(len(matched_jobs['medium'])) + """ medium match jobs.</p>

            <hr>
            <p style="color: #95a5a6; font-size: 12px;">
                This email was sent by Job Hunt Agent. Visit your dashboard to manage applications.
            </p>
        </body>
        </html>
        """

        return html

    async def _send_email(self, subject: str, body: str):
        """Send email via SMTP"""

        try:
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            smtp_email = os.getenv('SMTP_EMAIL')
            smtp_password = os.getenv('SMTP_PASSWORD')

            if not all([smtp_email, smtp_password]):
                print("⚠ Email credentials not configured")
                return

            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = smtp_email
            msg['To'] = self.config['profile']['email']
            msg['Subject'] = subject

            # Attach HTML body
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)

            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_email, smtp_password)
                server.send_message(msg)

            print("✓ Email sent successfully")

        except Exception as e:
            print(f"✗ Error sending email: {str(e)}")

    async def _send_telegram(self, message: str):
        """Send Telegram message"""

        # Telegram bot implementation
        # Would use python-telegram-bot library
        print(f"Telegram: {message}")
