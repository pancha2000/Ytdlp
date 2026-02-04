# API Documentation - YouTube Download API v2.0

## සම්පූර්ණ API ලියකියවිලි / Complete API Documentation

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [Endpoints](#endpoints)
3. [Error Codes](#error-codes)
4. [Rate Limiting](#rate-limiting)
5. [Bot Detection](#bot-detection)
6. [Examples](#examples)
7. [Best Practices](#best-practices)

---

## Quick Start

### Installation
```bash
# Clone repository
git clone <your-repo-url>
cd youtube-download-api

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

### First Request
```bash
curl "http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&quality=audio" \
  -H "User-Agent: Mozilla/5.0"
```

---

## Endpoints

### 1. Root Endpoint
**GET** `/`

API status එක check කරන්න.

**Response:**
```json
{
  "status": "Running",
  "version": "2.0",
  "endpoints": {
    "download": "/api/download?url=<youtube_url>&quality=<best|medium|low|audio>",
    "info": "/api/info?url=<youtube_url>",
    "health": "/health"
  }
}
```

---

### 2. Health Check
**GET** `/health`

Server එක running ද කියලා check කරන්න.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1706745600.123
}
```

---

### 3. Video Information
**GET** `/api/info`

Video information පමණක් download link නැතිව.

**Parameters:**
- `url` (required): YouTube video URL

**Headers:**
- `User-Agent`: Valid browser user agent (required)

**Example:**
```bash
curl "http://localhost:8000/api/info?url=https://www.youtube.com/watch?v=VIDEO_ID" \
  -H "User-Agent: Mozilla/5.0"
```

**Success Response (200):**
```json
{
  "success": true,
  "title": "Video Title Here",
  "duration": 240,
  "thumbnail": "https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg",
  "uploader": "Channel Name",
  "view_count": 1234567,
  "upload_date": "20240101",
  "description": "Video description..."
}
```

**Error Responses:**
- `400`: Invalid URL
- `403`: Bot detected or authentication required
- `404`: Video not found
- `429`: Rate limit exceeded
- `500`: Server error

---

### 4. Download Link
**GET** `/api/download`

Video download link එක generate කරන්න.

**Parameters:**
- `url` (required): YouTube video URL
- `quality` (optional): Video quality
  - `best` (default): හොඳම quality
  - `medium`: 720p quality
  - `low`: අඩු quality (data saver)
  - `audio`: Audio පමණක්

**Headers:**
- `User-Agent`: Valid browser user agent (required)

**Examples:**

Best Quality (Default):
```bash
curl "http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=VIDEO_ID" \
  -H "User-Agent: Mozilla/5.0"
```

Medium Quality (720p):
```bash
curl "http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=VIDEO_ID&quality=medium" \
  -H "User-Agent: Mozilla/5.0"
```

Audio Only:
```bash
curl "http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=VIDEO_ID&quality=audio" \
  -H "User-Agent: Mozilla/5.0"
```

Low Quality (Data Saver):
```bash
curl "http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=VIDEO_ID&quality=low" \
  -H "User-Agent: Mozilla/5.0"
```

**Success Response (200):**
```json
{
  "success": true,
  "title": "Video Title",
  "download_url": "https://rr3---sn-h5q7knee.googlevideo.com/videoplayback?...",
  "quality": "best",
  "duration": 240,
  "thumbnail": "https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg",
  "filesize": 15728640
}
```

**Error Responses:**
- `400`: Invalid URL or parameters
- `403`: Bot detected, format unavailable, or authentication required
- `404`: Video not found
- `429`: Rate limit exceeded
- `500`: Server error

---

## Error Codes

### 400 - Bad Request
Invalid URL හෝ parameters.

**Example:**
```json
{
  "detail": "Invalid YouTube URL"
}
```

**විසඳුම:**
- Valid YouTube URL එකක් use කරන්න
- URL encode කරන්න special characters

---

### 403 - Forbidden

#### Bot Detection
```json
{
  "error": "Bot Detection",
  "message": "YouTube detected automation. Please update cookies.txt file or try again later.",
  "solution": "Get fresh cookies from your browser and update cookies.txt"
}
```

**විසඳුම:**
1. Valid User-Agent header එකක් add කරන්න
2. Browser cookies export කරලා `cookies.txt` update කරන්න
3. Different IP එකකින් try කරන්න

#### Format Not Available
```json
{
  "error": "Format Not Available",
  "message": "The requested format is not available. Trying alternative...",
  "solution": "Try with quality=medium or quality=audio parameter"
}
```

**විසඳුම:**
Different quality parameter try කරන්න:
- `quality=medium` (720p)
- `quality=audio` (audio only)
- `quality=low` (data saver)

#### Age-Restricted Content
```json
{
  "detail": "This video is age-restricted. Authentication required."
}
```

**විසඳුම:**
Authenticated cookies.txt file එකක් use කරන්න.

---

### 404 - Not Found
Video unavailable හෝ deleted.

```json
{
  "detail": "Video not found or unavailable"
}
```

---

### 429 - Too Many Requests
Rate limit exceeded.

```json
{
  "detail": "Too many download requests. Please wait a minute."
}
```

**විසඳුම:**
1 minute wait කරලා retry කරන්න.

**Current Limits:**
- Info endpoint: 10 requests/minute per IP
- Download endpoint: 5 requests/minute per IP

---

### 500 - Server Error
Internal server error.

```json
{
  "error": "Server Error",
  "message": "Detailed error message",
  "url": "https://youtube.com/..."
}
```

---

## Rate Limiting

### How It Works
IP address based rate limiting:
- **Info endpoint**: 10 requests per minute
- **Download endpoint**: 5 requests per minute

### Response Headers
```
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 3
X-RateLimit-Reset: 1706745660
```

### Best Practices
1. Cache video information
2. Implement exponential backoff
3. Use download endpoint only when needed
4. Monitor rate limit headers

---

## Bot Detection

### What Gets Detected
- Missing User-Agent header
- Bot-like User-Agents (curl, wget, python-requests)
- Suspicious request patterns
- High request frequency

### How to Avoid Detection

#### 1. Valid User-Agent
Always include browser user-agent:
```bash
-H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

#### 2. Realistic Headers
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.youtube.com/',
}
```

#### 3. Rate Limiting
Don't send requests too quickly:
```python
import time
time.sleep(2)  # Wait between requests
```

#### 4. Fresh Cookies
Update cookies.txt regularly:
```bash
# Get from browser using extension
# Replace cookies.txt file
```

---

## Examples

### Python
```python
import requests

def download_youtube_video(url, quality='best'):
    api_url = "http://localhost:8000/api/download"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    params = {
        'url': url,
        'quality': quality
    }
    
    response = requests.get(api_url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Title: {data['title']}")
        print(f"Download: {data['download_url']}")
        return data
    else:
        print(f"Error: {response.json()}")
        return None

# Usage
download_youtube_video('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'audio')
```

### JavaScript (Node.js)
```javascript
const axios = require('axios');

async function downloadYoutubeVideo(url, quality = 'best') {
    const apiUrl = 'http://localhost:8000/api/download';
    
    try {
        const response = await axios.get(apiUrl, {
            params: { url, quality },
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        });
        
        console.log('Title:', response.data.title);
        console.log('Download:', response.data.download_url);
        return response.data;
    } catch (error) {
        console.error('Error:', error.response.data);
        return null;
    }
}

// Usage
downloadYoutubeVideo('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'audio');
```

### cURL
```bash
# Best quality
curl "http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -H "User-Agent: Mozilla/5.0"

# Audio only
curl "http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&quality=audio" \
  -H "User-Agent: Mozilla/5.0"

# Medium quality
curl "http://localhost:8000/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&quality=medium" \
  -H "User-Agent: Mozilla/5.0"
```

### PHP
```php
<?php
function downloadYoutubeVideo($url, $quality = 'best') {
    $apiUrl = 'http://localhost:8000/api/download';
    
    $params = http_build_query([
        'url' => $url,
        'quality' => $quality
    ]);
    
    $options = [
        'http' => [
            'header' => "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\n",
            'method' => 'GET'
        ]
    ];
    
    $context = stream_context_create($options);
    $result = file_get_contents($apiUrl . '?' . $params, false, $context);
    
    return json_decode($result, true);
}

// Usage
$data = downloadYoutubeVideo('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'audio');
print_r($data);
?>
```

---

## Best Practices

### 1. Error Handling
```python
def safe_download(url):
    try:
        response = requests.get(api_url, params={'url': url}, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            # Bot detected - update cookies
            print("Please update cookies.txt")
        elif e.response.status_code == 429:
            # Rate limit - wait and retry
            time.sleep(60)
            return safe_download(url)
        else:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

### 2. Caching
```python
import hashlib
import json
import time

cache = {}

def get_video_info_cached(url, cache_time=3600):
    cache_key = hashlib.md5(url.encode()).hexdigest()
    
    if cache_key in cache:
        data, timestamp = cache[cache_key]
        if time.time() - timestamp < cache_time:
            return data
    
    # Fetch fresh data
    data = get_video_info(url)
    cache[cache_key] = (data, time.time())
    return data
```

### 3. Retry Logic
```python
import time
from functools import wraps

def retry(max_attempts=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (attempt + 1))
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def download_with_retry(url):
    return download_youtube_video(url)
```

### 4. Quality Selection Strategy
```python
def smart_quality_selection(url):
    """
    Video information බලලා best quality එක තෝරගන්නවා
    """
    info = get_video_info(url)
    duration = info['duration']
    
    if duration > 3600:  # 1 hour+
        return 'medium'  # Large files වලට medium
    elif duration > 600:  # 10+ minutes
        return 'best'
    else:
        return 'best'
```

---

## Security Considerations

### 1. Input Validation
- URL validation enabled
- Only YouTube URLs accepted
- Parameter sanitization

### 2. Rate Limiting
- IP-based limiting
- Configurable thresholds
- Automatic blocking

### 3. Bot Detection
- User-agent validation
- Request pattern analysis
- Header verification

### 4. Cookie Security
- Store cookies.txt securely
- Don't commit to git
- Regular updates
- Use environment variables for sensitive data

---

## Troubleshooting

### Problem: All requests return 403
**විසඳුම:**
1. Check User-Agent header
2. Update cookies.txt
3. Try different quality parameter

### Problem: Slow response times
**විසඳුම:**
1. Use info endpoint first for metadata
2. Cache results
3. Choose appropriate quality

### Problem: Download links expire quickly
**විසඳුම:**
Download links expire after ~6 hours. Generate fresh links when needed.

### Problem: Rate limit hit too quickly
**විසඳුම:**
1. Implement caching
2. Reduce request frequency
3. Use info endpoint for metadata only

---

## Support

For issues and questions:
1. Check this documentation
2. Review error messages carefully
3. Update yt-dlp: `pip install --upgrade yt-dlp`
4. Verify cookies.txt is fresh
5. Check API logs

---

## Changelog

### v2.0 (Current)
- ✅ Improved bot detection bypass
- ✅ Multiple quality options
- ✅ Better error handling
- ✅ Rate limiting
- ✅ CORS support
- ✅ Multiple format fallbacks
- ✅ Comprehensive documentation

### v1.0
- Basic download functionality
- Simple error handling

---

**Made with ❤️ for bypassing YouTube bot detection**
