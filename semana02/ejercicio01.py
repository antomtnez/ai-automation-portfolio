import requests

class SessionWithTimeout(requests.Session):
    def __init__(self, timeout=5):
        super().__init__()
        self.timeout = timeout

    def request(self, method, url, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        return super().request(method, url, **kwargs)

try:
    s = SessionWithTimeout()
    s.headers.update({'User-Agent':'ai-automation-portfolio/1.0'})

    r = s.get("https://jsonplaceholder.typicode.com/posts")
    r.raise_for_status()

    posts = r.json()
    for post in posts:
        print(f"- [{post['id']}]: {post['title']}")
except requests.exceptions.ConnectionError:
    print("Error: no hay conexión")
except requests.exceptions.Timeout:
    print("Error: timeout")
except requests.exceptions.HTTPError as e:
    print(f"Error HTTP: {e}")