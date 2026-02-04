# 🚀 ඉක්මන් සකස් කිරීමේ මාර්ගෝපදේශය

## 📦 1. API Deploy කරන්න (Koyeb/Render)

### Koyeb (RECOMMENDED - ලේසියි!):

1. **Koyeb Account එකක් හදන්න:**
   - https://koyeb.com වලට යන්න
   - Sign up with GitHub

2. **New Service හදන්න:**
   - Create Service → GitHub
   - Repository select කරන්න (youtube-api-ultimate)
   - Builder: Buildpack
   - Build command: `pip install -r requirements.txt && pip install --upgrade yt-dlp`
   - Run command: `python main.py`
   - Port: `8000`
   - Deploy click කරන්න!

3. **API URL Copy කරන්න:**
   ```
   https://your-app-name-your-username.koyeb.app
   ```

---

## 🤖 2. WhatsApp Bot Setup කරන්න

### A. song.js File Replace කරන්න:

```bash
cd Apex-MD-v2-main/plugins/

# Backup
cp song.js song.js.backup

# Replace (download කරපු song.js file එක copy කරන්න)
cp /path/to/downloaded/song.js .
```

### B. config.env Update කරන්න:

```env
# ඔබේ API URL add කරන්න (NO https://)
YOUTUBE_API=your-app-name-your-username.koyeb.app

# උදාහරණයක්:
YOUTUBE_API=operational-babbie-h79160251-a8340c9a.koyeb.app
```

**⚠️ වැදගත්:**
- `https://` add කරන්න එපා
- URL එක copy කරද්දී පමණක් app name එක
- `/` අවසානේ add කරන්න එපා

### C. Bot Restart කරන්න:

```bash
# PM2 use කරනවා නම්:
pm2 restart apex-md

# හෝ manual:
npm start
```

---

## ✅ 3. Test කරන්න

### A. API Test (Terminal එකෙන්):

```bash
# Health check
curl https://your-api.koyeb.app/health

# Audio download test
curl "https://your-api.koyeb.app/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&quality=audio"
```

**Expected response:**
```json
{
  "success": true,
  "title": "...",
  "download_url": "https://...",
  "quality": "audio"
}
```

### B. Bot Test (WhatsApp එකෙන්):

Bot එකට message එකක් send කරන්න:
```
.song nirwaane
```

**Expected:**
1. 🔎 Searching...
2. Thumbnail + info එනවා
3. ⏳ Downloading...
4. 🎵 Audio file send වෙනවා
5. ✅ Success!

---

## 🔧 4. Troubleshooting (ගැටලු ඇත්නම්)

### ❌ API Response නැහැ:

```bash
# 1. Health check කරන්න
curl https://your-api.koyeb.app/health

# 2. Koyeb logs බලන්න
# Koyeb dashboard → Service → Logs tab

# 3. API running ද verify කරන්න
# Status: "Healthy" show වෙන්න ඕන
```

### ❌ Bot download වෙන්නේ නැහැ:

**Check 1: config.env**
```bash
cat config.env | grep YOUTUBE_API

# Output විය යුත්තේ:
YOUTUBE_API=your-app.koyeb.app
```

**Check 2: song.js file**
```bash
ls -la plugins/song.js

# File එක replace වෙලාද බලන්න
# Size එක ~18KB විතර විය යුතුයි
```

**Check 3: Bot logs**
```bash
pm2 logs apex-md

# Errors show වෙනවද බලන්න
```

### ❌ "All methods failed" Error:

**විසඳුම:**
1. Video private/restricted ද check කරන්න
2. Different video try කරන්න (test)
3. 2-3 minutes wait කරලා retry
4. API logs බලන්න errors ඇත්දැයි

---

## 📋 5. සම්පූර්ණ Setup එක Summary

```bash
# === 1. API Deploy (Koyeb) ===
# Web dashboard එකෙන් setup කරන්න
# URL copy කරන්න: your-app.koyeb.app

# === 2. Bot Files Update ===
cd Apex-MD-v2-main/plugins/
cp song.js song.js.backup
cp /downloaded/song.js .

# === 3. Config Update ===
nano config.env
# Add: YOUTUBE_API=your-app.koyeb.app
# Save: Ctrl+X, Y, Enter

# === 4. Restart Bot ===
pm2 restart apex-md

# === 5. Test ===
# WhatsApp: .song test
```

---

## 💡 Pro Tips

### 1. API URL හරියටද බලන්න:

```bash
# Terminal එකෙන් test කරන්න:
curl https://your-api.koyeb.app/health

# Success response:
{"status":"healthy","cache_size":0,"methods_available":4}
```

### 2. Bot Commands:

```
.song [name]        - Audio download (MP3)
.song [youtube url] - Audio from link
.video [name]       - Video download (MP4)
.video [url]        - Video from link
```

### 3. Cache System:

- එකම song 1 hour cache වෙනවා
- පළමු download slow, next fast
- Cache clear කරන්න: `curl https://your-api.koyeb.app/clear-cache`

### 4. Rate Limits:

- 10 downloads per minute (එකම IP)
- Limit exceed වුණොත් 1 minute wait

---

## 🎯 Expected Flow

### Successful Download:

```
User: .song nirwaane
  ↓
Bot: 🔎 Searching...
  ↓
Bot: [Thumbnail + Info Card]
     📌 Title: Nirwaane
     👤 Artist: THARAKA
     ⏱️ Duration: 3:13
     ⏳ Downloading from API...
  ↓
API: Try Cobalt → Success! ✅
  ↓
Bot: Downloads file from URL
  ↓
Bot: 🎵 [Sends Audio File]
  ↓
Bot: ✅ Success!
```

### Error Example:

```
User: .song test
  ↓
Bot: 🔎 Searching...
  ↓
API: All 4 methods tried → All failed
  ↓
Bot: ❌ Download failed!
     Possible reasons:
     • Video is private
     • Try again later
```

---

## 📞 Additional Help

### Koyeb Dashboard:
- Logs: Service → Logs tab
- Restart: Service → Settings → Restart
- URL: Service → Overview → Public URL

### Bot Logs:
```bash
# Real-time logs
pm2 logs apex-md --lines 100

# Specific errors
pm2 logs apex-md | grep ERROR
```

### API Logs:
Koyeb dashboard එකේ live logs පෙන්නනවා:
```
[API] Calling: https://...
[Cobalt] Trying cobalt.tools API...
[Cobalt] ✅ Got download URL
[Song] Download successful, file size: 7653928 bytes
[Song] Sent successfully!
```

---

## ✅ Checklist

Setup කරද්දී මේ සියල්ල verify කරන්න:

- [ ] API deployed on Koyeb/Render
- [ ] API health check works
- [ ] song.js file replaced
- [ ] config.env updated with API URL
- [ ] Bot restarted
- [ ] Test song download works
- [ ] No errors in logs

---

## 🎉 සාරාංශය

1. **API Deploy:** Koyeb/Render (5 minutes)
2. **Bot Update:** song.js + config.env (2 minutes)
3. **Restart:** pm2 restart (30 seconds)
4. **Test:** `.song test` (1 minute)

**Total Setup Time:** ~10 minutes!

---

**සියල්ල හරි නම් දැන් bot එක 95%+ වැඩ කරයි! 🎊**

Any issues? README.md full file එක කියවන්න හෝ logs check කරන්න!

---

Made with ❤️ by the community
