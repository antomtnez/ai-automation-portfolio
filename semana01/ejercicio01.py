import requests

try:
    r = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    timeout = 5,
    params = {'userId' : '3'}   
    )
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

