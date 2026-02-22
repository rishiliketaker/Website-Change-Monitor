# 🚀 Setup Guide - Website Monitor

Complete step-by-step guide to get your monitor running in 10 minutes.

## ⏱️ 10-Minute Setup

### Step 1: Install Python Packages (2 minutes)

Open terminal/command prompt:

```bash
pip install requests beautifulsoup4 schedule
```

**What gets installed:**
- `requests` - For fetching web pages
- `beautifulsoup4` - For parsing HTML
- `schedule` - For running tasks on a schedule

---

### Step 2: Get Gmail App Password (3 minutes)

**Why you need this:**
Gmail doesn't let apps use your regular password for security. You need a special "App Password".

**Steps:**

1. **Go to your Google Account**
   - Visit: https://myaccount.google.com

2. **Enable 2-Factor Authentication** (if not already on)
   - Click "Security" on the left
   - Scroll to "2-Step Verification"
   - Turn it on

3. **Create App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - You might need to sign in again
   - Select "Mail" from dropdown
   - Select "Other" and name it "Website Monitor"
   - Click "Generate"

4. **Copy the password**
   - You'll see a 16-character password like: `abcd efgh ijkl mnop`
   - Copy this (you'll need it in next step)
   - Click "Done"

**Can't find App Passwords?**
- Make sure 2-Factor Authentication is on first
- Try this direct link: https://security.google.com/settings/security/apppasswords

---

### Step 3: Configure Email (2 minutes)

Open `config.py` and update these lines:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-actual-email@gmail.com',      # ← Change this
    'sender_password': 'abcd efgh ijkl mnop',            # ← Paste app password
    'recipient_email': 'your-actual-email@gmail.com'    # ← Where to receive alerts
}
```

**Example:**
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'john.doe@gmail.com',
    'sender_password': 'vmky azer tyui qwer',
    'recipient_email': 'john.doe@gmail.com'
}
```

**Save the file!**

---

### Step 4: Test Email (1 minute)

Run the monitor:
```bash
python monitor.py
```

Menu appears:
```
1. Add website to monitor
2. Remove website
3. List monitored websites
4. Check all sites now
5. Start monitoring (scheduled)
6. Test email notification
7. Exit

Select option (1-7): 6
```

Type `6` and press Enter.

**You should see:**
```
📧 Testing email...
✅ Test email sent!
```

**Check your email!** You should receive a test email.

**If it failed:**
- Check your email/password in config.py
- Make sure you used App Password, not regular password
- Try with Outlook/Yahoo if Gmail doesn't work

---

### Step 5: Add Your First Website (2 minutes)

Let's monitor a real website!

**Example: Monitor TechCrunch for new articles**

```bash
python monitor.py
> 1  # Add website

Enter URL: https://techcrunch.com
Enter name (or press Enter to use URL): TechCrunch
Monitor specific section? (y/n): n

✅ Added: TechCrunch
```

**Example: Monitor Amazon product price**

```bash
python monitor.py
> 1  # Add website

Enter URL: https://www.amazon.com/dp/B08XYZ123
Enter name: Headphones
Monitor specific section? (y/n): y
Enter CSS selector: .price-section

✅ Added: Headphones
   Monitoring: .price-section
```

---

### Step 6: Run Your First Check (1 minute)

```bash
python monitor.py
> 4  # Check all sites now
```

You'll see:
```
🔍 Checking: TechCrunch
   URL: https://techcrunch.com
   📝 First check - baseline saved
   ✅ No email sent (first run)
```

**This creates the baseline.** Next time it checks, it will compare against this.

---

### Step 7: Start Monitoring! (Done!)

```bash
python monitor.py
> 5  # Start monitoring

🚀 Website Monitor Started
⏰ Checking every 60 minutes
📧 Notifications: your-email@gmail.com
📝 Monitoring 1 site(s)

Press Ctrl+C to stop
```

**That's it!** Your monitor is now running.

It will:
1. Check your websites every hour
2. Email you when something changes
3. Keep running until you stop it (Ctrl+C)

---

## 🎯 Quick Examples

### Example 1: Monitor Product Availability

**Goal:** Get notified when PS5 is back in stock

```bash
URL: https://www.target.com/p/playstation-5-console/-/A-81114595
Name: PS5 Target
Selector: .availability-status

When "Out of Stock" changes → You get email!
```

---

### Example 2: Monitor Job Postings

**Goal:** Know when company posts new jobs

```bash
URL: https://careers.google.com/jobs
Name: Google Careers
Selector: .job-listings

When new job appears → You get email!
```

---

### Example 3: Monitor News Headlines

**Goal:** Get breaking news alerts

```bash
URL: https://www.bbc.com/news
Name: BBC News
Selector: .top-stories

When headlines change → You get email!
```

---

## 🔧 Customization

