import requests, aiohttp
import atprototools

# upon receiving a psky.app request
# fetch the bloot from bsky

# need a webserver. flask or aiohttp
# lets aiohttp
# i wrote one recently.....

async def handle(request):
    if request.method == "GET":
        requests.get("")
        return web.Response(text="foo", content_type="text/html")

def main():
    app = web.Application()
    app.add_routes([
        web.get('/', handle),
        # web.post('/', handle),
        # web.post('/upload', handle_upload),
        # web.post('/testsetup', handle_testsetup)
    ])
    web.run_app(app)

# test_get_bsky_username()
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        if args[0] == "--test-get-bsky-username":
            test_get_bsky_username()
    else:
        main()
