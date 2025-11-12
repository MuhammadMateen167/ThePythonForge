# Google Custom Search wrapper. Requires GOOGLE_API_KEY and GOOGLE_CX environment variables.
# If not set, return an informative message.
import os, requests
API_KEY = os.getenv('GOOGLE_API_KEY','')
CX = os.getenv('GOOGLE_CX','')

def google_search(q, num=5):
    if not API_KEY or not CX:
        return [{'title':'API keys not configured','link':'', 'snippet':'Set GOOGLE_API_KEY and GOOGLE_CX on the server to enable searches.'}]
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {'q': q, 'key': API_KEY, 'cx': CX, 'num': num}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    items = data.get('items',[])
    results = []
    for it in items:
        results.append({'title': it.get('title'), 'link': it.get('link'), 'snippet': it.get('snippet')})
    return results
