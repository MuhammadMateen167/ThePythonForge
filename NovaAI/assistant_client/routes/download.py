# smart_download.py
from flask import Blueprint, request, jsonify
import os, requests, mimetypes, re, pathlib, subprocess, tempfile

dl_bp = Blueprint("download", __name__)

# Base save directory
BASE_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "NovaAI")
os.makedirs(BASE_DIR, exist_ok=True)


def safe_filename(name: str) -> str:
    """Remove illegal filename chars."""
    return re.sub(r'[<>:"/\\|?*]+', "_", name)


def run_yt_dlp(url: str, folder: str) -> str:
    try:
        import yt_dlp
    except ImportError:
        return "Error: yt-dlp not installed (pip install yt-dlp)."

    opts = {
        "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "ignoreerrors": True,
        "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best",
        "youtube_include_dash_manifest": False,
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = re.sub(r'[<>:"/\\|?*]+', "_", info.get("title", "video"))
            ext = info.get("ext", "mp4")
            return os.path.join(folder, f"{title}.{ext}")
    except Exception as e:
        return f"Error downloading video: {e}"


def download_file(url: str, folder: str) -> str:
    """Download generic files or images."""
    filename = os.path.basename(url.split("?")[0]) or "download"
    filename = safe_filename(filename)
    local_path = os.path.join(folder, filename)

    try:
        with requests.get(url, stream=True, timeout=20) as r:
            r.raise_for_status()
            content_type = r.headers.get("content-type", "")
            ext = mimetypes.guess_extension(content_type.split(";")[0]) or ""
            if not os.path.splitext(filename)[1] and ext:
                local_path += ext
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_path
    except Exception as e:
        return f"Error downloading file: {e}"


@dl_bp.route("/download", methods=["POST"])
def download_route():
    data = request.get_json() or {}
    url = data.get("url", "").strip()

    if not url or not url.startswith("http"):
        return jsonify({"error": "Invalid or missing URL"}), 400

    # Detect platform
    url_lower = url.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        subdir = "YouTube"
        handler = run_yt_dlp
    elif "tiktok.com" in url_lower:
        subdir = "TikTok"
        handler = run_yt_dlp
    elif "instagram.com" in url_lower:
        subdir = "Instagram"
        handler = run_yt_dlp
    else:
        subdir = "WebFiles"
        handler = download_file

    save_folder = os.path.join(BASE_DIR, subdir)
    os.makedirs(save_folder, exist_ok=True)

    result = handler(url, save_folder)

    # If it’s an error message, return 500
    if isinstance(result, str) and result.lower().startswith("error"):
        return jsonify({"error": result}), 500

    return jsonify(
        {"platform": subdir, "result": f"Downloaded to: {result}", "local_path": result}
    )
