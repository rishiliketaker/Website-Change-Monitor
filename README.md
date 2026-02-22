# 🔍 Website Change Monitor

Monitor websites for changes and get instant email notifications. Perfect for tracking price changes, product availability, news updates, and more!

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install requests beautifulsoup4 schedule
```

### 2. Configure Email

Open `config.py` and add your email settings:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',
    'sender_password': 'your-app-password',  # NOT your regular password!
    'recipient_email': 'notify-me@gmail.com'
}
```

**For Gmail:** You MUST use an "App Password", not your regular password.
1. Go to https://myaccount.google.com/apppasswords
2. Create an app password for "Mail"
3. Use that 16-character password in config.py

### 3. Run
```bash
python monitor.py
```

## ✨ Features

### Core Features
✅ **Monitor multiple websites** - Track unlimited sites  
✅ **Email notifications** - Instant alerts on changes  
✅ **Change detection** - Smart content hashing  
✅ **Diff reports** - See exactly what changed  
✅ **Scheduled checks** - Automatic hourly monitoring  
✅ **Error handling** - Retry on failures, notify on errors  
✅ **Selective monitoring** - Monitor specific page sections  

### Advanced Features
✅ **Ignore dynamic content** - Filter timestamps, ads, etc.  
✅ **Custom intervals** - Different check frequencies per site  
✅ **First-run baseline** - Save initial state  
✅ **Status tracking** - See last checked/changed times  
✅ **Logging** - Track all checks and changes  
✅ **User-agent spoofing** - Avoid bot detection  

## 📋 Usage

### Add a Website
```bash
python monitor.py
> 1 (Add website)
> URL: https://example.com/product
> Name: Product Page
> Monitor specific section: n
✅ Added!
```

### Start Monitoring
```bash
python monitor.py
> 5 (Start monitoring)
🚀 Checking every 60 minutes...
```

### Check Immediately
```bash
python monitor.py
> 4 (Check all sites now)
🔍 Checking 3 site(s)...
```

## 🎯 Common Use Cases

### 1. Price Tracking
```
Monitor: https://amazon.com/product/B08XYZ
Notify when: Price changes
Use for: Waiting for deals
```

### 2. Product Availability
```
Monitor: https://store.com/sold-out-item
Notify when: "Out of Stock" → "In Stock"
Use for: Grabbing limited items
```

### 3. News Updates
```
Monitor: https://news.com/breaking
Notify when: New articles appear
Use for: Breaking news alerts
```

### 4. Job Postings
```
Monitor: https://company.com/careers
Notify when: New job listings
Use for: Career opportunities
```

### 5. Course Registration
```
Monitor: https://university.edu/courses
Notify when: Course opens up
Use for: Getting into full classes
```

### 6. Stock Availability
```
Monitor: https://store.com/ps5
Notify when: "Sold Out" disappears
Use for: Buying limited stock items
```

## 🔧 Advanced Configuration

### Monitor Specific Section

Instead of the whole page, monitor just one part:

```python
# Example: Monitor only the price section
URL: https://amazon.com/product/B08XYZ
Selector: .price-section

# Example: Monitor main content only
URL: https://news.com/article
Selector: #main-content

# Example: Monitor availability status
URL: https://store.com/product
Selector: .stock-status
```

**CSS Selector Examples:**
- `#price` - Element with id="price"
- `.product-info` - Elements with class="product-info"
- `main` - The <main> element
- `.price-container .current-price` - Nested elements

### Custom Check Intervals

Different sites can have different check frequencies:

```python
# In config.py
MONITOR_CONFIG = {
    'check_interval_minutes': 60,  # Default: every hour
}

# Or per-site when adding:
monitor.add_site(
    url='https://high-priority-site.com',
    check_interval=15  # Check every 15 minutes
)
```

### Ignore Dynamic Content

Some pages have timestamps, ads, or random IDs that change constantly:

```python
# In config.py
IGNORE_PATTERNS = [
    'timestamp',
    'current-time',
    'advertisement',
    'ad-container',
    'session-id',
]
```

This filters out these elements before comparing.

## 📧 Email Setup Guide

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication**
   - Go to https://myaccount.google.com/security
   - Turn on 2-Step Verification

2. **Create App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password
   - Use this in `config.py`

3. **Update config.py**
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'youremail@gmail.com',
    'sender_password': 'abcd efgh ijkl mnop',  # App password
    'recipient_email': 'youremail@gmail.com'
}
```

### Outlook/Hotmail Setup

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp-mail.outlook.com',
    'smtp_port': 587,
    'sender_email': 'youremail@outlook.com',
    'sender_password': 'your-password',
    'recipient_email': 'youremail@outlook.com'
}
```

