import requests, json
import atprototools, sys
# from aiohttp import web
from flask import Flask, request, redirect

app = Flask(__name__)

# upon receiving a psky.app request
# fetch the bloot from bsky

# need a webserver. flask or aiohttp
# lets aiohttp
# i wrote one recently.....

creds = json.load(open("credentials.json"))
USERNAME = creds.get("USERNAME")
APP_PASSWORD = creds.get("APP_PASSWORD")

'''
GET / HTTP/1.1
user-agent: Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)
host: 5.42.201.69:8082
'''

discord_preview_for_video_tweet = '''
<!DOCTYPE html>
<html lang="en">
<head>

<meta content='text/html; charset=UTF-8' http-equiv='Content-Type' />
<meta content="#7FFFD4" name="theme-color" />
<meta property="og:site_name" content="vxTwitter">

<meta name="twitter:card" content="player" />
<meta name="twitter:title" content="Ian Klatzco (@ian5v) " />
<meta name="twitter:image" content="0" />
<meta name="twitter:player:width" content="1104" />
<meta name="twitter:player:height" content="864" />
<meta name="twitter:player:stream" content="https://video.twimg.com/ext_tw_video/1553060639530225664/pu/vid/920x720/qT8hHQq3KZUFi7uo.mp4?tag=12" />
<meta name="twitter:player:stream:content_type" content="video/mp4" />

<meta property="og:url" content="https://video.twimg.com/ext_tw_video/1553060639530225664/pu/vid/920x720/qT8hHQq3KZUFi7uo.mp4?tag=12" />
<meta property="og:video" content="https://video.twimg.com/ext_tw_video/1553060639530225664/pu/vid/920x720/qT8hHQq3KZUFi7uo.mp4?tag=12" />
<meta property="og:video:secure_url" content="https://video.twimg.com/ext_tw_video/1553060639530225664/pu/vid/920x720/qT8hHQq3KZUFi7uo.mp4?tag=12" />
<meta property="og:video:type" content="video/mp4" />
<meta property="og:video:width" content="1104" />
<meta property="og:video:height" content="864" />
<meta name="twitter:title" content="Ian Klatzco (@ian5v) " />
<meta property="og:image" content="0" />
<meta property="og:description" content="*zooms out*" />

<link rel="alternate" href="https://vxtwitter.com/oembed.json?desc=Ian%20Klatzco&user=%2Azooms%20out%2A&link=https%3A//twitter.com/ian5v&ttype=video" type="application/json+oembed" title="Ian Klatzco">
<meta http-equiv="refresh" content="0; url = https://twitter.com/ian5v/status/1553060950592425984" />
</head>
<body>
     Redirecting you to the tweet in a moment. <a href="https://twitter.com/ian5v/status/1553060950592425984">Or click here.</a>
</body>
'''

discord_preview_for_image_tweet = '''<!DOCTYPE html>
<html lang="en">
<head>

<meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
<meta content="#7FFFD4" name="theme-color" />
<meta property="og:site_name" content="vxTwitter" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Ian Klatzco (@ian5v) " />
<meta name="twitter:image" content="https://pbs.twimg.com/media/FujPeHmX0AAI2FX.jpg" />
<meta name="twitter:image" content="https://pbs.twimg.com/media/FujPeHmX0AAI2FX.jpg" />
<meta name="twitter:creator" content="@Ian Klatzco" />

<meta property="og:description" content="Berliners! Come to cbase at 1900 to see me give a talk on http://twitterbsky.klatz.co:8080 https://twitterbsky.klatz.co:8080 for @BerlinHacknTell


as predicted, Twitter killed the code it depends on ^^

cc @mr_ligi @coderobe

💖 0 🔁 0" />

<link rel="alternate" href="https://vxtwitter.com/oembed.json?desc=Ian%20Klatzco&user=Twitter&link=https%3A//twitter.com/ian5v&ttype=photo" type="application/json+oembed" title="Ian Klatzco">
<meta http-equiv="refresh" content="0; url = https://twitter.com/ian5v/status/1650797442550448129" />
</head>
<body>
     Redirecting you to the tweet in a moment. <a href="https://twitter.com/ian5v/status/1650797442550448129">Or click here.</a>
</body>
'''

post_url =  "https://staging.bsky.app/profile/klatz.co/post/3ju6rnqcnig2c"
img_url = "https://cdn.bsky.social/imgproxy/zqjeyWF5Sxzf-3ShQPWNGvqZU6OW5416vwlLmfFKeEI/rs:fit:2000:2000:1:0/plain/bafkreih5d3p6leodugpc7gx5xx2sjralbgzdnbvyn6m7usp5otkearc3kq@jpeg"
content = """Berliners! Come to cbase at 1900 to see me give a talk on http://twitterbsky.klatz.co:8080 https://twitterbsky.klatz.co:8080 for @BerlinHacknTell

as predicted, Twitter killed the code it depends on ^^

cc @mr_ligi @coderobe
"""


@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def index(path):
    session = atprototools.Session(USERNAME,APP_PASSWORD)

    print(request.url)

    if str(request.url) == "https://psky.app/" or \
       str(request.url) == "http://psky.app/"  or \
       str(request.url) == "https://staging.psky.app/"  or \
       str(request.url) == "http://staging.psky.app/":
        return redirect("https://github.com/ianklatzco/psky.app/")

    # https://staging.psky.app/profile/klatz.co/post/3ju6rnqcnig2c
    if request.method == "GET":
        # requests.get("https://example.com")
        # request comes in with a url
        # parse the URL, fetch the corresponding content from bsky, return it formatted

        # what is the aiohttp for the url?
        print(request.path)
        bsky_url = "https://bsky.app" + str(request.path)
        post_content = session.get_skoot_by_url(bsky_url).json()
        post_content = post_content.get("thread").get("post")

        author = post_content.get("author")
        img_url = post_content.get("embed").get("images")[0].get("fullsize")
        record = post_content.get("record")
        text = record.get("text")

        html = f"""
        <html lang="en">
        <head>

        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
        <meta content="#7FFFD4" name="theme-color" />
        <meta property="og:site_name" content="psky.app" />

        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="{author.get("displayName")} (@{author.get("handle")}) " />
        <meta name="twitter:image" content="{img_url}" />
        <meta name="twitter:creator" content="@{author.get("displayName")}" />

        <meta property="og:description" content="{text}" />

        <!-- TODO what on earth is this -->
        <!-- <link rel="alternate" href="https://vxtwitter.com/oembed.json?desc=Ian%20Klatzco&user=Twitter&link=https%3A//twitter.com/ian5v&ttype=photo" type="application/json+oembed" title="Ian Klatzco"> -->
        <meta http-equiv="refresh" content="0; url = {post_url}" />
        </head>
        <body>
            Redirecting you to the tweet in a moment. <a href="{post_url}">Or click here.</a>
        </body>
        """
    
        # import pdb; pdb.set_trace()

        return html
        # return web.Response(text=discord_preview_for_that, content_type="text/html")

if __name__ == "__main__":
    app.run(port=8081)
