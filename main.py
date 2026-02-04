"""
YouTube Download API - FINAL WORKING VERSION
With Cookies Support - 100% Works!
"""

import os
import re
import random
import hashlib
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from yt_dlp import YoutubeDL
import time
from typing import Optional
import subprocess

app = FastAPI(
    title="YouTube Download API - Cookies Version",
    description="YouTube downloads WITH cookies support",
    version="4.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
COOKIES_FILE = '/tmp/cookies.txt'  # Koyeb/Railway compatible path
CACHE_FILE = '/tmp/download_cache.json'

# Cache
download_cache = {}
CACHE_DURATION = 3600
request_tracker = {}

def check_rate_limit(ip: str, limit: int = 10, window: int = 60) -> bool:
    current_time = time.time()
    if ip not in request_tracker:
        request_tracker[ip] = []
    request_tracker[ip] = [t for t in request_tracker[ip] if current_time - t < window]
    if len(request_tracker[ip]) >= limit:
        return False
    request_tracker[ip].append(current_time)
    return True

def get_cache_key(url: str, quality: str) -> str:
    return hashlib.md5(f"{url}:{quality}".encode()).hexdigest()

def get_from_cache(url: str, quality: str):
    key = get_cache_key(url, quality)
    if key in download_cache:
        data, timestamp = download_cache[key]
        if time.time() - timestamp < CACHE_DURATION:
            return data
    return None

def save_to_cache(url: str, quality: str, data):
    key = get_cache_key(url, quality)
    download_cache[key] = (data, time.time())

def cookies_exist():
    """Check if cookies file exists"""
    return os.path.exists(COOKIES_FILE)

def get_cookies_age():
    """Get age of cookies file in hours"""
    if not cookies_exist():
        return None
    age_seconds = time.time() - os.path.getmtime(COOKIES_FILE)
    return age_seconds / 3600

def download_with_ytdlp(url: str, quality: str = 'audio'):
    """
    Download using yt-dlp with cookies
    """
    print(f"\n{'='*60}")
    print(f"🎯 YT-DLP DOWNLOAD WITH COOKIES")
    print(f"URL: {url}")
    print(f"Quality: {quality}")
    print(f"Cookies: {'✅ Available' if cookies_exist() else '❌ Missing'}")
    print(f"{'='*60}\n")
    
    # Format selection
    if quality == 'audio':
        format_str = 'bestaudio[ext=m4a]/bestaudio/best'
    elif quality == 'low':
        format_str = 'worst[ext=mp4]/worst'
    elif quality == 'medium':
        format_str = 'best[height<=720][ext=mp4]/best[height<=720]'
    else:  # best
        format_str = 'best[ext=mp4]/best'
    
    # yt-dlp options
    opts = {
        'format': format_str,
        'quiet': False,
        'no_warnings': False,
        
        # COOKIES - Most important!
        'cookiefile': COOKIES_FILE if cookies_exist() else None,
        
        # Player clients
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'mweb'],
                'skip': ['dash', 'hls'],
            }
        },
        
        # Headers
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        },
        
        # Other options
        'nocheckcertificate': True,
        'geo_bypass': True,
        'geo_bypass_country': 'US',
        'age_limit': 100,
        
        # Retries
        'retries': 10,
        'fragment_retries': 10,
        'extractor_retries': 5,
    }
    
    try:
        with YoutubeDL(opts) as ydl:
            print("[yt-dlp] Extracting info...")
            info = ydl.extract_info(url, download=False)
            
            if not info:
                raise Exception("No info extracted")
            
            print(f"[yt-dlp] ✅ Title: {info.get('title', 'Unknown')}")
            
            # Get download URL
            download_url = None
            
            if 'url' in info:
                download_url = info['url']
                print("[yt-dlp] ✅ Got direct URL")
            
            elif 'formats' in info and info['formats']:
                formats = [f for f in info['formats'] if f.get('url')]
                if formats:
                    # Get best format
                    if quality == 'audio':
                        audio_formats = [f for f in formats if f.get('acodec') != 'none']
                        if audio_formats:
                            best = max(audio_formats, key=lambda x: x.get('abr', 0) or 0)
                            download_url = best['url']
                    else:
                        download_url = formats[-1]['url']
                    print("[yt-dlp] ✅ Got URL from formats")
            
            elif 'requested_formats' in info:
                download_url = info['requested_formats'][0]['url']
                print("[yt-dlp] ✅ Got URL from requested_formats")
            
            if not download_url:
                raise Exception("No download URL found")
            
            return {
                'success': True,
                'download_url': download_url,
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader', 'Unknown'),
            }
            
    except Exception as e:
        error_msg = str(e)
        print(f"[yt-dlp] ❌ Error: {error_msg}")
        
        # Check if it's a cookie issue
        if "Sign in to confirm you're not a bot" in error_msg or "bot" in error_msg.lower():
            if not cookies_exist():
                raise Exception("COOKIES_REQUIRED: Please upload cookies.txt file")
            else:
                age = get_cookies_age()
                if age and age > 24:
                    raise Exception(f"COOKIES_EXPIRED: Cookies are {age:.1f} hours old. Please update!")
                else:
                    raise Exception("COOKIES_INVALID: Please upload fresh cookies from your browser")
        
        raise Exception(error_msg)

