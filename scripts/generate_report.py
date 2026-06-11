import os
import re
from datetime import datetime

# ဖိုင်လမ်းကြောင်းများ
ACTIVE_FILE = os.path.join("playlist", "active.m3u")
DEAD_FILE = os.path.join("playlist", "dead.m3u")
README_FILE = "README.md"

def count_channels(file_path):
    """M3U ဖိုင်ထဲရှိ စုစုပေါင်း လိုင်းအရေအတွက်ကို တွက်ချက်သည်"""
    if not os.path.exists(file_path):
        return 0
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # #EXTINF ပါသည့် အကြိမ်အရေအတွက်ကို ရေတွက်ခြင်း
    return len(re.findall(r"#EXTINF", content))

def generate_dashboard():
    print("[+] Dashboard Report စတင်ထုတ်လုပ်နေပါပြီ...")
    
    active_count = count_channels(ACTIVE_FILE)
    dead_count = count_channels(DEAD_FILE)
    total_count = active_count + dead_count
    
    # မြန်မာစံတော်ချိန်အတွက် UTC+6:30 တွက်ချက်ခြင်း (GitHub Actions သည် UTC သုံးသဖြင့်)
    # 2026 အတွက် လက်ရှိအချိန်ကို ယူမည်
    current_time = datetime.utcnow()
    # မြန်မာပြည်က ကြည့်ရင် အချိန်ကွက်တိဖြစ်အောင် UTC ထဲ ၆ နာရီ မိနစ် ၃၀ ပေါင်းပေးထားသည်
    import datetime as dt
    mm_time = current_time + dt.timedelta(hours=6, minutes=30)
    time_str = mm_time.strftime("%Y-%m-%d %I:%M %p")

    # README ထဲတွင် အလိုအလျောက် သွားရေးမည့် Markdown စာသား
    markdown_content = f"""# 🚀 M3U Sports Extractor Automation

ဒီ Project က သတ်မှတ်ထားတဲ့ Raw M3U Link တွေထဲကနေ အားကစားနဲ့ ဘောလုံးပွဲဆိုင်ရာ လိုင်းတွေကို ၆ နာရီခြားတစ်ခါ Auto စစ်ထုတ်ပြီး Active/Dead ခွဲခြားပေးနေတဲ့ Automated System ဖြစ်ပါတယ်။

---

### 📊 လက်ရှိ လိုင်းများ၏ အခြေအနေ (Live Status Dashboard)

* **နောက်ဆုံး Update လုပ်ခဲ့သည့်အချိန်:** `{time_str} (မြန်မာစံတော်ချိန်)`
* **စုစုပေါင်း စစ်ဆေးခဲ့သည့် လိုင်းအရေအတွက်:** `{total_count} လိုင်း`

| အခြေအနေ (Status) | လိုင်းအရေအတွက် | M3U Playlist Link | လုပ်ဆောင်ချက် |
| :--- | :---: | :--- | :--- |
| ✅ **Active Channels** | `{active_count}` | `https://raw.githubusercontent.com/{{{{ github.repository }}}}/main/playlist/active.m3u` | လက်ရှိ ကြည့်ရှု၍ရသော အားကစားလိုင်းများ |
| ⏳ **Dead Channels (စောင့်ကြည့်)** | `{dead_count}` | `https://raw.githubusercontent.com/{{{{ github.repository }}}}/main/playlist/dead.m3u` | ဒေါင်းနေသဖြင့် ၅ ရက် စောင့်ကြည့်ဇုန်ထဲ ရောက်နေသောလိုင်းများ |

---

### 🛠️ စနစ်၏ အလုပ်လုပ်ပုံ (Workflow Logic)
1. **Extract Sports:** Raw Links များထဲမှ အားကစား Keyword ပါဝင်သော လိုင်းများကို Regex ဖြင့် စက္ကန့်ပိုင်းအတွင်း ရှာဖွေစစ်ထုတ်သည်။
2. **Health Check:** ရလာသောလိုင်းများကို အလုပ်လုပ်မလုပ် စစ်ဆေးပြီး `active.m3u` နှင့် `dead.m3u` ခွဲထုတ်သည်။
3. **5-Days Quarantine:** Dead ဖြစ်သွားသော လိုင်းများကို ရက်စွဲမှတ်သားထားပြီး ၅ ရက်အတွင်း အသက်ပြန်ရှင်မလာပါက အပြီးတိုင် ဖျက်ထုတ်သည်။
4. **Auto Update:** ဤ Report နှင့် Playlist များကို ၆ နာရီခြားတစ်ခါ GitHub Actions မှ အလိုအလျောက် ပတ်ပေးသည်။

---
*Developed with ❤️ for the community.*
"""

    # GitHub workflow ထဲတွင် template link မှန်စေရန် string ပြင်ဆင်ခြင်း
    # github.repository ကို တကယ့် repo နာမည်နဲ့ အစားထိုးနိုင်အောင် လုပ်ပေးထားခြင်း
    repo_env = os.getenv("GITHUB_REPOSITORY", "your-username/m3u-sports-extractor")
    markdown_content = markdown_content.replace("{{{{ github.repository }}}}", repo_env)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print("[+] README.md Dashboard ကို Update လုပ်ပြီးပါပြီ။")

if __name__ == "__main__":
    generate_dashboard()
