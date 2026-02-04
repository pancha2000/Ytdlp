# YouTube Download API - ඉක්මන් ආරම්භක මාර්ගෝපදේශය 🚀

## ප්‍රධාන වෙනස්කම් (What's Fixed)

### ✅ පරණ ගැටලු විසඳුණු:
1. **"Requested format is not available" Error** - FIXED!
   - Multiple format fallback එකක් add කරලා
   - Different player clients use කරනවා (android, ios, web)
   - Quality options add කරලා (best, medium, low, audio)

2. **Bot Detection Error (403)** - FIXED!
   - Improved user-agent handling
   - Better HTTP headers
   - Request validation
   - Rate limiting system

3. **Better Error Messages** - IMPROVED!
   - Clear error messages Sinhala & English
   - Solutions එක්ක එකට error එනවා
   - Detailed error types

---

## ඉක්මන් ස්ථාපනය (Quick Installation)

### 1. Download කරලා Extract කරන්න
```bash
# Download කරපු zip එක extract කරන්න
unzip youtube-download-api-v2.zip
cd youtube-download-api-v2
```

### 2. Dependencies Install කරන්න
```bash
pip install -r requirements.txt
```

### 3. Run කරන්න
```bash
python main.py
```

Server එක run වෙයි http://localhost:8000 වල!

---

## භාවිතය (Quick Usage)

### වෙබ් බ්‍රව්සරයෙන් Test කරන්න:

#### Audio Download කරන්න:
```
http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&quality=audio
```

#### Best Quality Video:
```
http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&quality=best
```

#### Medium Quality (720p):
```
http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&quality=medium
```

---

## ප්‍රධාන Features

### 1️⃣ Quality Options
- `quality=best` - හොඳම quality (default)
- `quality=medium` - 720p
- `quality=low` - Data saving mode
- `quality=audio` - MP3/Audio පමණක්

### 2️⃣ Bot Detection Prevention
- Automatic user-agent rotation
- Multiple player client support
- Smart request handling

### 3️⃣ Rate Limiting
- 5 downloads per minute (එකම IP එකට)
- 10 info requests per minute
- Automatic blocking on abuse

### 4️⃣ Better Error Handling
සෑම error එකක්ම clear message එකක් සහ solution එකක් එක්ක එනවා:

```json
{
  "error": "Bot Detection",
  "message": "YouTube detected automation...",
  "solution": "Get fresh cookies from your browser..."
}
```

---

## Python Script Example

```python
import requests

def download_song(youtube_url):
    api_url = "http://localhost:8000/api/download"
    
    # IMPORTANT: User-Agent header එක අනිවාර්යයි!
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    params = {
        'url': youtube_url,
        'quality': 'audio'  # Audio පමණක් download කරන්න
    }
    
    response = requests.get(api_url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Title: {data['title']}")
        print(f"📥 Download: {data['download_url']}")
        return data['download_url']
    else:
        print(f"❌ Error: {response.json()}")
        return None

# භාවිතය
download_song('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
```

---

## Errors සහ විසඳුම් (Common Errors)

### ❌ Error: "Bot requests are not allowed"
**ගැටලුව:** User-Agent header එක නැහැ

**විසඳුම:**
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
requests.get(url, headers=headers)
```

---

### ❌ Error: "YouTube detected automation"
**ගැටලුව:** YouTube බොට් කියලා detect කරනවා

**විසඳුම:**
1. Browser එකෙන් YouTube login වෙන්න
2. "Get cookies.txt" extension install කරන්න
3. Cookies export කරලා `cookies.txt` file එකට paste කරන්න

Chrome Extension: https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid

---

### ❌ Error: "Format is not available"
**ගැටලුව:** Request කරපු format එක නැහැ

**විසඳුම:**
Different quality එකක් try කරන්න:
```
# Best වෙනුවට medium try කරන්න
quality=medium

# හෝ audio පමණක්
quality=audio
```

---

### ❌ Error: "Too many requests"
**ගැටලුව:** වැඩියෙන්ම requests යැව්වා

**විසඳුම:**
1 minute wait කරලා retry කරන්න.

---

## Advanced Usage

### 1. Docker එකෙන් Run කරන්න
```bash
# Build image
docker build -t youtube-api .

