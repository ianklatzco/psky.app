import requests, json
import atprototools, sys
from aiohttp import web

# upon receiving a psky.app request
# fetch the bloot from bsky

# need a webserver. flask or aiohttp
# lets aiohttp
# i wrote one recently.....

creds = json.loads("credentials.json")
USERNAME = creds.get("USERNAME")
APP_PASSWORD = creds.get("APP_PASSWORD")

async def handle(request):
    session = atprototools.Session(USERNAME,APP_PASSWORD)
    if request.method == "GET":
        requests.get("https://example.com")
        return web.Response(text="foo", content_type="text/html")

def main():
    app = web.Application()
    app.add_routes([
        web.get('/', handle),
        # web.post('/', handle),
        # web.post('/upload', handle_upload),
        # web.post('/testsetup', handle_testsetup)
    ])
    web.run_app(app, port=8081)

if __name__ == "__main__":
    main()
