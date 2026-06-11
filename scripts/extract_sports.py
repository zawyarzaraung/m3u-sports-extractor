import os
import re
import requests

SOURCE_FILE = os.path.join("source", "all_channels.m3u")
EXTRACTED_FILE = os.path.join("playlist", "extracted_sports.m3u")

KEYWORDS = [
    r"group-title=\".*?sports.*?\"",
    r"group-title=\".*?football.*?\"",
    r"group-title=\".*?world cup.*?\"",
    r"group-title=\".*?fifa.*?\"",
    r"group-title=\".*?live.*sports.*?\"",
    r"Football World Cup 2026",
    r"Sports",
    r"Football"
]

def fetch_raw_links():
    if not os.path.exists(SOURCE_FILE):
        print(f"[-] {SOURCE_FILE} မတွေ့ရှိပါ။")
        return []
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return links

def extract_sports_channels():
    print("[+] အားကစားလိုင်းများ စတင်စစ်ထုတ်နေပါပြီ...")
    raw_urls = fetch_raw_links()
    if not raw_urls:
        return

    extracted_channels = []
    seen_urls = set()
    combined_pattern = re.compile("|".join(KEYWORDS), re.IGNORECASE)

    for url in raw_urls:
        print(f"[+] Downloading: {url}")
        try:
            response = requests.get(url, timeout=15)
            if response.status_code != 200:
                continue
            lines = response.text.splitlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    inf_line = lines[i]
                    if i + 1 < len(lines) and not lines[i+1].startswith("#"):
                        stream_url = lines[i+1].strip()
                        if combined_pattern.search(inf_line):
                            if stream_url not in seen_urls:
                                seen_urls.add(stream_url)
                                extracted_channels.append((inf_line, stream_url))
        except Exception as e:
            print(f"[-] Error: {e}")

    os.makedirs(os.path.dirname(EXTRACTED_FILE), exist_ok=True)
    with open(EXTRACTED_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for inf, stream in extracted_channels:
            f.write(f"{inf}\n{stream}\n")
    print(f"[+] စုစုပေါင်း: {len(extracted_channels)} လိုင်း ထုတ်ယူပြီးပါပြီ။")

if __name__ == "__main__":
    extract_sports_channels()