# Run container
docker run -p 8000:8000 youtube-api
```

හෝ Docker Compose:
```bash
docker-compose up
```

### 2. Deploy කරන්න

#### Render.com:
1. GitHub repo එකක් හදන්න
2. Render.com වල connect කරන්න
3. `render.yaml` automatic detect කරයි
4. Deploy!

#### Railway:
```bash
railway up
```

#### Vercel:
```bash
vercel deploy
```

---

## Test කරන්න

Test script එක run කරන්න:
```bash
python test_api.py
```

මෙය සියලුම endpoints test කරයි:
- ✅ Health check
- ✅ Video info
- ✅ Download (all qualities)
- ✅ Bot detection
- ✅ Rate limiting
- ✅ Error handling

---

## Configuration

### Rate Limits වෙනස් කරන්න
`main.py` file එකේ:
```python
# Download endpoint
check_rate_limit(client_ip, limit=5, window=60)
# මේක වෙනස් කරන්න පුළුවන් (උදා: limit=10)
```

### CORS Settings
`main.py` file එකේ:
```python
allow_origins=["*"]  # සියලු domains
# හෝ
allow_origins=["https://yourdomain.com"]  # විශේෂිත domain එකක්
```

---

## Files සහ Folders

```
youtube-download-api-v2/
├── main.py                  # Main API code
├── requirements.txt         # Python dependencies
├── README.md               # Full documentation (English + Sinhala)
├── API_DOCUMENTATION.md    # Detailed API docs
├── QUICK_START_SINHALA.md  # මේ file එක
├── test_api.py             # Testing script
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose
├── cookies.txt.example     # Cookie template
├── .gitignore              # Git ignore rules
├── Procfile                # Heroku deployment
├── render.yaml             # Render.com deployment
├── railway.json            # Railway deployment
├── vercel.json             # Vercel deployment
└── LICENSE                 # MIT License
```

---

## වැදගත් සටහන් (Important Notes)

### 1. User-Agent Header අනිවාර්යයි!
සෑම request එකටම User-Agent header එක add කරන්න ඕන.

### 2. Cookies File (Optional but Recommended)
- Bot detection වළක්වන්න cookies use කරන්න
- Regular update කරන්න (expire වෙනවා)
- Private data නිසා git වලට commit කරන්න එපා

### 3. Rate Limits
- Abuse වළක්වන්න rate limits තියෙනවා
- Caching use කරන්න හැකි තැන්වල
- Responsible usage!

### 4. Download Links Expire
- Download links 6 hours වලින් පමණ expire වෙනවා
- Fresh links generate කරන්න ඕන download කරන වෙලාවේ

---

## Support & Help

### ගැටලු ඇත්නම්:
1. ✅ README.md file එක කියවන්න
2. ✅ API_DOCUMENTATION.md full docs බලන්න
3. ✅ Error message එක හොඳින් කියවන්න (solution එක තියෙනවා)
4. ✅ Cookies update කරලා බලන්න
5. ✅ yt-dlp update කරන්න: `pip install --upgrade yt-dlp`

### Testing:
```bash
# Health check
curl http://localhost:8000/health

# Info endpoint
curl "http://localhost:8000/api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -H "User-Agent: Mozilla/5.0"

# Download
curl "http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&quality=audio" \
  -H "User-Agent: Mozilla/5.0"
```

---

## වැඩිදුර මාර්ගෝපදේශ

සම්පූර්ණ documentation:
- 📖 **README.md** - සම්පූර්ණ මාර්ගෝපදේශය
- 📚 **API_DOCUMENTATION.md** - Detailed API reference
- 🧪 **test_api.py** - සියලුම features test කරන්න

---

## ස්තූතියි! 🙏

YouTube bot detection bypass කරන්න help කරපු ප්‍රජාවට ස්තූතියි!

**Made with ❤️ by the community**

---

## Quick Links

- GitHub Issues: [Report problems]
- API Docs: `API_DOCUMENTATION.md`
- Full README: `README.md`
- Test Script: `python test_api.py`

---

**සතුටින් භාවිතා කරන්න! Happy downloading! 🎵🎬**