### Change Check Interval

By default, checks every 60 minutes.

**To change:**

Open `config.py`:
```python
MONITOR_CONFIG = {
    'check_interval_minutes': 30,  # Check every 30 minutes
}
```

**Options:**
- `15` - Every 15 minutes (aggressive)
- `30` - Every 30 minutes (frequent)
- `60` - Every hour (default)
- `120` - Every 2 hours (relaxed)
- `360` - Every 6 hours (daily checks)

---

### Monitor Multiple Sites

Just add more!

```bash
python monitor.py

# Add site 1
> 1
URL: https://site1.com
Name: Site 1

# Add site 2
> 1
URL: https://site2.com
Name: Site 2

# Add site 3
> 1
URL: https://site3.com
Name: Site 3

# Start monitoring all 3
> 5
```

They'll all be checked every hour!

---

### See What's Being Monitored

```bash
python monitor.py
> 3  # List monitored websites
```

Output:
```
📋 MONITORED SITES
==================================================

1. ✅ TechCrunch
   URL: https://techcrunch.com
   Status: ok
   Last checked: 2026-02-18 14:30:00
   Last changed: Never

2. ✅ Amazon Headphones
   URL: https://amazon.com/dp/B08XYZ
   Status: ok
   Last checked: 2026-02-18 14:30:00
   Last changed: 2026-02-18 10:15:00
   Monitoring: .price-section
```

---

### Remove a Site

```bash
python monitor.py
> 2  # Remove website

Enter URL to remove: https://site.com
✅ Removed: https://site.com
```

---

## 🐛 Common Issues

### Issue 1: "Email authentication failed"

**Problem:** Wrong password or not using app password

**Solution:**
1. Make sure you're using Gmail App Password
2. Not your regular Gmail password
3. Check for typos in config.py
4. Make sure 2FA is enabled on your Google account

---

### Issue 2: "No module named 'requests'"

**Problem:** Didn't install dependencies

**Solution:**
```bash
pip install requests beautifulsoup4 schedule
```

---

### Issue 3: Email works but no change detected

**Problem:** Website hasn't changed yet

**Solution:**
- It's working! Just wait for a change.
- To test: Manually check a site that changes often (like news sites)
- Or add a test site and check it twice in a row

---

### Issue 4: Getting too many emails

**Problem:** Site changes constantly (ads, timestamps, etc.)

**Solution:**
Monitor specific section instead of whole page:
```bash
Monitor specific section? (y/n): y
Enter CSS selector: #main-content
```

This ignores ads, sidebars, footers.

---

### Issue 5: "Connection timeout"

**Problem:** Website is slow or blocked

**Solution:**
In `config.py`, increase timeout:
```python
MONITOR_CONFIG = {
    'timeout_seconds': 60,  # Increased from 30
}
```

---

## 💡 Tips

### Tip 1: Test with News Sites

News sites change frequently - perfect for testing!

```bash
URL: https://news.ycombinator.com
Name: Hacker News

Wait 30 minutes, run check → Should detect changes!
```

---

### Tip 2: Use Meaningful Names

```bash
# Bad
Name: Site 1

# Good
Name: iPhone Price - Amazon
```

Makes emails easier to understand!

---

### Tip 3: Start Small

```bash
# Don't add 20 sites immediately
# Start with 2-3 to test

1. A news site (changes often - good for testing)
2. A product page (your actual use case)
3. Maybe one more

# Once working, add more!
```

---

### Tip 4: Keep Terminal Open

When running the monitor:
```bash
python monitor.py
> 5 (Start monitoring)

# Keep this terminal window open!
# Don't close it or the monitor stops.
```

**To run in background (advanced):**

Linux/Mac:
```bash
nohup python monitor.py > monitor.out &
```

Windows:
Use Task Scheduler

---

### Tip 5: Check the Log

The monitor logs everything:

```bash
cat monitor.log
```

Or on Windows:
```bash
type monitor.log
```

See all checks, changes, errors!

---

## ✅ Checklist

Before you start monitoring:

- [ ] Python packages installed (`requests`, `beautifulsoup4`, `schedule`)
- [ ] Gmail App Password created
- [ ] Email configured in `config.py`
- [ ] Test email sent successfully
- [ ] At least one website added
- [ ] First baseline check completed
- [ ] Monitor started (option 5)
- [ ] Terminal window left open

**All checked?** You're monitoring! 🎉

---

## 🎓 Next Steps

Now that it's working:

1. **Add more sites** - Monitor everything you care about
2. **Tune intervals** - Different times for different sites
3. **Use selectors** - Monitor specific sections
4. **Let it run** - Leave it running 24/7
5. **Enjoy alerts** - Get notified instantly!

---

**Questions?** Check README.md for full documentation!

Your monitor is now watching the web for you! 🚀
