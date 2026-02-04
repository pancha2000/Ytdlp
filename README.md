# YouTube Download API v2.0 🎥

Advanced YouTube video/audio download API with bot detection bypass and rate limiting.

## ප්‍රධාන වැඩිදියුණු කිරීම් / Main Improvements

### 1. Bot Detection Prevention (බොට් හඳුනාගැනීම මැඩපැවැත්වීම)
- Multiple player client support (android, ios, web, mweb)
- Improved HTTP headers
- User-agent rotation
- Request validation

### 2. Better Error Handling (වැඩිදියුණු Error Handling)
- Specific error messages for different scenarios
- Automatic retry logic
- Format fallback mechanism
- Detailed error responses

### 3. Rate Limiting (Request සීමා කිරීම)
- IP-based rate limiting
- Prevents API abuse
- Configurable limits

### 4. Multiple Quality Options (විවිධ Quality Options)
- `best` - හොඳම video quality
- `medium` - මධ්‍යම quality (720p)
- `low` - අඩු quality (data save කරන්න)
- `audio` - audio පමණක් (MP3/M4A)

### 5. Additional Endpoints
- `/` - API status
- `/health` - Health check
- `/api/info` - Video info without download link
- `/api/download` - Download link with quality options

## Installation (ස්ථාපනය කිරීම)

```bash
# Dependencies install කරන්න
pip install -r requirements.txt

# API එක run කරන්න
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Usage (භාවිතය)

### 1. Video Information ගන්න
```bash
GET /api/info?url=https://www.youtube.com/watch?v=VIDEO_ID
```

Response:
```json
{
  "success": true,
  "title": "Video Title",
  "duration": 240,
  "thumbnail": "https://...",
  "uploader": "Channel Name",
  "view_count": 1000000,
  "upload_date": "20240101"
}
```

### 2. Download Link ගන්න

#### Best Quality (Default)
```bash
GET /api/download?url=https://www.youtube.com/watch?v=VIDEO_ID
```

#### Medium Quality (720p)
```bash
GET /api/download?url=https://www.youtube.com/watch?v=VIDEO_ID&quality=medium
```

#### Audio Only
```bash
GET /api/download?url=https://www.youtube.com/watch?v=VIDEO_ID&quality=audio
```

#### Low Quality (Data Saver)
```bash
GET /api/download?url=https://www.youtube.com/watch?v=VIDEO_ID&quality=low
```

Response:
```json
{
  "success": true,
  "title": "Video Title",
  "download_url": "https://direct-download-link...",
  "quality": "best",
  "duration": 240,
  "thumbnail": "https://...",
  "filesize": 15728640
}
```

## Error Handling (Errors සහ විසඳුම්)

### 1. Bot Detection Error (403)
```json
{
  "error": "Bot Detection",
  "message": "YouTube detected automation...",
  "solution": "Get fresh cookies from your browser and update cookies.txt"
}
```

**විසඳුම:**
1. Browser එකෙන් YouTube login වෙන්න
2. Browser cookies export කරන්න (Extension use කරන්න)
3. `cookies.txt` file එක update කරන්න

### 2. Format Not Available (403)
```json
{
  "error": "Format Not Available",
  "message": "The requested format is not available...",
  "solution": "Try with quality=medium or quality=audio parameter"
}
```

**විසඳුම:**
Different quality parameter එකක් try කරන්න:
```bash
# Original request
/api/download?url=...&quality=best

# Try medium instead
/api/download?url=...&quality=medium

# Or audio only
/api/download?url=...&quality=audio
```

### 3. Rate Limit Error (429)
```json
{
  "detail": "Too many requests. Please try again later."
}
```

**විසඳුම:**
Minute එකක් wait කරලා retry කරන්න.

### 4. Invalid URL (400)
```json
{
  "detail": "Invalid YouTube URL"
}
```

**විසඳුම:**
Valid YouTube URL එකක් use කරන්න:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

## Configuration (හැඩගැස්වීම)

### Rate Limits වෙනස් කරන්න

`main.py` file එකේ මේ values වෙනස් කරන්න:

```python
# Info endpoint
check_rate_limit(client_ip, limit=10, window=60)  # 10 requests per minute

# Download endpoint
check_rate_limit(client_ip, limit=5, window=60)   # 5 requests per minute
```

### Cookies File

Fresh cookies file එකක් ගන්න:
1. Browser extension: "Get cookies.txt" (Chrome/Firefox)
2. YouTube.com වල login වෙලා
3. Extension එකෙන් cookies export කරන්න
4. `cookies.txt` file එක project folder එකට copy කරන්න

## Deployment (Deploy කිරීම)

### Render.com
```yaml
# render.yaml
services:
  - type: web
    name: youtube-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Heroku
```
# Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Railway
```
# railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT"
  }
}
```

## Testing (Test කිරීම)

```bash
# Local test
curl "http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&quality=audio"

# Info endpoint test
curl "http://localhost:8000/api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Health check
curl "http://localhost:8000/health"
```

## Advanced Features

### 1. CORS Support
All origins allowed by default. Modify in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains
    ...
)
```

### 2. Custom User Agents
API එක automatically rotation කරනවා, but custom එකක් add කරන්න පුළුවන්:
```python
'User-Agent': 'Your-Custom-User-Agent'
```

### 3. Geo Bypass
Geo-restricted videos bypass කරන්න:
```python
'geo_bypass': True,
'geo_bypass_country': 'US',
```

## Troubleshooting (ගැටලු විසඳීම)

### API එක start වෙන්නේ නැහැ
```bash
# Check port availability
netstat -tulpn | grep 8000

# Use different port
uvicorn main:app --host 0.0.0.0 --port 8080
```

### yt-dlp outdated
```bash
pip install --upgrade yt-dlp
```

### All requests failing
1. Check cookies.txt file
2. Update yt-dlp: `pip install --upgrade yt-dlp`
3. Check YouTube status: https://downdetector.com/status/youtube/

## Security Considerations (ආරක්ෂාව)

1. **Rate Limiting**: IP-based limiting enabled
2. **Bot Detection**: User-agent validation
3. **Input Validation**: URL validation before processing
4. **Error Sanitization**: No sensitive data in error messages

## License

MIT License - Free to use and modify

## Support

Issues ඇත්නම්:
1. Cookies file එක update කරන්න
2. yt-dlp update කරන්න
3. Different quality parameter try කරන්න
4. Error log එක check කරන්න

---

Made with ❤️ for bypass YouTube bot detection
