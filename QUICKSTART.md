# 🚀 AI Job Hunt Platform - Quick Start Guide

## 📋 What We've Built (Phase 1 Complete!)

### ✅ Completed Features

1. **Comprehensive Blueprint** (BLUEPRINT.md)
   - 170-page detailed plan
   - UI/UX specifications
   - Technical architecture
   - 12-week implementation roadmap
   - Competitive analysis

2. **Stunning Landing Page**
   - Hero section with animated statistics
   - Feature highlights (6 cards)
   - Testimonials from AI professionals
   - Social proof (companies)
   - CTA sections
   - Professional footer
   - Fully responsive (mobile, tablet, desktop)

3. **Backend Foundation**
   - Job scraping agents (LinkedIn, Indeed, Glassdoor, etc.)
   - Switzerland-specific scraper (jobs.ch, ETH, EPFL)
   - Auto-apply engine
   - AI cover letter generator
   - Job matching algorithm
   - Application tracker

### 🎨 Design Highlights

- **Color Scheme**: Purple (#8b5cf6) + Teal (#14b8a6)
- **Effects**: Glass morphism, gradient animations
- **Typography**: Inter font, modern and clean
- **Components**: Card-based, hover effects
- **Responsive**: Mobile-first design

---

## 🏃 Running the Application

### Option 1: Frontend Only (Landing Page)

```bash
# Navigate to frontend directory
cd job-hunt-agent/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Open browser: **http://localhost:3000**

### Option 2: Full Stack (Backend + Frontend)

**Terminal 1 - Backend:**
```bash
cd job-hunt-agent
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Add .env file (see below)
python main.py --mode jobs --region europe
```

**Terminal 2 - Frontend:**
```bash
cd job-hunt-agent/frontend
npm install
npm run dev
```

---

## 🔑 Environment Setup

### Backend (.env)
Create `job-hunt-agent/.env`:

```bash
# AI API Keys (Choose one)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx  # Get from console.groq.com
# OR
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx

# Email Notifications (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your.email@gmail.com
SMTP_PASSWORD=your_app_password

# Database (SQLite by default - no setup needed!)
DATABASE_URL=sqlite:///data/jobs.db
```

### Frontend (.env.local)
Create `job-hunt-agent/frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📂 Project Structure

```
job-hunt-agent/
├── BLUEPRINT.md                 # 170-page comprehensive plan ⭐
├── QUICKSTART.md               # This file
├── README.md                   # Main README
├── main.py                     # Backend entry point
├── requirements.txt            # Python dependencies
│
├── agents/                     # Job scraping & auto-apply
│   ├── job_scraper.py         # Multi-platform scraper
│   ├── switzerland_scraper.py # Swiss jobs & internships
│   ├── auto_apply.py          # Auto-application engine
│   └── cover_letter_gen.py    # AI cover letter generator
│
├── utils/                      # Utilities
│   ├── matching.py            # Job matching algorithm
│   ├── tracker.py             # Application tracking
│   └── notifications.py       # Email notifications
│
├── config/                     # Configuration
│   └── profile.yaml           # Your job preferences
│
└── frontend/                   # Next.js web app ⭐
    ├── app/
    │   ├── page.tsx           # Landing page (LIVE!)
    │   ├── layout.tsx         # Root layout
    │   └── globals.css        # Global styles
    ├── package.json
    └── tailwind.config.ts     # Design system
```

---

## 🎯 What to Do Next

### Immediate (Test What's Built):

1. **View Landing Page:**
   ```bash
   cd frontend && npm install && npm run dev
   ```
   Open: http://localhost:3000

2. **Configure Your Profile:**
   Edit `config/profile.yaml` with your info

3. **Get Groq API Key** (FREE):
   - Visit: https://console.groq.com
   - Create account
   - Generate API key
   - Add to `.env`

### Phase 2 (Next 2 Weeks):

1. **CV Builder**
   - 5 templates (Swiss, German, futuristic)
   - Drag-and-drop editor
   - AI bullet generation
   - PDF export

2. **Job Search UI**
   - Browse curated AI/ML jobs
   - Filters (location, salary, remote)
   - Job detail pages
   - Save jobs

3. **Application Tracker**
   - Kanban board (Saved → Applied → Interview → Offer)
   - Notes and follow-ups
   - Timeline view

---

## 🌐 URLs & Links

### Live Application (Local):
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### GitHub Repository:
https://github.com/MAYANK12-WQ/job-hunt-agent

### Documentation:
- Blueprint: `BLUEPRINT.md` (170 pages!)
- README: `README.md`
- API Keys Guide: `API_KEYS_GUIDE.md` (from research-agent-pro)

---

## 🐛 Troubleshooting

### Frontend won't start:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend Python errors:
```bash
# Make sure you're in virtual environment
venv\Scripts\activate

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Port already in use:
- Frontend (3000): Kill existing process or use `npm run dev -- -p 3001`
- Backend (8000): Change port in `main.py`

---

## 📊 Current Statistics

**Lines of Code:**
- Frontend: ~500 lines (landing page, config)
- Backend: ~2,100 lines (agents, utils, scraping)
- Total: ~2,600 lines

**Features Built:**
- ✅ Landing page with hero section
- ✅ Job scraping (10+ platforms)
- ✅ AI cover letter generation
- ✅ Job matching algorithm
- ✅ Application tracking (database)
- ⏳ CV builder (coming Phase 2)
- ⏳ Dashboard (coming Phase 2)
- ⏳ Auto-apply UI (coming Phase 2)

**Deployment Ready:**
- Frontend: Vercel (1-click deploy)
- Backend: Railway, Render, or Fly.io
- Database: SQLite (local) or Supabase (cloud)

---

## 🎨 Preview Screenshots

### Landing Page:
- Hero section with animated stats (15,483 jobs, 1,234 offers, €95k avg)
- Feature cards (6 key features)
- Mock dashboard preview (glass morphism)
- Testimonials from AI professionals
- CTA sections

### Colors:
- **Primary Purple**: #8b5cf6 (buttons, accents)
- **Accent Teal**: #14b8a6 (success, highlights)
- **Gradients**: Purple → Teal (hero, CTAs)
- **Background**: White → Light purple/teal mesh

---

## 💡 Tips for Success

1. **Start with Landing Page**: Test the design and feel
2. **Configure Profile**: Add your real preferences
3. **Get Free API Keys**: Groq is generous (14k requests/day)
4. **Test Job Scraping**: Run backend to see jobs found
5. **Read Blueprint**: 170 pages of detailed planning!

---

## 📞 Need Help?

**GitHub Issues:**
https://github.com/MAYANK12-WQ/job-hunt-agent/issues

**Documentation:**
- BLUEPRINT.md - Full specifications
- README.md - Project overview
- This file - Quick start

---

## 🚀 Next Phase Preview

**Phase 2 (Weeks 3-4): CV Builder**
- Country-specific templates
- Futuristic designs
- AI-powered bullet points
- Real-time preview
- PDF/DOCX export

**Phase 3 (Weeks 5-6): Job Search**
- AI/ML job database
- Smart filters
- Semantic search
- Job detail pages

**Phase 4 (Weeks 7-8): Dashboard**
- Application tracker
- Analytics charts
- Email notifications
- Profile settings

**Phase 5 (Weeks 9-10): Auto-Apply**
- Automated applications
- Cover letter generation
- Rate limiting
- Error handling

**Phase 6 (Weeks 11-12): Polish & Launch**
- Mobile optimization
- Performance tuning
- Stripe integration
- Public launch

---

<p align="center">
  <strong>🎉 Phase 1 Complete! Ready to build Phase 2?</strong>
  <br>
  Made with 💙 for AI job seekers everywhere
</p>
