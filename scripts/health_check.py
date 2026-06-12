import os
import re
import requests
from datetime import datetime, timedelta

# ဖိုင်လမ်းကြောင်းများ
EXTRACTED_FILE = os.path.join("playlist", "extracted_sports.m3u")
ACTIVE_FILE = os.path.join("playlist", "active.m3u")
DEAD_FILE = os.path.join("playlist", "dead.m3u")

def check_link_status(url):
    """Firewall များကို ကျော်ဖြတ်နိုင်ရန် User-Agent အပြည့်အစုံဖြင့် စစ်ဆေးသည်"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # ၁။ HEAD Request ဖြင့် အရင်စစ်သည်
        response = requests.head(url, headers=headers, timeout=8, allow_redirects=True)
        if response.status_code in [200, 206, 301, 302]:
            return True
        
        # ⚠️ GET ဖြင့် ထပ်စစ်သည်
        response = requests.get(url, headers=headers, timeout=8, stream=True)
        if response.status_code in [200, 206]:
            return True
            
        # 💡 Response Status Code က 403 ဖြစ်နေရင်တောင် အရှင်အဖြစ် ယာယီသတ်မှတ်ပေးမည်
        if response.status_code == 403:
            return True
    except:
        pass
    return False

def load_m3u_file(file_path):
    channels = []
    if not os.path.exists(file_path):
        return channels
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF"):
            inf = lines[i]
            if i + 1 < len(lines) and not lines[i+1].startswith("#"):
                url = lines[i+1].strip()
                channels.append({"inf": inf, "url": url})
    return channels

def parse_dead_since(inf_line):
    match = re.search(r'dead_since="(\d{4}-\d{2}-\d{2})"', inf_line)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d")
    return None

def run_health_check():
    print("[+] Enhanced Health Check စတင်နေပါပြီ...")
    
    extracted_pool = load_m3u_file(EXTRACTED_FILE)
    old_dead_pool = load_m3u_file(DEAD_FILE)
    
    all_to_check = {ch['url']: ch['inf'] for ch in extracted_pool}
    for ch in old_dead_pool:
        if ch['url'] not in all_to_check:
            all_to_check[ch['url']] = ch['inf']

    active_channels = []
    new_dead_pool = []
    
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    five_days_ago = datetime.utcnow() - timedelta(days=5)

    print(f"[+] Сုစုပေါင်း စစ်ဆေးမည့်လိုင်းအရေအတွက်: {len(all_to_check)}")

    for url, inf in all_to_check.items():
        is_alive = check_link_status(url)
        clean_inf = re.sub(r'\s*dead_since="[^"]*"', '', inf)

        if is_alive:
            print(f"[✅ ACTIVE] -> {url}")
            active_channels.append((clean_inf, url))
        else:
            print(f"[❌ DEAD] -> {url}")
            dead_date = parse_dead_since(inf)
            if dead_date is None:
                updated_inf = f'{clean_inf} dead_since="{today_str}"'
                new_dead_pool.append((updated_inf, url))
            else:
                if dead_date >= five_days_ago:
                    new_dead_pool.append((inf, url))
                else:
                    print(f"[-] ၅ ရက်ကျော်သွားသဖြင့် အပြီးဖျက်လိုက်ပါပြီ: {url}")

    with open(ACTIVE_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for inf, url in active_channels:
            f.write(f"{inf}\n{url}\n")

    with open(DEAD_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for inf, url in new_dead_pool:
            f.write(f"{inf}\n{url}\n")

    print(f"[+] Enhanced Health Check ပြီးဆုံးပါပြီ။ Active: {len(active_channels)} | Dead: {len(new_dead_pool)}")

if __name__ == "__main__":
    run_health_check()
