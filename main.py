"""
YouTube Download API - Cookie-free version
No cookies required, uses advanced bypass techniques
"""

import os
import re
import random
import hashlib
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL
import time
from typing import Optional
import subprocess

app = FastAPI(
    title="YouTube Download API - Cookie-Free",
    description="YouTube download API without cookie dependency",
    version="2.2"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache for reducing duplicate requests
download_cache = {}
CACHE_DURATION = 3600  # 1 hour

request_tracker = {}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
]

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
    """Generate cache key"""
    return hashlib.md5(f"{url}:{quality}".encode()).hexdigest()

def get_from_cache(url: str, quality: str):
    """Get from cache if available and not expired"""
    key = get_cache_key(url, quality)
    if key in download_cache:
        data, timestamp = download_cache[key]
        if time.time() - timestamp < CACHE_DURATION:
            print(f"✅ Cache hit for {url}")
            return data
    return None

def save_to_cache(url: str, quality: str, data):
    """Save to cache"""
    key = get_cache_key(url, quality)
    download_cache[key] = (data, time.time())

def get_aggressive_bypass_opts(quality: str = 'best', strategy: int = 0):
    """
    AGGRESSIVE bypass options - NO cookies required
    Uses multiple Android/iOS client spoofing
    """
    user_agent = random.choice(USER_AGENTS)
    
    # Format selection by quality
    format_options = {
        'audio': [
            'bestaudio[ext=m4a]/bestaudio/best',
            '140/bestaudio',
            'bestaudio[acodec=opus]/bestaudio'
        ],
        'low': [
            'worst[height<=360]/worst',
            'best[height<=360]'
        ],
        'medium': [
            'best[height<=720]',
            'bestvideo[height<=720]+bestaudio/best[height<=720]'
        ],
        'best': [
            'best',
            'bestvideo+bestaudio/best',
            'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
        ]
    }
    
    format_str = format_options.get(quality, format_options['best'])[min(strategy, 2)]
    
    # Different client strategies
    client_strategies = [
        ['android', 'android_music'],  # Strategy 0: Android clients
        ['ios', 'mweb'],                # Strategy 1: iOS + mobile web
        ['android_creator', 'ios'],     # Strategy 2: Creator apps
        ['mweb', 'android'],           # Strategy 3: Mobile web fallback
        ['android_testsuite', 'web'],  # Strategy 4: Test clients
    ]
    
    clients = client_strategies[strategy % len(client_strategies)]
    
    opts = {
        'format': format_str,
        'quiet': False,  # Show output for debugging
        'no_warnings': False,
        'ignoreerrors': True,
        
        # NO COOKIES! পूरी तरह बिना cookies के
        'cookiefile': None,
        
        # CRITICAL: Advanced extraction arguments
        'extractor_args': {
            'youtube': {
                'player_client': clients,
                'skip': ['dash', 'hls'],
                # Force specific API endpoints
                'player_skip': ['webpage'],
            }
        },
        
        # Spoof mobile device
        'http_headers': {
            'User-Agent': user_agent,
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': '*/*',
            'Referer': 'https://www.youtube.com/',
            'Origin': 'https://www.youtube.com',
        },
        
        # Network options
        'nocheckcertificate': True,
        'geo_bypass': True,
        'geo_bypass_country': 'US',
        
        # Retry configuration
        'retries': 10,
        'fragment_retries': 10,
        'skip_unavailable_fragments': True,
        'extractor_retries': 5,
        
        # Rate limiting
        'sleep_interval': 1,
        'max_sleep_interval': 3,
        
        # Additional bypass options
        'age_limit': 100,
        'extract_flat': False,
        
        # Force IPv4 (sometimes helps)
        'source_address': '0.0.0.0',
    }
    
    return opts

def extract_with_multiple_strategies(url: str, quality: str = 'best', max_strategies: int = 5):
    """
    Try multiple bypass strategies sequentially
    """
    # Check cache first
    cached = get_from_cache(url, quality)
    if cached:
        return cached
    
    last_error = None
    
    for strategy in range(max_strategies):
        try:
            print(f"\n{'='*60}")
            print(f"🔄 Strategy {strategy + 1}/{max_strategies}")
            print(f"{'='*60}")
            
            opts = get_aggressive_bypass_opts(quality=quality, strategy=strategy)
            
            with YoutubeDL(opts) as ydl:
                print(f"Extracting info from {url}...")
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    print("❌ No info extracted")
                    continue
                
                print(f"✅ Info extracted: {info.get('title', 'Unknown')}")
                
                # Extract download URL
                download_url = None
                
                # Try different methods
                if 'url' in info:
                    download_url = info['url']
                    print(f"✅ Got direct URL")
                
                elif 'formats' in info and info['formats']:
                    formats = info['formats']
                    print(f"📋 Found {len(formats)} formats")
                    
                    if quality == 'audio':
                        # Get best audio
                        audio_formats = [f for f in formats 
                                       if f.get('acodec') != 'none' 
                                       and f.get('url')
                                       and not f.get('vcodec') or f.get('vcodec') == 'none']
                        if audio_formats:
                            best = max(audio_formats, key=lambda x: x.get('abr', 0) or x.get('tbr', 0) or 0)
                            download_url = best['url']
                            print(f"✅ Got audio URL (codec: {best.get('acodec')})")
                    else:
                        # Get best video
                        valid = [f for f in formats if f.get('url')]
                        if valid:
                            download_url = valid[-1]['url']
                            print(f"✅ Got video URL")
                
                elif 'requested_formats' in info:
                    download_url = info['requested_formats'][0]['url']
                    print(f"✅ Got URL from requested_formats")
                
                if download_url:
                    result = {
                        'success': True,
                        'data': info,
                        'download_url': download_url,
                        'strategy': strategy + 1,
                        'cached': False
                    }
                    
                    # Save to cache
                    save_to_cache(url, quality, result)
                    
                    print(f"✅✅ SUCCESS with strategy {strategy + 1}!")
                    return result
                else:
                    print(f"❌ No download URL found in info")
                    
        except Exception as e:
            error_str = str(e)
            last_error = error_str
            print(f"❌ Strategy {strategy + 1} failed: {error_str}")
            
            # If it's a known bot detection error, try next strategy immediately
            if "Sign in to confirm" in error_str or "bot" in error_str.lower():
                print("⚠️ Bot detected, trying next strategy...")
                continue
            
            # For other errors, wait a bit
            if strategy < max_strategies - 1:
                wait = min(2 ** strategy, 10)
                print(f"⏳ Waiting {wait}s...")
                time.sleep(wait)
    
    print(f"\n❌❌ All {max_strategies} strategies failed")
    return {
        'success': False,
        'error': last_error or "All extraction strategies failed",
        'attempted': max_strategies
    }

@app.get("/")
async def root():
    return {
        "status": "Running - Cookie-Free Mode",
        "version": "2.2",
        "mode": "NO_COOKIES_REQUIRED",
        "strategies": 5,
        "features": [
            "Cookie-free operation",
            "5 different bypass strategies",
            "Automatic retry with exponential backoff",
            "Result caching (1 hour)",
            "Mobile client spoofing"
        ]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "mode": "cookie_free",
        "cache_size": len(download_cache)
    }

@app.get("/clear-cache")
async def clear_cache():
    """Clear download cache"""
    size = len(download_cache)
    download_cache.clear()
    return {"cleared": size, "message": f"Cleared {size} cached items"}

@app.get("/api/download")
async def download_video(url: str, quality: str = 'best', request: Request = None):
    """
    Download endpoint - Cookie-free version
    """
    # Rate limiting
    if not check_rate_limit(request.client.host, limit=8, window=60):
        raise HTTPException(429, "Too many requests")
    
    # URL validation
    if not re.match(r'(https?://)?(www\.)?(youtube|youtu)\.(com|be)/', url):
        raise HTTPException(400, "Invalid YouTube URL")
    
    # Quality validation
    if quality not in ['best', 'medium', 'low', 'audio']:
        quality = 'best'
    
    print(f"\n{'='*60}")
    print(f"📥 NEW REQUEST")
    print(f"URL: {url}")
    print(f"Quality: {quality}")
    print(f"{'='*60}")
    
    # Try extraction with multiple strategies
    result = extract_with_multiple_strategies(url, quality, max_strategies=5)
    
    if not result['success']:
        raise HTTPException(
            500,
            detail={
                "error": "All extraction strategies failed",
                "message": result['error'],
                "attempted_strategies": result.get('attempted', 5),
                "solutions": [
                    "1. Try different quality: audio, medium, or low",
                    "2. Wait 2-3 minutes and try again",
                    "3. Try a different video to test",
                    "4. Some videos may be region-locked or require sign-in",
                    "5. Visit /clear-cache to clear cache and retry"
                ]
            }
        )
    
    info = result['data']
    
    return {
        "success": True,
        "title": info.get('title'),
        "download_url": result['download_url'],
        "quality": quality,
        "duration": info.get('duration'),
        "thumbnail": info.get('thumbnail'),
        "strategy_used": result['strategy'],
        "from_cache": result.get('cached', False),
        "note": "Download link expires in ~6 hours"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Cookie-Free YouTube Download API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
