# music.py
import asyncio
import os
import tempfile
import logging
from pathlib import Path
import yt_dlp

logger = logging.getLogger(__name__)

# ── Пошук ─────────────────────────────────────────────────────────────────────
def _fmt_duration(secs) -> str:
    if not secs:
        return "—"
    m, s = divmod(int(secs), 60)
    return f"{m}:{s:02d}"


def search_youtube(query: str, limit: int = 10) -> list[dict]:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)

    tracks = []
    for entry in (results.get("entries") or []):
        if not entry:
            continue
        duration = entry.get("duration", 0)
        if duration and duration > 900:
            continue
        tracks.append({
            "title":    entry.get("title", "Unknown"),
            "url":      f"https://www.youtube.com/watch?v={entry['id']}",
            "id":       entry["id"],
            "duration": _fmt_duration(duration),
            "channel":  entry.get("channel") or entry.get("uploader") or "—",
        })
    return tracks


def search_soundcloud(query: str, limit: int = 5) -> list[dict]:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(
                f"scsearch{limit}:{query}", download=False
            )
        except Exception:
            return []

    tracks = []
    for entry in (results.get("entries") or []):
        if not entry:
            continue
        tracks.append({
            "title":    entry.get("title", "Unknown"),
            "url":      entry.get("webpage_url") or entry.get("url", ""),
            "id":       entry.get("id", ""),
            "duration": _fmt_duration(entry.get("duration", 0)),
            "channel":  entry.get("uploader") or "SoundCloud",
            "source":   "soundcloud",
        })
    return tracks


def search_all(query: str, limit: int = 10) -> list[dict]:
    """Шукає по всіх джерелах і об'єднує результати."""
    yt = search_youtube(query, limit=limit)
    sc = search_soundcloud(query, limit=5)

    # Позначаємо джерело
    for t in yt:
        t.setdefault("source", "youtube")
    for t in sc:
        t.setdefault("source", "soundcloud")

    # Об'єднуємо: спочатку YouTube, потім SoundCloud
    combined = yt + sc
    return combined[:limit + 5]


def get_artist_songs(artist: str, limit: int = 50) -> list[dict]:
    return search_youtube(f"{artist} official audio", limit=limit)


def get_top_100() -> list[dict]:
    """Топ 100 з YouTube Music charts."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "playlistend": 100,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(
                "https://www.youtube.com/playlist?list=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI",
                download=False
            )
        tracks = []
        for i, entry in enumerate(results.get("entries") or []):
            if not entry:
                continue
            tracks.append({
                "title":    entry.get("title", "Unknown"),
                "url":      f"https://www.youtube.com/watch?v={entry['id']}",
                "id":       entry["id"],
                "duration": _fmt_duration(entry.get("duration", 0)),
                "channel":  entry.get("channel") or "—",
                "rank":     i + 1,
                "source":   "youtube",
            })
        return tracks[:100]
    except Exception as e:
        logger.error(f"Top 100 error: {e}")
        # Fallback — звичайний пошук
        return search_youtube("top hits 2024", limit=100)


# ── Завантаження ──────────────────────────────────────────────────────────────
def download_audio(video_url: str, out_dir: str, quality: str = "192") -> str | None:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(out_dir, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": quality,
        }],
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(video_url, download=True)

    for f in Path(out_dir).glob("*.mp3"):
        return str(f)
    return None


async def download_audio_async(video_url: str, out_dir: str, quality: str = "192") -> str | None:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, download_audio, video_url, out_dir, quality)


async def search_all_async(query: str, limit: int = 10) -> list[dict]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, search_all, query, limit)


async def get_artist_songs_async(artist: str, limit: int = 50) -> list[dict]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_artist_songs, artist, limit)


async def get_top_100_async() -> list[dict]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_top_100)
          
