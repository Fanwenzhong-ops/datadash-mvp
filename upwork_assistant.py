"""
Upwork Job Assistant — 自动搜工作 + 生成定制 Proposal
用法: python upwork_assistant.py
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from datetime import datetime

# Add stealth-browser scripts to path
SKILL_DIR = Path.home() / ".workbuddy" / "skills" / "skill_2053082740118388736"
SESSION_DIR = Path.home() / ".clawdbot" / "browser-sessions"
SESSION_DIR.mkdir(parents=True, exist_ok=True)

UPWORK_PROFILE = "Fanwenzhong-ops"
DEMO_URL = "https://9d3a10e4fbf34d52b55590d0f6e97950.app.codebuddy.work"
GITHUB_URL = f"https://github.com/{UPWORK_PROFILE}/datadash-mvp"

# ============================================================
# Step 1: Open Upwork in visible browser for login
# ============================================================

def open_upwork_login():
    """Open Upwork in visible Chrome so user can log in"""
    try:
        from DrissionPage import ChromiumPage, ChromiumOptions
        
        print("\n🔧 Starting Chrome with stealth profile...")
        
        co = ChromiumOptions()
        co.set_argument('--disable-blink-features=AutomationControlled')
        co.set_argument('--no-first-run')
        co.set_argument('--no-default-browser-check')
        
        # Use a dedicated automation profile
        profile_dir = str(Path.home() / ".upwork-automation-profile")
        co.set_argument(f'--user-data-dir={profile_dir}')
        
        page = ChromiumPage(co)
        page.get("https://www.upwork.com/")
        
        print("\n✅ Chrome opened. Please log into your Upwork account.")
        print("   After logged in, press Enter here to continue...")
        input()
        
        # Save session
        cookies = page.cookies()
        session_file = SESSION_DIR / "upwork.json"
        session_file.write_text(json.dumps({
            "cookies": cookies,
            "saved_at": datetime.now().isoformat(),
            "url": page.url
        }, indent=2))
        
        print(f"✅ Session saved to {session_file}")
        print("\n📋 Now let's search for jobs. Keep the browser open...")
        
        return page
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure DrissionPage is installed:")
        print("   pip install DrissionPage")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


# ============================================================
# Step 2: Search for jobs
# ============================================================

SEARCH_QUERIES = [
    {
        "name": "Data Visualization Dashboard",
        "url": "https://www.upwork.com/nx/jobs/search/?q=data+visualization+dashboard+chart&sort=recency&duration=3&t=0&nbs=1"
    },
    {
        "name": "API Integration Frontend",
        "url": "https://www.upwork.com/nx/jobs/search/?q=API+integration+frontend+React&sort=recency&t=0&nbs=1"
    },
    {
        "name": "Crypto/Finance Dashboard",
        "url": "https://www.upwork.com/nx/jobs/search/?q=crypto+finance+dashboard+real-time&sort=recency&t=0&nbs=1"
    },
    {
        "name": "Chart.js / D3.js Projects",
        "url": "https://www.upwork.com/nx/jobs/search/?q=Chart.js+D3.js+data+visualization&sort=recency&t=0&nbs=1"
    },
    {
        "name": "Admin Panel Dashboard",
        "url": "https://www.upwork.com/nx/jobs/search/?q=admin+panel+dashboard+analytics&sort=recency&t=0&nbs=1"
    },
]

def search_jobs(page):
    """Search Upwork for matching jobs"""
    results = []
    
    for query in SEARCH_QUERIES:
        print(f"\n🔍 Searching: {query['name']}...")
        
        try:
            page.get(query['url'])
            time.sleep(3)
            
            # Try to extract job listings
            # Upwork renders jobs dynamically, wait for them
            page.wait.ele_displayed("section[data-test='JobsList']", timeout=10)
            time.sleep(2)
            
            # Extract job cards
            job_cards = page.eles("css:article.job-tile, section[data-ev-label='search_results'] article")
            
            if not job_cards:
                # Try alternative selectors
                job_cards = page.eles("css:[data-test='job-tile-list'] > div, .job-tile")
            
            for card in job_cards[:10]:  # Limit to top 10
                try:
                    title_el = card.ele("css:a[data-test='job-tile-title-link'], h2 a, .job-title a")
                    title = title_el.text.strip() if title_el else "N/A"
                    link = title_el.attr("href") if title_el else ""
                    
                    # Budget / type
                    budget_el = card.ele("css:[data-test='job-type'], .job-type, li[data-test='job-type-label']")
                    budget = budget_el.text.strip() if budget_el else "N/A"
                    
                    # Description snippet
                    desc_el = card.ele("css:[data-test='job-description-text'], .job-description, p.description")
                    desc = desc_el.text.strip()[:200] if desc_el else ""
                    
                    # Client info
                    client_el = card.ele("css:[data-test='client-country'], .client-location")
                    client = client_el.text.strip() if client_el else ""
                    
                    results.append({
                        "query": query['name'],
                        "title": title,
                        "url": f"https://www.upwork.com{link}" if link and not link.startswith("http") else link,
                        "budget": budget,
                        "description": desc,
                        "client": client,
                    })
                except Exception:
                    continue
                    
            print(f"   Found {len(job_cards)} listings")
            
        except Exception as e:
            print(f"   ⚠️ Search failed: {e}")
            continue
    
    return results


# ============================================================
# Step 3: Generate proposal for a selected job
# ============================================================

def generate_proposal(job):
    """Generate a custom proposal for a given job"""
    
    title = job.get("title", "")
    desc = job.get("description", "")
    budget = job.get("budget", "")
    
    # Extract key skills from job description
    skills = []
    if re.search(r'react|next\.?js', desc + title, re.I): skills.append("React")
    if re.search(r'chart\.?js|chartjs', desc + title, re.I): skills.append("Chart.js")
    if re.search(r'd3\.?js', desc + title, re.I): skills.append("D3.js")
    if re.search(r'api|rest', desc + title, re.I): skills.append("API integration")
    if re.search(r'dashboard', desc + title, re.I): skills.append("dashboard")
    if re.search(r'crypto|bitcoin|ethereum', desc + title, re.I): skills.append("crypto data")
    if re.search(r'postgres|mysql|sql', desc + title, re.I): skills.append("database")
    if re.search(r'python|django|flask', desc + title, re.I): skills.append("Python")
    
    skill_str = ", ".join(skills[:3]) if skills else "data visualization"
    
    # Build first line hook
    hooks = []
    if "dashboard" in title.lower():
        hooks.append(f"I noticed you're looking to build a dashboard")
    elif "api" in title.lower():
        hooks.append(f"I have extensive experience building and integrating data APIs")
    elif "visualization" in title.lower() or "chart" in title.lower():
        hooks.append(f"Your data visualization project caught my eye")
    else:
        hooks.append(f"I took a close look at your project requirements")
    
    if "real-time" in (desc + title).lower():
        hooks.append("with real-time data capabilities")
    if "crypto" in (desc + title).lower() or "finance" in (desc + title).lower():
        hooks.append("in the finance/crypto space")
    
    hook = " ".join(hooks) + "."
    
    # Full proposal
    proposal = f"""Hi,