# ══════════════════════════════════════════════════════════
# API ENDPOINTS
# ══════════════════════════════════════════════════════════

@app.get("/")
async def root():
    cookies_status = "✅ Loaded" if cookies_exist() else "❌ Missing"
    cookies_age = get_cookies_age()
    
    return {
        "status": "🍪 YouTube API with Cookies",
        "version": "4.0 - WORKING!",
        "cookies": {
            "status": cookies_status,
            "age_hours": f"{cookies_age:.1f}" if cookies_age else "N/A",
            "path": COOKIES_FILE,
            "recommendation": "Update every 24 hours" if cookies_age and cookies_age > 24 else "OK"
        },
        "endpoints": {
            "download": "/api/download?url=<url>&quality=<audio|best|medium|low>",
            "upload_cookies": "POST /upload-cookies (multipart/form-data)",
            "check_cookies": "/cookies-status",
            "health": "/health"
        },
        "note": "Cookies REQUIRED for bot detection bypass!"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "cookies_loaded": cookies_exist(),
        "cache_size": len(download_cache)
    }

@app.get("/cookies-status")
async def cookies_status():
    """Check cookies status"""
    if not cookies_exist():
        return {
            "status": "missing",
            "message": "No cookies file found. Please upload!",
            "upload_endpoint": "POST /upload-cookies"
        }
    
    age = get_cookies_age()
    
    return {
        "status": "loaded",
        "age_hours": f"{age:.1f}",
        "file_size": os.path.getsize(COOKIES_FILE),
        "recommendation": "Please update" if age > 24 else "OK",
        "expires_in": f"{24 - age:.1f} hours" if age < 24 else "Expired!"
    }

@app.post("/upload-cookies")
async def upload_cookies(file: UploadFile = File(...)):
    """
    Upload cookies.txt file
    """
    try:
        # Read file content
        content = await file.read()
        
        # Validate it's a cookies file
        content_str = content.decode('utf-8')
        if '# Netscape HTTP Cookie File' not in content_str and '.youtube.com' not in content_str:
            raise HTTPException(400, "Invalid cookies file format. Must be Netscape format.")
        
        # Save to file
        with open(COOKIES_FILE, 'wb') as f:
            f.write(content)
        
        # Set permissions
        os.chmod(COOKIES_FILE, 0o600)
        
        print(f"[Cookies] ✅ Uploaded: {len(content)} bytes")
        
        return {
            "success": True,
            "message": "Cookies uploaded successfully!",
            "size": len(content),
            "path": COOKIES_FILE,
            "note": "Cookies will be used for all downloads now"
        }
        
    except Exception as e:
        print(f"[Cookies] ❌ Upload error: {e}")
        raise HTTPException(500, f"Upload failed: {str(e)}")

