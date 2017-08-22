import http.cookiejar
import urllib.parse
import urllib.request
import json

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

with open('config.json', 'r') as f:
    config = json.load(f)

def login(bid):
    payload = {
        'username': config['username'],
        'password': config['password'],
        'redirect': 'http://osu.ppy.sh/forum/ucp.php',
        'sid': '',
        'login': 'login'
    }

    payload = urllib.parse.urlencode(payload).encode("utf-8")
    response = opener.open("http://osu.ppy.sh/forum/ucp.php?mode=login", payload)

    data = bytes(str(response.read()), "utf-8").decode("unicode_escape")

    if "incorrect password" in data:
        print("Incorrect password")

    return downloadReplays(bid)

def downloadReplays(bid):
    try:
        url = 'http://osu.ppy.sh/d/{}n'.format(bid)
        d = opener.open(url, b"")
        return d.read()
    except Exception as e:
        print("Failed to download")