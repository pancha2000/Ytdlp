# 🍪 Cookies Upload කරන සම්පූර්ණ මාර්ගෝපදේශය

## ⚡ ඉක්මන් සාරාංශය

YouTube bot detection bypass කරන්න **cookies අනිවාර්යයි!**

```
Browser Cookies → Export → Upload to API → ✅ Downloads Work!
```

---

## 📋 Step-by-Step (සිංහලෙන්)

### 1️⃣ Browser Extension Install කරන්න

#### Chrome/Edge:
1. මෙතනට යන්න: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
2. "Add to Chrome" click කරන්න
3. Install confirm කරන්න

#### Firefox:
1. මෙතනට යන්න: https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/
2. "Add to Firefox" click කරන්න
3. Install confirm කරන්න

---

### 2️⃣ YouTube Login වෙන්න

1. **youtube.com** වලට යන්න
2. ඔබේ Google account එකෙන් **login** වෙන්න
3. Video එකක් play කරන්න (test කරන්න login working ද කියලා)

⚠️ **වැදගත්:** 
- Private/Incognito mode එකෙන් **නොවෙයි**
- Normal browser window එකෙන් login වෙන්න

---

### 3️⃣ Cookies Export කරන්න

#### Chrome/Edge:
1. YouTube page එකේ ඉන්න විට extension icon click කරන්න (browser toolbar එකේ)
2. "Export" හෝ "Download" click කරන්න
3. File එක save වෙනවා → **`cookies.txt`** කියලා rename කරන්න

#### Firefox:
1. YouTube page එකේ extension icon click කරන්න
2. "Current Site" select කරලා export click
3. File save → **`cookies.txt`** rename කරන්න

---

### 4️⃣ Cookies File Verify කරන්න

File එක text editor එකෙන් open කරලා බලන්න:

```txt
# Netscape HTTP Cookie File
.youtube.com	TRUE	/	FALSE	1234567890	CONSENT	YES+...
.youtube.com	TRUE	/	TRUE	1234567890	__Secure-3PSID	xxxxx
.youtube.com	TRUE	/	FALSE	0	VISITOR_INFO1_LIVE	xxxxx
```

**තිබිය යුතු දේවල්:**
- ✅ `# Netscape HTTP Cookie File` - පළමු line එක
- ✅ `.youtube.com` - multiple lines
- ✅ `__Secure-3PSID` - ප්‍රධාන cookie
- ✅ `CONSENT` cookie

**නැති නම්:** Login කරලා නැතිව export කරලා තියෙන්න පුළුවන්. නැවත login වෙලා export කරන්න.

---

## 🚀 Upload කරන්න API එකට

### Method 1: Web Interface (ලේසිම!)

#### A. Local API (Testing):
```bash
# Browser එකෙන්:
http://localhost:8000
```

#### B. Deployed API (Koyeb/Render):
```bash
# Browser එකෙන්:
https://your-api.koyeb.app
```

**Steps:**
1. API URL එකට යන්න browser එකෙන්
2. "Upload Cookies" button click කරන්න
3. `cookies.txt` file select කරන්න
4. Upload click
5. ✅ "Cookies uploaded successfully!"

---

### Method 2: Command Line (Terminal)

#### Local API:
```bash
curl -X POST http://localhost:8000/upload-cookies \
  -F "file=@cookies.txt"
```

#### Deployed API:
```bash
curl -X POST https://your-api.koyeb.app/upload-cookies \
  -F "file=@cookies.txt"
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Cookies uploaded successfully!",
  "size": 4567,
  "path": "/tmp/cookies.txt"
}
```

---

### Method 3: Python Script

```python
import requests

api_url = "https://your-api.koyeb.app"

# Upload cookies
with open('cookies.txt', 'rb') as f:
    files = {'file': f}
    response = requests.post(f"{api_url}/upload-cookies", files=files)
    print(response.json())

# Test download
response = requests.get(f"{api_url}/api/download", params={
    'url': 'https://youtube.com/watch?v=xxxxx',
    'quality': 'audio'
})
print(response.json())
```

---

## ✅ Verify කරන්න Cookies Work කරනවද

### 1. Check Status:
```bash
curl https://your-api.koyeb.app/cookies-status
```

**Success Response:**
```json
{
  "status": "loaded",
  "age_hours": "0.2",
  "recommendation": "OK"
}
```

### 2. Test Download:
```bash
curl "https://your-api.koyeb.app/api/download?url=https://youtube.com/watch?v=dQw4w9WgXcQ&quality=audio"
```

**Success:**
```json
{
  "success": true,
  "title": "Rick Astley - Never Gonna Give You Up",
  "download_url": "https://...",
  ...
}
```

**Cookies Issue:**
```json
{
  "error": "COOKIES_REQUIRED",
  "solution": "Upload cookies.txt using POST /upload-cookies"
}
```

---

## 🔄 Cookies Update කරන්න (Regular Maintenance)

Cookies **24 hours** වලින් පමණ expire වෙනවා. Regular update කරන්න ඕන.

### Automatic Check:
```bash
# Cookies status check කරන්න
curl https://your-api.koyeb.app/cookies-status
```

