'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowRight, Briefcase, FileText, Target, Zap, Globe, Shield, TrendingUp, Users, CheckCircle2, Star } from 'lucide-react';

export default function LandingPage() {
  const [stats, setStats] = useState({
    jobsApplied: 0,
    offersReceived: 0,
    avgSalary: 0,
  });

  // Animate stats on load
  useEffect(() => {
    const targets = {
      jobsApplied: 15483,
      offersReceived: 1234,
      avgSalary: 95,
    };

    const duration = 2000; // 2 seconds
    const steps = 60;
    const interval = duration / steps;

    let step = 0;
    const timer = setInterval(() => {
      step++;
      const progress = step / steps;

      setStats({
        jobsApplied: Math.floor(targets.jobsApplied * progress),
        offersReceived: Math.floor(targets.offersReceived * progress),
        avgSalary: Math.floor(targets.avgSalary * progress),
      });

      if (step >= steps) {
        clearInterval(timer);
        setStats(targets);
      }
    }, interval);

    return () => clearInterval(timer);
  }, []);

  const features = [
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Auto-Apply to 100+ Jobs",
      description: "Our AI agent applies to relevant jobs while you sleep. Save 20+ hours/week.",
    },
    {
      icon: <FileText className="w-6 h-6" />,
      title: "AI-Optimized Resumes",
      description: "Country-specific templates for Switzerland, Germany, and Europe. ATS-friendly.",
    },
    {
      icon: <Target className="w-6 h-6" />,
      title: "Smart Matching",
      description: "Semantic search finds perfect-fit roles. 95%+ match accuracy.",
    },
    {
      icon: <Globe className="w-6 h-6" />,
      title: "Europe & Switzerland Focus",
      description: "Specialized for AI/ML/Gen AI roles in European tech hubs.",
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: "Privacy-First",
      description: "GDPR compliant. Your data stays local. No selling to recruiters.",
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: "Salary Insights",
      description: "Know your worth. Benchmark data for AI/ML roles across Europe.",
    },
  ];

  const companies = [
    "Google", "Meta", "DeepMind", "OpenAI", "Anthropic", "Mistral AI",
    "ETH Zurich", "EPFL", "Siemens", "SAP"
  ];

  const testimonials = [
    {
      name: "Sarah M.",
      role: "ML Engineer at Google Zurich",
      text: "Applied to 147 jobs in 2 weeks, got 12 interviews, landed my dream role. This platform is a game-changer!",
      rating: 5,
    },
    {
      name: "David L.",
      role: "AI Researcher at ETH Zurich",
      text: "The research-focused CV template helped me highlight my publications perfectly. Got offers from 3 universities!",
      rating: 5,
    },
    {
      name: "Maria K.",
      role: "Data Scientist at DeepMind",
      text: "Auto-apply saved me so much time. The AI cover letters were surprisingly good - better than mine!",
      rating: 5,
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-accent-50">
      {/* Navbar */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-lg border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <Briefcase className="w-8 h-8 text-primary-600" />
              <span className="text-xl font-bold bg-gradient-to-r from-primary-600 to-accent-600 bg-clip-text text-transparent">
                AI Job Hunt
              </span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <Link href="#features" className="text-gray-600 hover:text-primary-600 transition">
                Features
              </Link>
              <Link href="#pricing" className="text-gray-600 hover:text-primary-600 transition">
                Pricing
              </Link>
              <Link href="#testimonials" className="text-gray-600 hover:text-primary-600 transition">
                Testimonials
              </Link>
              <Link href="/dashboard" className="px-4 py-2 text-primary-600 hover:bg-primary-50 rounded-lg transition">
                Sign In
              </Link>
              <Link
                href="/dashboard"
                className="px-6 py-2 bg-gradient-to-r from-primary-600 to-accent-600 text-white rounded-lg hover:shadow-lg transform hover:-translate-y-0.5 transition"
              >
                Get Started Free
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Column - Content */}
            <div className="space-y-8">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary-100 rounded-full">
                <Star className="w-4 h-4 text-primary-600" />
                <span className="text-sm font-medium text-primary-700">
                  4.9/5 from 1,247 AI Professionals
                </span>
              </div>

              <h1 className="text-5xl md:text-6xl font-bold leading-tight">
                Land Your Dream
                <span className="block bg-gradient-to-r from-primary-600 to-accent-600 bg-clip-text text-transparent">
                  AI Job
                </span>
                While You Sleep 😴
              </h1>

              <p className="text-xl text-gray-600 leading-relaxed">
                AI-powered job search & auto-apply for <strong>ML Engineers</strong>, <strong>Data Scientists</strong>, and <strong>AI Researchers</strong> in Europe & Switzerland.
              </p>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  href="/dashboard"
                  className="group px-8 py-4 bg-gradient-to-r from-primary-600 to-accent-600 text-white rounded-xl font-semibold text-lg hover:shadow-2xl transform hover:-translate-y-1 transition flex items-center justify-center gap-2"
                >
                  Get Started Free
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition" />
                </Link>
                <Link
                  href="#demo"
                  className="px-8 py-4 border-2 border-primary-300 text-primary-700 rounded-xl font-semibold text-lg hover:bg-primary-50 transition flex items-center justify-center gap-2"
                >
                  Watch Demo (2 min)
                </Link>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-6 pt-8 border-t border-gray-200">
                <div>
                  <div className="text-3xl font-bold text-primary-600">
                    {stats.jobsApplied.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-600">Jobs Applied</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-primary-600">
                    {stats.offersReceived.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-600">Offers Received</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-primary-600">
                    €{stats.avgSalary}k
                  </div>
                  <div className="text-sm text-gray-600">Avg Salary</div>
                </div>
              </div>

              {/* Social Proof */}
              <div className="pt-4">
                <p className="text-sm text-gray-600 mb-3">Our users landed jobs at:</p>
                <div className="flex flex-wrap gap-6 items-center">
                  {companies.slice(0, 6).map((company, index) => (
                    <div key={index} className="text-gray-400 font-semibold text-sm">
                      {company}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Right Column - Visual */}
            <div className="relative">
              <div className="relative glass rounded-2xl p-8 shadow-2xl">
                <div className="absolute top-4 right-4 px-3 py-1 bg-green-500 text-white text-xs font-semibold rounded-full">
                  ● Live
                </div>

                {/* Mock Dashboard Preview */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between pb-4 border-b">
                    <h3 className="font-semibold text-gray-800">Today's Activity</h3>
                    <span className="text-sm text-gray-500">Jan 19, 2025</span>
                  </div>

                  {/* Mock job application cards */}
                  {[
                    { company: "Google", role: "ML Engineer", match: 95, status: "Applied" },
                    { company: "DeepMind", role: "AI Researcher", match: 92, status: "Interview" },
                    { company: "ETH Zurich", role: "Postdoc AI", match: 88, status: "Offer" },
                  ].map((job, index) => (
                    <div key={index} className="flex items-center gap-4 p-4 bg-white rounded-lg shadow-sm border border-gray-100">
                      <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                        <Briefcase className="w-6 h-6 text-primary-600" />
                      </div>
                      <div className="flex-1">
                        <div className="font-semibold text-gray-800">{job.role}</div>
                        <div className="text-sm text-gray-500">{job.company}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-semibold text-primary-600">{job.match}% match</div>
                        <div className="text-xs text-gray-500">{job.status}</div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Floating stats */}
                <div className="absolute -bottom-6 -left-6 px-4 py-3 bg-white rounded-xl shadow-lg border border-primary-100">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-sm font-semibold">12 applications today</span>
                  </div>
                </div>
              </div>

              {/* Decorative elements */}
              <div className="absolute -z-10 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-gradient-to-r from-primary-200 to-accent-200 rounded-full blur-3xl opacity-20"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Why AI Job Hunt?</h2>
            <p className="text-xl text-gray-600">
              The most powerful job search automation platform for AI/ML professionals
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group p-6 rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-lg transition cursor-pointer"
              >
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600 group-hover:bg-primary-600 group-hover:text-white transition mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-primary-50 to-accent-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Loved by AI Professionals</h2>
            <p className="text-xl text-gray-600">
              Join 1,247+ successful job seekers
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="p-6 bg-white rounded-xl shadow-lg">
                <div className="flex gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                  ))}
                </div>
                <p className="text-gray-700 mb-4">{testimonial.text}</p>
                <div className="border-t pt-4">
                  <div className="font-semibold">{testimonial.name}</div>
                  <div className="text-sm text-gray-600">{testimonial.role}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary-600 to-accent-600">
        <div className="max-w-4xl mx-auto text-center text-white">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Land Your Dream Job?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Join 1,247+ AI professionals who've automated their job search
          </p>
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white text-primary-600 rounded-xl font-semibold text-lg hover:shadow-2xl transform hover:-translate-y-1 transition"
          >
            Get Started Free
            <ArrowRight className="w-5 h-5" />
          </Link>
          <p className="mt-4 text-sm opacity-75">
            ✓ No credit card required  ✓ Setup in 5 minutes  ✓ Cancel anytime
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 sm:px-6 lg:px-8 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Briefcase className="w-6 h-6" />
                <span className="font-bold">AI Job Hunt</span>
              </div>
              <p className="text-gray-400 text-sm">
                AI-powered job search for ML professionals in Europe & Switzerland
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link href="#features" className="hover:text-white transition">Features</Link></li>
                <li><Link href="#pricing" className="hover:text-white transition">Pricing</Link></li>
                <li><Link href="/dashboard" className="hover:text-white transition">Dashboard</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link href="/about" className="hover:text-white transition">About</Link></li>
                <li><Link href="/blog" className="hover:text-white transition">Blog</Link></li>
                <li><Link href="/contact" className="hover:text-white transition">Contact</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link href="/privacy" className="hover:text-white transition">Privacy Policy</Link></li>
                <li><Link href="/terms" className="hover:text-white transition">Terms of Service</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-gray-400 text-sm">
            © 2025 AI Job Hunt. Made with 💙 for job seekers everywhere.
          </div>
        </div>
      </footer>
    </div>
  );
}