### Yahoo Setup

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.mail.yahoo.com',
    'smtp_port': 587,
    'sender_email': 'youremail@yahoo.com',
    'sender_password': 'your-app-password',  # Yahoo also needs app password
    'recipient_email': 'youremail@yahoo.com'
}
```

## 📊 Example Workflows

### Workflow 1: Monitor Product Price

```bash
# 1. Add site
python monitor.py
> 1 (Add website)
> URL: https://amazon.com/product/B08XYZ
> Name: Headphones
> Selector: .price-section

# 2. Test immediately
> 4 (Check now)
✅ Baseline saved

# 3. Start monitoring
> 5 (Start monitoring)
🚀 Checking every 60 minutes

# 4. Wait for change
# When price changes, you get email:
# "🔔 Website Changed: Headphones"
```

### Workflow 2: Track Multiple Sites

```bash
# Add multiple sites
1. Tech news: https://techcrunch.com
2. Job board: https://company.com/careers
3. Course page: https://university.edu/CS101

# Start monitoring all at once
> 5 (Start monitoring)

# You'll get email whenever ANY of them change
```

### Workflow 3: Monitor Every 15 Minutes

For high-priority sites that update frequently:

```python
# In monitor.py, when adding:
monitor.add_site(
    url='https://high-priority.com',
    name='Important Site',
    check_interval=15  # Minutes
)
```

## 🎨 Email Notifications

### What You Receive

**Subject:**
```
🔔 Website Changed: Product Name
```

**Body:**
```
Website Change Detected!

Site: Headphones on Amazon
URL: https://amazon.com/product/B08XYZ
Time: 2026-02-18 14:30:00

Previous Check: 2026-02-18 13:30:00
Current Check: 2026-02-18 14:30:00

Status: Content has changed

Changes Detected:
==================================================
REMOVED: $129.99
ADDED: $99.99
REMOVED: Only 2 left in stock
ADDED: In Stock
==================================================

---
Website Change Monitor
```

### Customizing Notifications

In `config.py`:

```python
NOTIFICATION_CONFIG = {
    'send_on_first_check': False,  # Don't email on first run
    'send_on_error': True,         # Email if site is down
    'include_diff': True,          # Show what changed
    'max_diff_length': 500,        # Limit diff size
}
```

## 🛠️ Troubleshooting

### "Email authentication failed"

**Problem:** Wrong email password

**Solution:**
- Gmail: Use App Password, not regular password
- Yahoo: Use App Password
- Outlook: Regular password should work

### "No changes detected" but page looks different

**Problem:** Monitoring dynamic content (ads, timestamps)

**Solution:**
Use a CSS selector to monitor specific content:
```python
selector = '#main-content'  # Monitor only main content
```

### "SSL Certificate Error"

**Problem:** SSL verification issue

**Solution:**
Add to `monitor.py`:
```python
response = self.session.get(url, verify=False)
```

### "Connection timeout"

**Problem:** Slow website or network

**Solution:**
Increase timeout in `config.py`:
```python
MONITOR_CONFIG = {
    'timeout_seconds': 60,  # Increased from 30
}
```

### Site blocking the monitor

**Problem:** Website detects automated access

**Solution:**
1. Use better user agent (already in config)
2. Add delays between checks
3. Monitor specific sections (less data = less suspicious)

## 💡 Pro Tips

### Tip 1: Test First
```bash
# Always test email before leaving it running
python monitor.py
> 6 (Test email)
✅ Check your inbox!
```

### Tip 2: Start with Manual Check
```bash
# Before starting scheduler, do manual check first
> 4 (Check now)
# This creates baseline
# Then start scheduler
> 5 (Start monitoring)
```

### Tip 3: Use Specific Selectors

Don't monitor the whole page if you care about one thing:

```python
# Bad: Monitors entire page (ads, menus, footer, etc.)
selector = None

# Good: Monitors only what matters
selector = '.product-price'
```

### Tip 4: Run in Background

**Linux/Mac:**
```bash
nohup python monitor.py &
```

**Windows:**
Use Task Scheduler or run in separate terminal

### Tip 5: Monitor the Log

```bash
# Check what's happening
tail -f monitor.log
```

## 📁 File Structure

```
website-monitor/
├── monitor.py              # Main script
├── config.py               # Your configuration
├── monitored_sites.json    # List of monitored sites
├── monitor.log            # Activity log
└── cache/                 # Cached website snapshots
    ├── abc123.json
    ├── def456.json
    └── ...
```

## 🔐 Privacy & Security

**Your data:**
- Stored locally in `cache/` folder
- No external services used
- Email credentials in config.py (keep safe!)

**Best practices:**
- Don't commit config.py to GitHub
- Use app passwords, not regular passwords
- Keep cache/ folder secure (may contain sensitive data)

