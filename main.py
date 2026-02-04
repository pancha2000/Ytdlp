import os
import re
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL
import time
from typing import Optional

app = FastAPI(
    title="YouTube Download API",
    description="Advanced YouTube video/audio download API with bot detection bypass",
    version="2.0"
)

# CORS එක enable කරනවා
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COOKIES_FILE = 'cookies.txt'

# Rate limiting සඳහා simple in-memory storage
request_tracker = {}

def is_bot_request(request: Request) -> bool:
    """
    Request එක bot එකකින් ආවේද කියලා detect කරනවා
    """
    user_agent = request.headers.get('user-agent', '').lower()
    
    # Common bot user agents
    bot_patterns = [
        'bot', 'crawler', 'spider', 'scraper', 'curl', 'wget',
        'python-requests', 'postman', 'insomnia', 'axios'
    ]
    
    # User agent එක තියේද බලනවා
    if not user_agent:
        return True
    
    # Bot patterns තියේද බලනවා
    for pattern in bot_patterns:
        if pattern in user_agent:
            return True
    
    return False

def check_rate_limit(ip: str, limit: int = 10, window: int = 60) -> bool:
    """
    Rate limiting - එකම IP එකෙන් වැඩියෙන්ම requests එනවද බලනවා
    """
    current_time = time.time()
    
    if ip not in request_tracker:
        request_tracker[ip] = []
    
    # පරණ requests clear කරනවා
    request_tracker[ip] = [
        req_time for req_time in request_tracker[ip]
        if current_time - req_time < window
    ]
    
    # Limit එක exceeded වෙලාද බලනවා
    if len(request_tracker[ip]) >= limit:
        return False
    
    request_tracker[ip].append(current_time)
    return True

def get_ydl_opts(prefer_audio: bool = False, quality: str = 'best'):
    """
    Improved yt-dlp options with multiple fallback strategies
    """
    # Quality based format selection
    if quality == 'audio':
        format_str = 'bestaudio/best'
    elif quality == 'low':
        format_str = 'worst[ext=mp4]/worst'
    elif quality == 'medium':
        format_str = 'bestvideo[height<=720]+bestaudio/best[height<=720]/best'
    else:  # best/high
        format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    
    return {
        'format': format_str,
        'quiet': True,
        'no_warnings': True,
        'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
        
        # වැදගත්: YouTube bot detection මග හරින්න
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web', 'mweb'],
                'skip': ['dash', 'hls'],
            }
        },
        
        # Headers වැඩි දියුණු කරනවා
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        },
        
        'nocheckcertificate': True,
        'geo_bypass': True,
        'age_limit': None,
        
        # Retry logic
        'retries': 3,
        'fragment_retries': 3,
        'skip_unavailable_fragments': True,
    }

