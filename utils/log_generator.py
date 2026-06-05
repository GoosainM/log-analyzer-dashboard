import random
import time
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Configuration
NUM_NORMAL_RECORDS = 800
NUM_ATTACK_RECORDS = 200
OUTPUT_FILE = "data/sample_access.log"

# Standard mock data pools
RESOURCES = ["/index.html", "/about.html", "/contact.html", "/products", "/blog/post-1", "/assets/css/style.css", "/assets/js/main.js"]
METHODS = ["GET", "POST", "GET", "GET"] # Weighted towards GET requests

# Attack vectors to inject
MALICIOUS_URLS = [
    "/admin", "/admin/login", "/wp-login.php", "/config.php", 
    "/../../etc/passwd", "/index.php?id=1' UNION SELECT NULL--",
    "/admin.php?user=admin' OR '1'='1"
]

def generate_timestamp(base_time, index):
    """Generates sequential timestamps to simulate real-time traffic flow."""
    custom_time = base_time + timedelta(seconds=index * random.randint(1, 15))
    return custom_time.strftime("%d/%b/%Y:%H:%M:%S +0000")

def create_log_line(ip, timestamp, method, url, status, size):
    """Formats data into standard Apache Common Log Format."""
    return f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} {size}\n'

def generate_logs():
    log_lines = []
    base_time = datetime.now() - timedelta(days=1)
    
    # 1. Generate Normal Traffic
    print(f"Generating {NUM_NORMAL_RECORDS} normal traffic logs...")
    for i in range(NUM_NORMAL_RECORDS):
        ip = fake.ipv4_public()
        timestamp = generate_timestamp(base_time, i)
        method = random.choice(METHODS)
        url = random.choice(RESOURCES)
        status = random.choice([200, 200, 200, 304, 404]) # Mostly successful
        size = random.randint(150, 5000)
        
        log_lines.append((timestamp, create_log_line(ip, timestamp, method, url, status, size)))

    # 2. Inject Brute Force Attack (Simulating an attacker trying to crack a password)
    print("Injecting Brute Force attack simulation...")
    attacker_ip = "198.51.100.42"  # Distinct IP for tracking
    brute_time = base_time + timedelta(hours=4)
    for i in range(45):  # 45 rapid failed attempts
        brute_time += timedelta(seconds=random.randint(1, 3))
        ts = brute_time.strftime("%d/%b/%Y:%H:%M:%S +0000")
        log_lines.append((ts, create_log_line(attacker_ip, ts, "POST", "/login", 401, 240)))
    
    # One final successful login after brute forcing
    brute_time += timedelta(seconds=5)
    ts = brute_time.strftime("%d/%b/%Y:%H:%M:%S +0000")
    log_lines.append((ts, create_log_line(attacker_ip, ts, "POST", "/dashboard", 200, 1024)))

    # 3. Inject Web Vulnerability Scanning (SQLi & Directory Traversal)
    print(f"Injecting {NUM_ATTACK_RECORDS} web vulnerability scans...")
    scanner_ips = [fake.ipv4_public() for _ in range(3)] # 3 distinct attackers
    scan_time = base_time + timedelta(hours=8)
    
    for i in range(NUM_ATTACK_RECORDS):
        scan_time += timedelta(seconds=random.randint(5, 30))
        ts = scan_time.strftime("%d/%b/%Y:%H:%M:%S +0000")
        ip = random.choice(scanner_ips)
        url = random.choice(MALICIOUS_URLS)
        method = "GET"
        status = random.choice([403, 404, 500]) # Security blocks or missing paths
        size = random.randint(200, 400)
        
        log_lines.append((ts, create_log_line(ip, ts, method, url, status, size)))

    # Sort all logs by timestamp so they are mixed realistically
    log_lines.sort(key=lambda x: datetime.strptime(x[0], "%d/%b/%Y:%H:%M:%S +0000"))

    # Write to file
    import os
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        for _, line in log_lines:
            f.write(line)
            
    print(f"Successfully generated log file at: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_logs()