import os
import re
import requests
from datetime import datetime, timedelta

# ဖိုင်လမ်းကြောင်းများ
EXTRACTED_FILE = os.path.join("playlist", "extracted_sports.m3u")
ACTIVE_FILE = os.path.join("playlist", "active.m3u")
DEAD_FILE = os.path.join("playlist", "dead.m3u")

def check_link_status(url):
    """Link အသက်ရှင်/မရှင်ကို HTTP Header (သို့) Request ဖြင့် စစ်ဆေးသည်"""
    try:
        # Stream link တွေမို့လို့ တစ်ဖိုင်လုံးမဒေါင်းဘဲ Header ပဲ အမြန်စစ်ပါတယ်
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code in [200, 206, 301, 302]:
            return True
        # အချို့ server များက HEAD ကိုငြင်းတတ်သဖြင့် GET ဖြင့် ထပ်စစ်သည်
        response = requests.get(url, timeout=5, stream=True)
        if response.status_code in [200, 206]:
            return True
    except:
        pass
    return False

def load_m3u_file(file_path):
    """M3U ဖိုင်ကို ဖတ်ပြီး လိုင်းများကို list ပုံစံပြောင်းသည်"""
    channels = []
    if not os.path.exists(file_path):
        return channels
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.splitlines() if hasattr(f, 'splitlines') else f.read().splitlines()
        
    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF"):
            inf = lines[i]
            if i + 1 < len(lines) and not lines[i+1].startswith("#"):
                url = lines[i+1].strip()
                channels.append({"inf": inf, "url": url})
    return channels

def parse_dead_since(inf_line):
    """dead_since=\"YYYY-MM-DD\" tag ကို ရှာပြီး datetime object ပြောင်းသည်"""
    match = re.search(r'dead_since="(\d{4}-\d{2}-\d{2})"', inf_line)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d")
    return None

def run_health_check():
    print("[+] Health Check စတင်နေပါပြီ...")
    
    # ၁။ လက်ရှိ ရှိပြီးသား ဖိုင်ဟောင်းများထဲမှ လိုင်းများကို ဖတ်ယူခြင်း
    extracted_pool = load_m3u_file(EXTRACTED_FILE)
    old_dead_pool = load_m3u_file(DEAD_FILE)
    
    # လိုင်းအားလုံးကို စုစည်းပြီး စစ်ဆေးရန် ပြင်ဆင်ခြင်း
    # Extracted ထဲကရော Dead ထဲကပါ အကုန်ပြန်စစ်မည် (Dead ကနေ Active ပြန်ဖြစ်လာနိုင်၍)
    all_to_check = {ch['url']: ch['inf'] for ch in extracted_pool}
    for ch in old_dead_pool:
        # Extracted ထဲမှာ မပါသေးရင်လည်း Dead ထဲကကောင်ကို ထည့်စစ်မည်
        if ch['url'] not in all_to_check:
            all_to_check[ch['url']] = ch['inf']

    active_channels = []
    new_dead_pool = []
    
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    five_days_ago = datetime.utcnow() - timedelta(days=5)

    print(f"[+] စုစုပေါင်း စစ်ဆေးမည့်လိုင်းအရေအတွက်: {len(all_to_check)}")

    for url, inf in all_to_check.items():
        is_alive = check_link_status(url)
        
        # tag အဟောင်းများကို ရှင်းထုတ်ခြင်း
        clean_inf = re.sub(r'\s*dead_since="[^"]*"', '', inf)

        if is_alive:
            print(f"[✅ ACTIVE] -> {url}")
            active_channels.append((clean_inf, url))
        else:
            print(f"[❌ DEAD] -> {url}")
            # စသေတဲ့ နေ့စွဲကို စစ်ဆေးခြင်း
            dead_date = parse_dead_since(inf)
            
            if dead_date is None:
                # ယခုမှ စသေသောလိုင်းဖြစ်ပါက ယနေ့ရက်စွဲတပ်မည်
                updated_inf = f'{clean_inf} dead_since="{today_str}"'
                new_dead_pool.append((updated_inf, url))
            else:
                # အရင်ကတည်းက သေနေသောလိုင်းဖြစ်ပါက ၅ ရက် ပြည့်မပြည့်စစ်မည်
                if dead_date >= five_days_ago:
                    # ၅ ရက်မပြည့်သေးပါက dead.m3u ထဲ ဆက်ထားမည်
                    new_dead_pool.append((inf, url))
                else:
                    # ၅ ရက်ကျော်သွားပါက အပြီးဖျက်မည် (ဒီနေရာမှာ skip လိုက်တာမို့ new_dead_pool ထဲမပါတော့ပါ)
                    print(f"[-] ၅ ရက်ကျော်သွားသဖြင့် အပြီးဖျက်လိုက်ပါပြီ: {url}")

    # ၂။ active.m3u ထဲသို့ ရလဒ်များ သိမ်းဆည်းခြင်း
    with open(ACTIVE_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for inf, url in active_channels:
            f.write(f"{inf}\n{url}\n")

    # ၃။ dead.m3u ထဲသို့ ရလဒ်များ သိမ်းဆည်းခြင်း
    with open(DEAD_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for inf, url in new_dead_pool:
            f.write(f"{inf}\n{url}\n")

    print(f"[+] Health Check ပြီးဆုံးပါပြီ။ Active: {len(active_channels)} | Dead: {len(new_dead_pool)}")

if __name__ == "__main__":
    run_health_check()