def validate_youtube_url(url: str) -> bool:
    """
    URL එක valid YouTube URL එකක්ද බලනවා
    """
    youtube_patterns = [
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/',
        r'(https?://)?(www\.)?youtu\.be/',
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True
    return False

@app.get("/")
async def root():
    """
    API status check කරන endpoint
    """
    return {
        "status": "Running",
        "version": "2.0",
        "endpoints": {
            "download": "/api/download?url=<youtube_url>&quality=<best|medium|low|audio>",
            "info": "/api/info?url=<youtube_url>",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

@app.get("/api/info")
async def get_video_info(url: str, request: Request):
    """
    Video information පමණක් ගන්න endpoint (download link නැතිව)
    """
    # Bot detection
    if is_bot_request(request):
        raise HTTPException(
            status_code=403, 
            detail="Bot requests are not allowed. Please use a valid browser."
        )
    
    # Rate limiting
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=429, 
            detail="Too many requests. Please try again later."
        )
    
    # URL validation
    if not url or not validate_youtube_url(url):
        raise HTTPException(
            status_code=400, 
            detail="Invalid YouTube URL"
        )
    
    ydl_opts = get_ydl_opts()
    ydl_opts['skip_download'] = True
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                "success": True,
                "title": info.get('title'),
                "duration": info.get('duration'),
                "thumbnail": info.get('thumbnail'),
                "uploader": info.get('uploader'),
                "view_count": info.get('view_count'),
                "upload_date": info.get('upload_date'),
                "description": info.get('description', '')[:200] + '...' if info.get('description') else None,
            }
            
    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        
        if "Sign in to confirm you're not a bot" in error_msg or "bot" in error_msg.lower():
            raise HTTPException(
                status_code=403,
                detail="YouTube detected automation. Please update cookies.txt file."
            )
        elif "Video unavailable" in error_msg:
            raise HTTPException(status_code=404, detail="Video not found or unavailable")
        elif "Private video" in error_msg:
            raise HTTPException(status_code=403, detail="This video is private")
        else:
            raise HTTPException(status_code=500, detail=f"Error: {error_msg}")

@app.get("/api/download")
async def download_video(
    url: str, 
    quality: Optional[str] = 'best',
    request: Request = None
):
    """
    YouTube video download link එක ගන්න endpoint
    
    Parameters:
    - url: YouTube video URL
    - quality: best (default), medium, low, audio
    """
    # Bot detection
    if is_bot_request(request):
        raise HTTPException(
            status_code=403, 
            detail="Bot requests are not allowed. Please use a valid browser."
        )
    
    # Rate limiting
    client_ip = request.client.host
    if not check_rate_limit(client_ip, limit=5, window=60):
        raise HTTPException(
            status_code=429, 
            detail="Too many download requests. Please wait a minute."
        )
    
    # URL validation
    if not url or not validate_youtube_url(url):
        raise HTTPException(
            status_code=400, 
            detail="Invalid YouTube URL"
        )
    
    # Quality validation
    valid_qualities = ['best', 'medium', 'low', 'audio']
    if quality not in valid_qualities:
        quality = 'best'
    
    ydl_opts = get_ydl_opts(quality=quality)
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Download URL එක extract කරනවා
            download_url = None
            
            # Method 1: Direct URL තියේද බලනවා
            if 'url' in info:
                download_url = info['url']
            
            # Method 2: Formats array එකෙන් ගන්නවා
            elif 'formats' in info and len(info['formats']) > 0:
                # Best format එක තෝරගන්නවා
                formats = info['formats']
                
                # Audio පමණක් නම්
                if quality == 'audio':
                    audio_formats = [f for f in formats if f.get('acodec') != 'none']
                    if audio_formats:
                        download_url = audio_formats[-1]['url']
                else:
                    # Video formats
                    video_formats = [f for f in formats if f.get('vcodec') != 'none']
                    if video_formats:
                        download_url = video_formats[-1]['url']
                    else:
                        download_url = formats[-1]['url']
            
            # Method 3: requested_formats (merged formats)
            elif 'requested_formats' in info:
                download_url = info['requested_formats'][0]['url']
            
            if not download_url:
                raise Exception("Could not extract download URL")
            
            return {
                "success": True,
                "title": info.get('title'),
                "download_url": download_url,
                "quality": quality,
                "duration": info.get('duration'),
                "thumbnail": info.get('thumbnail'),
                "filesize": info.get('filesize') or info.get('filesize_approx'),
            }
            
    except Exception as e:
        error_msg = str(e)
        print(f"Error log: {error_msg}")
        
        # විවිධ error types හඳුනා ගන්නවා
        if "Sign in to confirm you're not a bot" in error_msg or "bot" in error_msg.lower():
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Bot Detection",
                    "message": "YouTube detected automation. Please update cookies.txt file or try again later.",
                    "solution": "Get fresh cookies from your browser and update cookies.txt"
                }
            )
        elif "format is not available" in error_msg.lower():
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Format Not Available",
                    "message": "The requested format is not available. Trying alternative...",
                    "solution": "Try with quality=medium or quality=audio parameter"
                }
            )
        elif "Video unavailable" in error_msg:
            raise HTTPException(status_code=404, detail="Video not found or unavailable")
        elif "Private video" in error_msg:
            raise HTTPException(status_code=403, detail="This video is private")
        elif "age-restricted" in error_msg.lower():
            raise HTTPException(
                status_code=403,
                detail="This video is age-restricted. Authentication required."
            )
        else:
            raise HTTPException(
                status_code=500, 
                detail={
                    "error": "Server Error",
                    "message": error_msg,
                    "url": url
                }
            )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
