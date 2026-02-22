#!/usr/bin/env python3
"""
Website Change Monitor
Monitor websites for changes and get email notifications
Usage: python monitor.py
"""

import requests
from bs4 import BeautifulSoup
import hashlib
import json
import os
import time
import smtplib
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
import difflib
from config import *


class WebsiteMonitor:
    """Monitor websites for changes and send notifications."""
    
    def __init__(self):
        self.sites = self.load_sites()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': MONITOR_CONFIG['user_agent']})
    
    def load_sites(self):
        """Load monitored sites from JSON file."""
        if os.path.exists(SITES_FILE):
            with open(SITES_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def save_sites(self):
        """Save monitored sites to JSON file."""
        with open(SITES_FILE, 'w') as f:
            json.dump(self.sites, f, indent=2)
    
    def add_site(self, url, name=None, selector=None, check_interval=None):
        """
        Add a website to monitor.
        
        Args:
            url: Website URL to monitor
            name: Friendly name for the site
            selector: CSS selector to monitor (optional)
            check_interval: Custom check interval in minutes (optional)
        """
        site = {
            'url': url,
            'name': name or url,
            'selector': selector,
            'check_interval': check_interval,
            'added': datetime.now().isoformat(),
            'last_checked': None,
            'last_changed': None,
            'status': 'pending',
            'error_count': 0
        }
        
        self.sites.append(site)
        self.save_sites()
        
        print(f"✅ Added: {site['name']}")
        print(f"   URL: {url}")
        if selector:
            print(f"   Monitoring: {selector}")
        
        return site
    
    def remove_site(self, url):
        """Remove a website from monitoring."""
        self.sites = [s for s in self.sites if s['url'] != url]
        self.save_sites()
        
        # Remove cache file
        cache_file = self.get_cache_path(url)
        if os.path.exists(cache_file):
            os.remove(cache_file)
        
        print(f"✅ Removed: {url}")
    
    def get_cache_path(self, url):
        """Get cache file path for a URL."""
        # Create safe filename from URL
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(CACHE_DIR, f"{url_hash}.json")
    
    def fetch_content(self, url, selector=None):
        """
        Fetch and parse webpage content.
        
        Args:
            url: URL to fetch
            selector: CSS selector to extract specific content
            
        Returns:
            dict with content, hash, and metadata
        """
        try:
            response = self.session.get(
                url,
                timeout=MONITOR_CONFIG['timeout_seconds']
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style tags
            for tag in soup(['script', 'style', 'noscript']):
                tag.decompose()
            
            # Remove elements matching ignore patterns
            for pattern in IGNORE_PATTERNS:
                for element in soup.find_all(class_=lambda x: x and pattern in x.lower()):
                    element.decompose()
                for element in soup.find_all(id=lambda x: x and pattern in x.lower()):
                    element.decompose()
            
            # Extract specific content if selector provided
            if selector:
                content_elements = soup.select(selector)
                if content_elements:
                    content = '\n'.join([elem.get_text(strip=True) for elem in content_elements])
                else:
                    content = ""
            elif MONITOR_SELECTORS:
                # Use global selectors from config
                content_elements = []
                for sel in MONITOR_SELECTORS:
                    content_elements.extend(soup.select(sel))
                content = '\n'.join([elem.get_text(strip=True) for elem in content_elements])
            else:
                # Get all text content
                content = soup.get_text(separator='\n', strip=True)
            
            # Remove extra whitespace
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            content = '\n'.join(lines)
            
            # Calculate hash
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            return {
                'success': True,
                'content': content,
                'hash': content_hash,
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat(),
                'size': len(content)
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_cached_content(self, url):
        """Load cached content for a URL."""
        cache_file = self.get_cache_path(url)
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None
    
    def save_cached_content(self, url, data):
        """Save content to cache."""
        cache_file = self.get_cache_path(url)
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def calculate_diff(self, old_content, new_content, max_length=500):
        """Calculate human-readable diff between two contents."""
        old_lines = old_content.split('\n')
        new_lines = new_content.split('\n')
        
        diff = list(difflib.unified_diff(
            old_lines,
            new_lines,
            lineterm='',
            n=0  # No context lines
        ))
        
        if not diff:
            return None
        
        # Format diff nicely
        changes = []
        for line in diff[2:]:  # Skip header lines
            if line.startswith('+'):
                changes.append(f"ADDED: {line[1:]}")
            elif line.startswith('-'):
                changes.append(f"REMOVED: {line[1:]}")
        
        diff_text = '\n'.join(changes)
        
        # Truncate if too long
        if len(diff_text) > max_length:
            diff_text = diff_text[:max_length] + f"\n... (truncated, {len(changes)} total changes)"
        
        return diff_text
    
    def send_email(self, subject, body, is_html=False):
        """Send email notification."""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = EMAIL_CONFIG['sender_email']
            msg['To'] = EMAIL_CONFIG['recipient_email']
            
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
                server.starttls()
                server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"❌ Email failed: {e}")
            self.log(f"Email error: {e}")
            return False
    
    def send_change_notification(self, site, old_data, new_data):
        """Send notification about website change."""
        subject = f"🔔 Website Changed: {site['name']}"
        
        # Calculate diff if enabled
        diff_text = ""
        if NOTIFICATION_CONFIG['include_diff'] and old_data and new_data:
            diff = self.calculate_diff(
                old_data.get('content', ''),
                new_data.get('content', ''),
                NOTIFICATION_CONFIG['max_diff_length']
            )
            if diff:
                diff_text = f"\n\nChanges Detected:\n{'='*50}\n{diff}\n{'='*50}"
        
        body = f"""
Website Change Detected!

Site: {site['name']}
URL: {site['url']}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Previous Check: {old_data.get('timestamp', 'Unknown') if old_data else 'First check'}
Current Check: {new_data.get('timestamp', 'Unknown')}

Status: Content has changed
{diff_text}

---
Website Change Monitor
"""
        
        self.send_email(subject, body)
        print(f"📧 Email sent: {site['name']}")
    
    def send_error_notification(self, site, error):
        """Send notification about monitoring error."""
        if not NOTIFICATION_CONFIG['send_on_error']:
            return
        
        subject = f"⚠️ Website Monitor Error: {site['name']}"
        
        body = f"""
Error Monitoring Website

Site: {site['name']}
URL: {site['url']}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Error: {error}

The website may be down or unreachable.

---
Website Change Monitor
"""
        
        self.send_email(subject, body)
        print(f"📧 Error notification sent: {site['name']}")
    
    def check_site(self, site):
        """Check a single site for changes."""
        url = site['url']
        print(f"\n🔍 Checking: {site['name']}")
        print(f"   URL: {url}")
        
        # Fetch current content
        current_data = self.fetch_content(url, site.get('selector'))
        
        if not current_data['success']:
            print(f"   ❌ Error: {current_data['error']}")
            site['error_count'] += 1
            site['status'] = 'error'
            
            if site['error_count'] >= MONITOR_CONFIG['retry_attempts']:
                self.send_error_notification(site, current_data['error'])
            
            self.save_sites()
            return False
        
        # Reset error count on success
        site['error_count'] = 0
        site['status'] = 'ok'
        site['last_checked'] = datetime.now().isoformat()
        
        # Load cached content
        cached_data = self.get_cached_content(url)
        
        # Compare hashes
        if cached_data:
            if current_data['hash'] != cached_data['hash']:
                print(f"   🔔 CHANGE DETECTED!")
                print(f"   Old hash: {cached_data['hash'][:16]}...")
                print(f"   New hash: {current_data['hash'][:16]}...")
                
                site['last_changed'] = datetime.now().isoformat()
                
                # Send notification
                self.send_change_notification(site, cached_data, current_data)
                
                # Update cache
                self.save_cached_content(url, current_data)
            else:
                print(f"   ✅ No changes")
        else:
            print(f"   📝 First check - baseline saved")
            if NOTIFICATION_CONFIG['send_on_first_check']:
                self.send_change_notification(site, None, current_data)
            
            # Save initial cache
            self.save_cached_content(url, current_data)
        
        self.save_sites()
        return True
    
    def check_all_sites(self):
        """Check all monitored sites."""
        if not self.sites:
            print("\n📭 No sites being monitored")
            return
        
        print(f"\n{'='*60}")
        print(f"🔍 Website Change Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        print(f"Monitoring {len(self.sites)} site(s)")
        
        for site in self.sites:
            self.check_site(site)
            time.sleep(2)  # Polite delay between requests
        
        print(f"\n{'='*60}")
        print(f"✅ Check complete")
        print(f"{'='*60}\n")
    
    def list_sites(self):
        """List all monitored sites."""
        if not self.sites:
            print("\n📭 No sites being monitored")
            return
        
        print(f"\n{'='*60}")
        print("📋 MONITORED SITES")
        print(f"{'='*60}\n")
        
        for i, site in enumerate(self.sites, 1):
            status_emoji = {
                'ok': '✅',
                'error': '❌',
                'pending': '⏳'
            }.get(site['status'], '❓')
            
            print(f"{i}. {status_emoji} {site['name']}")
            print(f"   URL: {site['url']}")
            print(f"   Status: {site['status']}")
            
            if site['last_checked']:
                last_checked = datetime.fromisoformat(site['last_checked'])
                print(f"   Last checked: {last_checked.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"   Last checked: Never")
            
            if site['last_changed']:
                last_changed = datetime.fromisoformat(site['last_changed'])
                print(f"   Last changed: {last_changed.strftime('%Y-%m-%d %H:%M:%S')}")
            
            if site.get('selector'):
                print(f"   Monitoring: {site['selector']}")
            
            print()
    
    def log(self, message):
        """Log message to file."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def run_scheduler(self):
        """Run the monitor on a schedule."""
        interval = MONITOR_CONFIG['check_interval_minutes']
        
        print(f"\n🚀 Website Monitor Started")
        print(f"⏰ Checking every {interval} minutes")
        print(f"📧 Notifications: {EMAIL_CONFIG['recipient_email']}")
        print(f"📝 Monitoring {len(self.sites)} site(s)")
        print(f"\nPress Ctrl+C to stop\n")
        
        # Schedule the check
        schedule.every(interval).minutes.do(self.check_all_sites)
        
        # Run immediately on start
        self.check_all_sites()
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Monitor stopped")


def show_menu():
    """Show interactive menu."""
    print("\n" + "="*60)
    print("🔍 WEBSITE CHANGE MONITOR")
    print("="*60)
    print("\nOptions:")
    print("1. Add website to monitor")
    print("2. Remove website")
    print("3. List monitored websites")
    print("4. Check all sites now")
    print("5. Start monitoring (scheduled)")
    print("6. Test email notification")
    print("7. Exit")
    print()
    
    choice = input("Select option (1-7): ").strip()
    return choice


def main():
    """Main entry point."""
    monitor = WebsiteMonitor()
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            # Add website
            print("\n➕ Add Website")
            url = input("Enter URL: ").strip()
            name = input("Enter name (or press Enter to use URL): ").strip()
            
            use_selector = input("Monitor specific section? (y/n): ").strip().lower()
            selector = None
            if use_selector == 'y':
                selector = input("Enter CSS selector (e.g., '#main-content'): ").strip()
            
            monitor.add_site(url, name or None, selector)
            
        elif choice == '2':
            # Remove website
            monitor.list_sites()
            if monitor.sites:
                url = input("\nEnter URL to remove: ").strip()
                monitor.remove_site(url)
        
        elif choice == '3':
            # List websites
            monitor.list_sites()
        
        elif choice == '4':
            # Check now
            monitor.check_all_sites()
        
        elif choice == '5':
            # Start monitoring
            if not monitor.sites:
                print("\n❌ No sites to monitor. Add some first!")
            else:
                monitor.run_scheduler()
        
        elif choice == '6':
            # Test email
            print("\n📧 Testing email...")
            success = monitor.send_email(
                "Website Monitor Test",
                "This is a test email from Website Change Monitor.\n\nIf you received this, email notifications are working!"
            )
            if success:
                print("✅ Test email sent!")
            else:
                print("❌ Email failed. Check your config.py settings.")
        
        elif choice == '7':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid choice")
        
        if choice != '5':  # Don't pause after scheduler (it runs continuously)
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
