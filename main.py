from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ytmusicapi import YTMusic
import yt_dlp

app = FastAPI()

# Allow our frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ytmusicapi (works without login for basic search)
yt = YTMusic()

@app.get("/search")
def search_music(query: str):
    """Search YouTube Music for songs and return clean metadata."""
    results = yt.search(query, filter="songs", limit=6)
    
    # Format the results to be clean and easy for the frontend to use
    formatted_results = []
    for r in results:
        formatted_results.append({
            "videoId": r["videoId"],
            "title": r["title"],
            "artist": r["artists"][0]["name"] if r.get("artists") else "Unknown Artist",
            "thumbnail": r["thumbnails"][-1]["url"] # Get the highest quality thumbnail
        })
    return formatted_results

@app.get("/stream")
def get_stream_url(videoId: str):
    """Use yt-dlp to extract the direct, playable audio URL."""
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract info without downloading the file
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={videoId}", download=False)
        return {"url": info["url"], "title": info["title"]}