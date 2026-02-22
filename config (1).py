# config.py
# Configuration for Website Change Monitor

import os

# Email Configuration (Gmail example)
# For Gmail: Use "App Password" not your regular password
# Generate at: https://myaccount.google.com/apppasswords
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',  # Your Gmail address
    'sender_password': 'your-app-password',   # Gmail App Password (not regular password!)
    'recipient_email': 'notify-me@gmail.com' # Where to send alerts
}

# Alternative Email Providers
# Uncomment and modify for your provider:

# OUTLOOK/HOTMAIL
# EMAIL_CONFIG = {
#     'smtp_server': 'smtp-mail.outlook.com',
#     'smtp_port': 587,
#     'sender_email': 'your-email@outlook.com',
#     'sender_password': 'your-password',
#     'recipient_email': 'notify-me@outlook.com'
# }

# YAHOO
# EMAIL_CONFIG = {
#     'smtp_server': 'smtp.mail.yahoo.com',
#     'smtp_port': 587,
#     'sender_email': 'your-email@yahoo.com',
#     'sender_password': 'your-app-password',
#     'recipient_email': 'notify-me@yahoo.com'
# }

# Monitor Settings
MONITOR_CONFIG = {
    'check_interval_minutes': 60,  # How often to check (in minutes)
    'timeout_seconds': 30,         # HTTP request timeout
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'retry_attempts': 3,           # Number of retries on failure
    'retry_delay_seconds': 10,     # Delay between retries
}

# Notification Settings
NOTIFICATION_CONFIG = {
    'send_on_first_check': False,  # Send email on first run
    'send_on_error': True,         # Send email when site is down
    'include_diff': True,          # Include what changed in email
    'max_diff_length': 500,        # Max characters of diff to show
}

# Storage
CACHE_DIR = 'cache'
SITES_FILE = 'monitored_sites.json'
LOG_FILE = 'monitor.log'

# Create cache directory if it doesn't exist
os.makedirs(CACHE_DIR, exist_ok=True)

# Ignore Patterns (for filtering out dynamic content)
# Common elements that change but aren't important
IGNORE_PATTERNS = [
    'timestamp',
    'current-time',
    'last-updated',
    'ad-container',
    'advertisement',
    'cookie-banner',
    'session-id',
    'csrf-token',
    'random-id',
]

# CSS Selectors to Monitor (optional - monitor specific parts only)
# Example: Only monitor main content, ignore sidebar/footer
# MONITOR_SELECTORS = [
#     'main',
#     '#content',
#     '.article-body',
# ]
MONITOR_SELECTORS = None  # None = monitor entire page
