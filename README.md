# 🎯 Job Hunt Agent

> **AI-Powered Job Search & Auto-Apply Agent for Europe & Switzerland**
>
> Automatically searches for jobs across Europe and internships in Switzerland, then applies on your behalf using AI.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Features

### 🔍 **Smart Job Search**
- **Europe-wide Job Search**: Searches across major European job boards
  - LinkedIn Jobs (all European countries)
  - Indeed Europe
  - Glassdoor Europe
  - EuroJobs
  - EURES (European Job Mobility Portal)
  - Monster Europe
  - StepStone

- **Switzerland Internship Focus**: Specialized search for Swiss internships
  - jobs.ch
  - JobScout24 Switzerland
  - SwissDevJobs
  - ETH Zurich job board
  - EPFL career services
  - Swiss startup job boards

### 🤖 **AI-Powered Auto-Apply**
- Intelligent resume customization per job
- Cover letter generation tailored to each position
- Form auto-fill using AI
- Application tracking
- Follow-up email scheduling

### 📊 **Advanced Features**
- **Job Matching Score**: AI calculates fit percentage
- **Salary Insights**: Estimates based on role and location
- **Application Status Dashboard**: Track all applications
- **Daily Email Digest**: Summary of new opportunities
- **Smart Filters**: Location, salary, visa sponsorship, remote options

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Chrome/Chromium browser
- API Keys (all have free tiers)

### 1. Clone the Repository
```bash
git clone https://github.com/MAYANK12-WQ/job-hunt-agent.git
cd job-hunt-agent
```

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configure Your Profile
Edit `config/profile.yaml`:
```yaml
profile:
  name: "Your Name"
  email: "your.email@example.com"
  phone: "+41 XX XXX XX XX"

  location:
    preferred_countries:
      - "Switzerland"
      - "Germany"
      - "Netherlands"
    preferred_cities:
      - "Zurich"
      - "Geneva"
      - "Basel"

  job_preferences:
    titles:
      - "Software Engineer"
      - "Data Scientist"
      - "Product Manager"
    experience_level: "Mid-Level"  # Entry-Level, Mid-Level, Senior
    work_arrangement: ["Remote", "Hybrid", "On-site"]
    visa_sponsorship_required: true

  resume_path: "./documents/resume.pdf"
  cover_letter_template: "./documents/cover_letter_template.txt"
```

### 4. Add API Keys
Create `.env` file:
```bash
# AI for cover letter generation
OPENAI_API_KEY=your_openai_key_here
# OR
GROQ_API_KEY=your_groq_key_here  # Free tier: 14,400 requests/day

# Job Search APIs (optional but recommended)
LINKEDIN_EMAIL=your_email
LINKEDIN_PASSWORD=your_password
```

### 5. Run the Agent
```bash
# Start job search
python main.py

# Switzerland internships only
python main.py --mode internships --country switzerland

# Europe-wide job search
python main.py --mode jobs --region europe

# Auto-apply to matched jobs
python main.py --auto-apply --match-threshold 75
```

---

## 📁 Project Structure

```
job-hunt-agent/
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
│
├── config/
│   ├── profile.yaml           # Your job preferences
│   └── job_boards.yaml        # Job board configurations
│
├── agents/
│   ├── job_scraper.py         # Job search engine
│   ├── switzerland_scraper.py # Switzerland-specific scraper
│   ├── auto_apply.py          # Auto-application engine
│   └── cover_letter_gen.py    # AI cover letter generator
│
├── utils/
│   ├── browser.py             # Browser automation (Selenium)
│   ├── matching.py            # Job matching algorithm
│   ├── tracker.py             # Application tracking
│   └── notifications.py       # Email notifications
│
├── documents/
│   ├── resume.pdf             # Your resume
│   └── cover_letter_template.txt
│
└── data/
    ├── jobs.db                # SQLite database for jobs
    └── applications.db        # Track your applications
```

---

## 🎯 How It Works

### 1. Job Discovery
```python
# The agent searches multiple platforms
Europe Jobs → LinkedIn, Indeed, Glassdoor, EuroJobs, EURES
Switzerland → jobs.ch, JobScout24, ETH/EPFL boards
```

### 2. AI Matching
```python
# Each job is scored based on:
- Skills match (40%)
- Experience level (30%)
- Location preference (15%)
- Salary range (10%)
- Company rating (5%)
```

### 3. Auto-Apply Process
```python
# For jobs with ≥75% match:
1. Generate custom cover letter using AI
2. Fill application form automatically
3. Attach resume and cover letter
4. Submit application
5. Log to database
6. Set up follow-up reminders
```

---

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Web Scraping**: Selenium, BeautifulSoup4, Scrapy
- **AI**: OpenAI GPT-4 / Groq Llama 3.3
- **Database**: SQLite (for local tracking)
- **Job APIs**: LinkedIn API, Indeed API, Custom scrapers
- **Automation**: Selenium WebDriver
- **Notifications**: SMTP, Telegram Bot

---

## 📊 Example Output

```bash
🔍 Searching for jobs...
✓ Found 45 jobs in Switzerland
✓ Found 123 jobs in Europe

🎯 Matching jobs to your profile...
✓ 12 high-match jobs (≥80%)
✓ 28 medium-match jobs (60-79%)
✓ 128 low-match jobs (<60%)

🤖 Auto-applying to high-match jobs...
✓ Applied to "Senior Software Engineer" at Google Zurich (95% match)
✓ Applied to "Data Scientist" at ETH Zurich (92% match)
✓ Applied to "ML Engineer" at Siemens Munich (88% match)
...

📧 Sending daily digest email...
✓ Email sent to your.email@example.com

✅ Job hunt agent completed successfully!
```

---

## 🔐 Privacy & Ethics

### Data Privacy
- All data stored locally in SQLite database
- No data shared with third parties
- Resume/cover letter encrypted at rest
- API keys stored securely in `.env`

### Responsible Auto-Apply
- Only applies to jobs matching your criteria (>75% match)
- Respects rate limits (max 10 applications/day)
- Includes genuine cover letters (not spam)
- Honors "do not apply again" flags

---

## 📈 Roadmap

### Phase 1: Core Features ✅
- [x] Project setup
- [ ] Multi-platform job scraping
- [ ] Switzerland internship search
- [ ] AI cover letter generation
- [ ] Basic auto-apply

### Phase 2: Intelligence
- [ ] Advanced matching algorithm
- [ ] Salary prediction model
- [ ] Company research integration
- [ ] Interview preparation agent

### Phase 3: Scale
- [ ] Web dashboard
- [ ] Mobile app
- [ ] Multi-user support
- [ ] Job alert system

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 📧 Contact

**Mayank** - AI Engineer & Creator

- GitHub: [@MAYANK12-WQ](https://github.com/MAYANK12-WQ)
- Project: [https://github.com/MAYANK12-WQ/job-hunt-agent](https://github.com/MAYANK12-WQ/job-hunt-agent)

---

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please:
- Respect job board Terms of Service
- Don't spam applications
- Review each application before submission
- Use responsibly and ethically

---

<p align="center">
  <strong>Happy Job Hunting! 🎯</strong>
  <br>
  Made with 💙 for job seekers everywhere
</p>
