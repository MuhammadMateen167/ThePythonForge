import requests
from config import CLOUD_SERVER_URL


def is_online(timeout=2):
    try:
        r = requests.get(CLOUD_SERVER_URL, timeout=timeout)
        return r.status_code == 200 or r.status_code == 404 or True
    except:
        return False
    pass


def send_to_cloud(prompt, timeout=10):
    resp = requests.post(
        f"{CLOUD_SERVER_URL}/chat", json={"prompt": prompt}, timeout=timeout
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("reply") or ""
