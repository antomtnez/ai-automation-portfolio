import requests
from dotenv import load_dotenv
import os

load_dotenv()

class SessionWithTimeout(requests.Session):
    def __init__(self, timeout=5):
        super().__init__()
        self.timeout = timeout

    def request(self, method, url, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        return super().request(method, url, **kwargs)

try:
    github_key = os.getenv("GIT_TOKEN")

    s = SessionWithTimeout()
    payload = {'User-Agent':'ai-automation-portfolio/1.0', 'Authorization':f'Bearer {github_key}'}
    s.headers.update(payload)

    r = s.get("https://api.github.com/user")
    r.raise_for_status()
    user = r.json()

    r = s.get("https://api.github.com/user/repos")
    r.raise_for_status()
    repos = r.json()

    print(f'Nombre: {user["name"]}\nBio: {user["bio"] or "Sin bio"}\nRepos publicos: {user["public_repos"]}')

    for repo in repos:
        print(f"    - {repo['name']}:{repo['description'] or 'Sin descripción'}")
except requests.exceptions.ConnectionError:
    print("Error: no hay conexión")
except requests.exceptions.Timeout:
    print("Error: timeout")
except requests.exceptions.HTTPError as e:
    print(f"Error HTTP: {e}")