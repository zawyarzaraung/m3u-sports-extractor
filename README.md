# 🚀 M3U Sports Extractor Automation

ဒီ Project က သတ်မှတ်ထားတဲ့ Raw M3U Link တွေထဲကနေ အားကစားနဲ့ ဘောလုံးပွဲဆိုင်ရာ လိုင်းတွေကို ၆ နာရီခြားတစ်ခါ Auto စစ်ထုတ်ပြီး Active/Dead ခွဲခြားပေးနေတဲ့ Automated System ဖြစ်ပါတယ်။

---

### 📊 လက်ရှိ လိုင်းများ၏ အခြေအနေ (Live Status Dashboard)

* **နောက်ဆုံး Update လုပ်ခဲ့သည့်အချိန်:** `2026-07-15 02:59 PM (မြန်မာစံတော်ချိန်)`
* **စုစုပေါင်း စစ်ဆေးခဲ့သည့် လိုင်းအရေအတွက်:** `153 လိုင်း`

| အခြေအနေ (Status) | လိုင်းအရေအတွက် | M3U Playlist Link | လုပ်ဆောင်ချက် |
| :--- | :---: | :--- | :--- |
| ✅ **Active Channels** | `69` | `https://raw.githubusercontent.com/zawyarzaraung/m3u-sports-extractor/main/playlist/active.m3u` | လက်ရှိ ကြည့်ရှု၍ရသော အားကစားလိုင်းများ |
| ⏳ **Dead Channels (စောင့်ကြည့်)** | `84` | `https://raw.githubusercontent.com/zawyarzaraung/m3u-sports-extractor/main/playlist/dead.m3u` | ဒေါင်းနေသဖြင့် ၅ ရက် စောင့်ကြည့်ဇုန်ထဲ ရောက်နေသောလိုင်းများ |

---

### 🛠️ စနစ်၏ အလုပ်လုပ်ပုံ (Workflow Logic)
1. **Extract Sports:** Raw Links များထဲမှ အားကစား Keyword ပါဝင်သော လိုင်းများကို Regex ဖြင့် စက္ကန့်ပိုင်းအတွင်း ရှာဖွေစစ်ထုတ်သည်။
2. **Health Check:** ရလာသောလိုင်းများကို အလုပ်လုပ်မလုပ် စစ်ဆေးပြီး `active.m3u` နှင့် `dead.m3u` ခွဲထုတ်သည်။
3. **5-Days Quarantine:** Dead ဖြစ်သွားသော လိုင်းများကို ရက်စွဲမှတ်သားထားပြီး ၅ ရက်အတွင်း အသက်ပြန်ရှင်မလာပါက အပြီးတိုင် ဖျက်ထုတ်သည်။
4. **Auto Update:** ဤ Report နှင့် Playlist များကို ၆ နာရီခြားတစ်ခါ GitHub Actions မှ အလိုအလျောက် ပတ်ပေးသည်။

---
*Developed with ❤️ for the community.*