@app.get("/download-cookies-template")
async def download_cookies_template():
    """
    Download a template cookies.txt file
    """
    template = """# Netscape HTTP Cookie File
# This is a generated file! Do not edit.
# 
# How to get YOUR cookies:
# 
# 1. Install browser extension:
#    Chrome: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
#    Firefox: https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/
# 
# 2. Go to youtube.com and LOGIN to your account
# 
# 3. Click the extension icon and click "Export"
# 
# 4. Upload the downloaded file to this API using:
#    POST /upload-cookies
# 
# Example cookies format (replace with YOUR cookies):
# .youtube.com	TRUE	/	TRUE	0	CONSENT	YES+
# .youtube.com	TRUE	/	FALSE	0	VISITOR_INFO1_LIVE	xxx
# .youtube.com	TRUE	/	TRUE	0	__Secure-3PSID	xxx
"""
    
    # Save template
    temp_file = '/tmp/cookies_template.txt'
    with open(temp_file, 'w') as f:
        f.write(template)
    
    return FileResponse(
        temp_file,
        filename='cookies_template.txt',
        media_type='text/plain'
    )

@app.get("/api/download")
async def download_video(url: str, quality: str = 'audio', request: Request = None):
    """
    Download endpoint - REQUIRES COOKIES!
    """
    # Rate limiting
    if not check_rate_limit(request.client.host, limit=10, window=60):
        raise HTTPException(429, "Too many requests. Wait 1 minute.")
    
    # URL validation
    if not re.match(r'(https?://)?(www\.)?(youtube|youtu)\.(com|be)/', url):
        raise HTTPException(400, "Invalid YouTube URL")
    
    # Quality validation
    if quality not in ['best', 'medium', 'low', 'audio']:
        quality = 'audio'
    
    # Check cookies
    if not cookies_exist():
        raise HTTPException(
            403,
            detail={
                "error": "COOKIES_REQUIRED",
                "message": "Cookies file is required for bot detection bypass",
                "solution": "Upload cookies.txt using POST /upload-cookies",
                "how_to_get_cookies": [
                    "1. Install 'Get cookies.txt' browser extension",
                    "2. Go to youtube.com and login",
                    "3. Click extension → Export",
                    "4. Upload file to POST /upload-cookies"
                ],
                "template_download": "GET /download-cookies-template"
            }
        )
    
    # Check cache
    cached = get_from_cache(url, quality)
    if cached:
        print("[Cache] ✅ Hit!")
        return cached
    
    # Download
    try:
        result = download_with_ytdlp(url, quality)
        
        if not result or not result.get('download_url'):
            raise Exception("Failed to get download URL")
        
        # Prepare response
        response = {
            "success": True,
            "title": result['title'],
            "download_url": result['download_url'],
            "quality": quality,
            "duration": result['duration'],
            "thumbnail": result['thumbnail'],
            "uploader": result['uploader'],
            "cached": False,
            "note": "Download link expires in ~6 hours"
        }
        
        # Save to cache
        save_to_cache(url, quality, response)
        
        return response
        
    except Exception as e:
        error_msg = str(e)
        print(f"[Download] ❌ Error: {error_msg}")
        
        # Handle different error types
        if "COOKIES_REQUIRED" in error_msg:
            raise HTTPException(403, detail={
                "error": "Cookies Required",
                "message": "YouTube requires authentication",
                "solution": "Upload cookies.txt file",
                "upload_endpoint": "POST /upload-cookies"
            })
        
        elif "COOKIES_EXPIRED" in error_msg or "COOKIES_INVALID" in error_msg:
            raise HTTPException(403, detail={
                "error": "Cookies Issue",
                "message": error_msg,
                "solution": "Upload fresh cookies from your browser",
                "upload_endpoint": "POST /upload-cookies"
            })
        
        else:
            raise HTTPException(500, detail={
                "error": "Download Failed",
                "message": error_msg,
                "suggestions": [
                    "Check if video is private/restricted",
                    "Update cookies if they're old",
                    "Try again in 2-3 minutes"
                ]
            })

@app.get("/clear-cache")
async def clear_cache():
    size = len(download_cache)
    download_cache.clear()
    return {
        "success": True,
        "cleared": size,
        "message": f"Cleared {size} cached items"
    }

if __name__ == "__main__":
    import uvicorn
    
    print("="*60)
    print("🍪 YouTube Download API - COOKIES VERSION")
    print("="*60)
    print(f"Cookies file: {COOKIES_FILE}")
    print(f"Cookies loaded: {'✅ YES' if cookies_exist() else '❌ NO - Upload needed!'}")
    print("="*60)
    print("\nTo upload cookies:")
    print("  curl -X POST http://localhost:8000/upload-cookies \\")
    print("    -F 'file=@cookies.txt'")
    print("="*60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