**Response:**
```json
{
  "status": "loaded",
  "age_hours": "26.5",
  "recommendation": "Please update",  // ← Expired!
  "expires_in": "Expired!"
}
```

### Update කරන විදිය:

1. **Browser වල නැවත login** (දැනට login නම් refresh කරන්න)
2. Extension ගෙන් **fresh cookies export** කරන්න
3. **Upload කරන්න** API එකට (same method)
4. **Verify** - test download එකක් කරන්න

---

## 🐛 Common Issues (සාමාන්‍ය ගැටලු)

### ❌ "COOKIES_REQUIRED"

**ගැටලුව:** Cookies upload කරලා නැහැ

**විසඳුම:**
```bash
# Upload කරන්න
curl -X POST https://your-api.koyeb.app/upload-cookies \
  -F "file=@cookies.txt"
```

---

### ❌ "COOKIES_EXPIRED"

**ගැටලුව:** Cookies පරණයි (>24 hours)

**විසඳුම:**
1. Browser වල YouTube refresh කරන්න (login වෙලා තියෙනවද බලන්න)
2. Fresh cookies export කරන්න
3. නැවත upload කරන්න

---

### ❌ "COOKIES_INVALID"

**ගැටලුව:** Cookies හරි format එකෙන් නැහැ

**විසඳුම:**
1. Login වෙලාද export කළේ බලන්න
2. Correct extension එකද use කළේ
3. File එක හරියට save වෙලාද (`cookies.txt`)
4. File open කරලා format එක verify කරන්න

---

### ❌ "Invalid cookies file format"

**ගැටලුව:** File එක Netscape format එකෙන් නැහැ

**විසඳුම:**
1. Extension එකෙන් පමණක් export කරන්න
2. Manual copy-paste කරන්න එපා
3. File එක edit කරන්න එපා

---

## 📱 Postman/Insomnia Use කරන්න

### Postman:
1. New Request → POST
2. URL: `https://your-api.koyeb.app/upload-cookies`
3. Body → form-data
4. Key: `file` (type: File)
5. Value: Select `cookies.txt`
6. Send!

### Insomnia:
1. New Request → POST
2. URL: `https://your-api.koyeb.app/upload-cookies`
3. Body → Multipart Form
4. Add File: `file` → Select `cookies.txt`
5. Send!

---

## 🔐 Security (ආරක්ෂාව)

### Cookies යනු සංවේදී දත්ත!

- ✅ **කාගේවත්** cookies file share කරන්න එපා
- ✅ Public repositories එකට commit කරන්න එපා
- ✅ API server එක **ඔබටම පමණක්** access විය යුතුයි
- ✅ Regular update කරන්න
- ✅ Logout වුණොත් cookies invalid වෙනවා

### Best Practices:

1. **Private API:** API එක public access නැතිව තියන්න (password protect)
2. **HTTPS:** Always HTTPS use කරන්න
3. **Regular Updates:** Daily හෝ අවශ්‍ය වෙලාවට update
4. **Backup:** Old cookies backup කරන්න issue එකක් ආවොත්

---

## 🎯 Complete Workflow

```bash
# 1. Export cookies (දිනකට එක්තරා විටක්)
Browser → youtube.com → Login → Extension → Export

# 2. Upload to API
curl -X POST https://your-api.koyeb.app/upload-cookies \
  -F "file=@cookies.txt"

# 3. Verify
curl https://your-api.koyeb.app/cookies-status

# 4. Test download
curl "https://your-api.koyeb.app/api/download?url=YOUTUBE_URL&quality=audio"

# 5. Success! ✅
```

---

## 📊 Cookies Lifecycle

```
Fresh Cookies (0-12 hours)
  ↓
  ✅ Perfect! API works 100%
  
Still Valid (12-24 hours)
  ↓
  ✅ Works! But consider updating soon
  
Expired (24-48 hours)
  ↓
  ⚠️ May fail. Update recommended!
  
Very Old (>48 hours)
  ↓
  ❌ Will fail! Must update!
```

---

## 💡 Pro Tips

### 1. Multiple Browsers:
```
Chrome cookies → Upload
Firefox cookies → Backup
```

### 2. Automation (Advanced):
```bash
# Script to auto-update cookies daily
#!/bin/bash
# Get fresh cookies from browser
# Upload to API
# Restart API if needed
```

### 3. Monitoring:
```bash
# Check cookies age daily
curl https://your-api.koyeb.app/cookies-status | jq '.age_hours'
```

---

## ✅ සාරාංශය

### Quick Steps:
1. 📥 Install extension
2. 🔐 Login to YouTube
3. 📤 Export cookies
4. ⬆️ Upload to API
5. ✅ Test download

### Maintenance:
- Update **every 24 hours**
- Check status endpoint
- Keep backup cookies

### Security:
- Don't share cookies
- Use HTTPS only
- Private API server

---

**මේ method එක 100% වැඩ කරයි!** 🎉

Cookies upload කළාම bot detection **සම්පූර්ණයෙන්ම bypass** වෙනවා!

---

Made with ❤️ by the community