{hook}

I recently built DataDash — a real-time cryptocurrency market dashboard that fetches live data from REST APIs and renders interactive Chart.js charts. It includes market analytics, searchable coin explorer, and auto-refreshing data. You can see it here:
📊 Live Demo: {DEMO_URL}
📂 GitHub: {GITHUB_URL}

My relevant experience for your project includes {skill_str}. I would approach this by:
1. First understanding your data sources and key metrics you want to display
2. Designing a clean, responsive interface that makes complex data intuitive
3. Implementing with a focus on performance and maintainability

One quick question: what's your preferred tech stack for this project?

Would a 15-minute call work to discuss the details? I'm available during US business hours.

Best,
{UPWORK_PROFILE}"""

    return proposal


# ============================================================
# Step 4: Open a specific job and prepare proposal
# ============================================================

def view_job_and_prepare(page, job_url):
    """Open a job posting and prepare a tailored proposal"""
    try:
        page.get(job_url)
        time.sleep(2)
        
        # Try to get full description
        desc_el = page.ele("css:[data-test='job-description'], .job-description-content, .description")
        full_desc = desc_el.text.strip() if desc_el else ""
        
        # Try to get client info
        client_el = page.ele("css:[data-test='client-info'], .client-activity")
        client_info = client_el.text.strip() if client_el else ""
        
        return {
            "url": job_url,
            "full_description": full_desc,
            "client_info": client_info,
        }
    except Exception as e:
        return {"url": job_url, "error": str(e)}


# ============================================================
# Main
# ============================================================

def main():
    print("=" * 60)
    print("  🚀 Upwork Job Assistant — powered by Stealth Browser")
    print("=" * 60)
    
    # Step 1: Open browser for login
    page = open_upwork_login()
    if not page:
        print("\n❌ Could not start browser. Trying alternative method...")
        print("\n📋 Please manually log into Upwork in Chrome, then run:")
        print("   python upwork_assistant.py --search")
        return
    
    # Step 2: Search jobs
    print("\n" + "=" * 60)
    print("  🔍 Searching for matching jobs...")
    print("=" * 60)
    
    jobs = search_jobs(page)
    
    if not jobs:
        print("\n⚠️ No jobs found. Try these manual searches in your Upwork:")
        for q in SEARCH_QUERIES:
            print(f"   • {q['name']}: {q['url']}")
        return
    
    # Step 3: Show results
    print(f"\n✅ Found {len(jobs)} potential jobs:\n")
    for i, job in enumerate(jobs, 1):
        print(f"──────────────────────────────────────────────")
        print(f"  [{i}] {job['title']}")
        print(f"  💰 {job['budget']}  |  📍 {job['client']}")
        print(f"  📝 {job['description'][:150]}...")
        print(f"  🔗 {job['url']}")
    
    # Step 4: Let user pick
    print("\n" + "=" * 60)
    print("  Enter job number to generate a proposal (or 'q' to quit)")
    print("=" * 60)
    
    while True:
        choice = input("\n👉 Job number: ").strip()
        if choice.lower() == 'q':
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(jobs):
                job = jobs[idx]
                print(f"\n📋 Viewing: {job['title']}")
                
                # Get full details
                details = view_job_and_prepare(page, job['url'])
                if details.get('full_description'):
                    print(f"\n📄 Full Description:\n{details['full_description'][:500]}")
                    print(f"\n👤 Client Info: {details.get('client_info', 'N/A')}")
                
                # Generate proposal
                job['description'] = details.get('full_description', job['description'])
                proposal = generate_proposal(job)
                
                print("\n" + "=" * 60)
                print("  ✍️  Your Custom Proposal:")
                print("=" * 60)
                print(proposal)
                print("=" * 60)
                
                print("\n📋 Copy this proposal, paste it into Upwork, and submit!")
                print("   (Pro tip: Always customize the first 2 sentences for each job)")
                
        except ValueError:
            print("❌ Please enter a valid number")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Good luck with your proposals!")
    page.quit()


if __name__ == "__main__":
    main()
