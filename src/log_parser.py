import re
import pandas as pd

# The regex pattern matching the Apache Common Log Format
LOG_PATTERN = r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<timestamp>[\w:/]+\s[+\-]\d{4})\]\s+"(?P<method>\S+)\s+(?P<url>\S+)\s+HTTP/\d\.\d"\s+(?P<status>\d{3})\s+(?P<size>\S+)'

def parse_log_file(file_path):
    """Reads a log file line by line, parses it with regex, and returns a Pandas DataFrame."""
    log_data = []
    
    print(f"Reading logs from {file_path}...")
    with open(file_path, "r") as f:
        for line in f:
            match = re.match(LOG_PATTERN, line)
            if match:
                log_data.append(match.groupdict())
                
    # Convert list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(log_data)
    
    # Clean up data types
    df['status'] = df['status'].astype(int)
    # If size is '-', replace with 0 (common in server logs for no payload)
    df['size'] = df['size'].replace('-', 0).astype(int)
    # Convert timestamp string to actual datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z')
    
    return df

def detect_threats(df):
    """Analyzes the DataFrame to find suspicious security activities."""
    print("\n=== RUNNING SECURITY THREAT DETECTION ===")
    
    # 1. Detect Brute Force Attempts (More than 20 failed logins from a single IP)
    failed_logins = df[(df['url'] == '/login') & (df['status'] == 401)]
    login_counts = failed_logins['ip'].value_counts()
    brute_force_suspects = login_counts[login_counts > 20]
    
    print(f"\n[!] Brute Force Suspects (Targeting /login with 401 errors):")
    if not brute_force_suspects.empty:
        for ip, count in brute_force_suspects.items():
            print(f"  - IP: {ip} failed {count} times.")
    else:
        print("  - No brute force patterns detected.")

    # 2. Detect Web Attacks (SQLi, Directory Traversal)
    attack_pattern = r"UNION|SELECT|'|OR|etc/passwd|\.\.\/"
    web_attacks = df[df['url'].str.contains(attack_pattern, case=False, na=False)]
    
    print(f"\n[!] Suspicious Web Attack Indicators Detected: {len(web_attacks)}")
    if not web_attacks.empty:
        attacker_summary = web_attacks['ip'].value_counts()
        for ip, count in attacker_summary.head(5).items():
            print(f"  - Attacker IP: {ip} sent {count} suspicious payloads.")
    
    return brute_force_suspects, web_attacks

if __name__ == "__main__":
    LOG_FILE = "data/sample_access.log"
    
    # Run the parser
    log_df = parse_log_file(LOG_FILE)
    print(f"Successfully loaded {len(log_df)} log lines into DataFrame.")
    
    # Run threat detection
    detect_threats(log_df)