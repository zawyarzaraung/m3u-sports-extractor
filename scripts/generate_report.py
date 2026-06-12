import os
import re
from datetime import datetime

ACTIVE_FILE = os.path.join("playlist", "active.m3u")
DEAD_FILE = os.path.join("playlist", "dead.m3u")
README_FILE = "README.md"

def count_channels(file_path):
    if not os.path.exists(file_path):
        return 0
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return len(re.findall(r"#EXTINF", content))

def generate_dashboard():
    print("[+] Dashboard Report စတင်ထုတ်လုပ်နေပါပြီ...")
    
    active_count = count_channels(ACTIVE_FILE)
    dead_count = count_channels(DEAD_FILE)
    total_count = active_count + dead_count
    
    import datetime as dt
    mm_time = datetime.utcnow() + dt.timedelta(hours=6, minutes=30)
    time_str = mm_time.strftime("%Y-%m-%d %I:%M %p")

    repo_env = os.getenv("GITHUB_REPOSITORY", "zawyarzaraung/m3u-sports-extractor")

    markdown_content = f"""# 🚀 M3U Sports Extractor Automation

ဒီ Project က သတ်မှတ်ထားတဲ့ Raw M3U Link တွေထဲကနေ အားကစားနဲ့ ဘောလုံးပွဲဆိုင်ရာ လိုင်းတွေကို ၆ နာရီခြားတစ်ခါ Auto စစ်ထုတ်ပြီး Active/Dead ခွဲခြားပေးနေတဲ့ Automated System ဖြစ်ပါတယ်။

---

### 📊 လက်ရှိ လိုင်းများ၏ အခြေအနေ (Live Status Dashboard)

* **နောက်ဆုံး Update လုပ်ခဲ့သည့်အချိန်:** `{time_str} (မြန်မာစံတော်ချိန်)`
* **စုစုပေါင်း စစ်ဆေးခဲ့သည့် လိုင်းအရေအတွက်:** `{total_count} လိုင်း`

| အခြေအနေ (Status) | လိုင်းအရေအတွက် | M3U Playlist Link | လုပ်ဆောင်ချက် |
| :--- | :---: | :--- | :--- |
| ✅ **Active Channels** | `{active_count}` | `https://raw.githubusercontent.com/{repo_env}/main/playlist/active.m3u` | လက်ရှိ ကြည့်ရှု၍ရသော အားကစားလိုင်းများ |
| ⏳ **Dead Channels (စောင့်ကြည့်)** | `{dead_count}` | `https://raw.githubusercontent.com/{repo_env}/main/playlist/dead.m3u` | ဒေါင်းနေသဖြင့် ၅ ရက် စောင့်ကြည့်ဇုန်ထဲ ရောက်နေသောလိုင်းများ |

---

### 🛠️ စနစ်၏ အလုပ်လုပ်ပုံ (Workflow Logic)
1. **Extract Sports:** Raw Links များထဲမှ အားကစား Keyword ပါဝင်သော လိုင်းများကို Regex ဖြင့် စက္ကန့်ပိုင်းအတွင်း ရှာဖွေစစ်ထုတ်သည်။
2. **Health Check:** ရလာသောလိုင်းများကို အလုပ်လုပ်မလုပ် စစ်ဆေးပြီး `active.m3u` နှင့် `dead.m3u` ခွဲထုတ်သည်။
3. **5-Days Quarantine:** Dead ဖြစ်သွားသော လိုင်းများကို ရက်စွဲမှတ်သားထားပြီး ၅ ရက်အတွင်း အသက်ပြန်ရှင်မလာပါက အပြီးတိုင် ဖျက်ထုတ်သည်။
4. **Auto Update:** ဤ Report နှင့် Playlist များကို ၆ နာရီခြားတစ်ခါ GitHub Actions မှ အလိုအလျောက် ပတ်ပေးသည်။

---
*Developed with ❤️ for the community.*
"""

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print("[+] README.md Dashboard ကို Update လုပ်ပြီးပါပြီ။")

if __name__ == "__main__":
    generate_dashboard()
