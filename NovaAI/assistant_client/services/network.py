import requests
from config import CLOUD_SERVER_URL

# ---------------------------
# Global backend state
# ---------------------------
BACKEND_URL = CLOUD_SERVER_URL


# ---------------------------
# Backend URL management
# ---------------------------
def set_backend_url(url: str | None):
    """
    Dynamically update the backend URL for this session.
    Called when user changes backend or switches offline.
    """
    global BACKEND_URL
    if url:
        BACKEND_URL = url
    else:
        BACKEND_URL = None


def get_backend_url() -> str | None:
    """Return the currently active backend URL."""
    return BACKEND_URL


# ---------------------------
# Online status check
# ---------------------------
def is_online(url: str | None = None) -> bool:
    """Check if a backend server is reachable."""
    test_url = url or BACKEND_URL
    if not test_url:
        return False

    try:
        r = requests.get(test_url, timeout=2)
        return r.status_code in (200, 404)
    except Exception:
        return False


# ---------------------------
# Send text or data to backend
# ---------------------------
def send_to_cloud(prompt: str):
    """Send a prompt or command to the backend and get the response."""
    if not BACKEND_URL:
        raise ConnectionError("[Offline] No backend server set.")

    try:
        resp = requests.post(f"{BACKEND_URL}/chat", json={"prompt": prompt}, timeout=10)
        if resp.ok:
            data = resp.json()
            return data.get("reply", "(No reply from server)")
        else:
            return f"[Error {resp.status_code}] Server error."
    except Exception as e:
        raise ConnectionError(f"[Offline] Backend unreachable — {e}")
