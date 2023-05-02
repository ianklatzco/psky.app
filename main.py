import requests, json
import atprototools, sys
# from aiohttp import web
from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)

# upon receiving a psky.app request
# fetch the bloot from bsky

# need a webserver. flask or aiohttp
# lets aiohttp
# i wrote one recently.....

# lol jk aiohttp is more finicky than flask despite being more performant
# throws a 400 error, seems like you need another server/wsgi in front of it to validate correctly formatted html
# but my requests are relatively benign and it's still failing

creds = json.load(open("credentials.json"))
USERNAME = creds.get("USERNAME")
APP_PASSWORD = creds.get("APP_PASSWORD")


def is_just_profile_url(full_path):
    url = urlparse(full_path).path.split('/')
    newli = []
    for x in url:
        if x == '':
            continue
        newli.append(x)
    return len(newli) == 2

def get_username(full_path):
    url = urlparse(full_path).path.split('/')
    newli = []
    for x in url:
        if x == '':
            continue
        newli.append(x)
    return newli[1]

def is_quotebloot(full_path):
    pass


def generate_html(full_path):
    # path = /profile/klatz.co/post/3jua5rlgrq42p
    # or
    # path = /profile/DID/post/3jua5rlgrq42p

    session = atprototools.Session(USERNAME,APP_PASSWORD)

    if is_just_profile_url(full_path):
        username = get_username(full_path)
        profile_json = session.getProfile(username).json()

        handle = profile_json.get("handle")
        bio = profile_json.get("description")
        displayName = profile_json.get("displayName")
        profile_url = full_path

        html = f"""
        <html lang="en">
        <head>

        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
        <meta content="#7FFFD4" name="theme-color" />
        <meta property="og:site_name" content="psky.app" />

        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="{displayName} (@{handle}) " />
        <meta name="twitter:creator" content="@{displayName}" />

        <meta property="og:description" content="{bio}" />

        <!-- TODO what on earth is this -->
        <!-- <link rel="alternate" href="https://vxtwitter.com/oembed.json?desc=Ian%20Klatzco&user=Twitter&link=https%3A//twitter.com/ian5v&ttype=photo" type="application/json+oembed" title="Ian Klatzco"> -->
        <meta http-equiv="refresh" content="0; url = {profile_url}" />
        </head>
        <body>
            Redirecting you to the tweet in a moment. <a href="{profile_url}">Or click here.</a>
        </body>
        """
        return html

    post_content = session.get_bloot_by_url(full_path).json()

    post_content = post_content.get("posts")[0]

    print(full_path) # TODO flask log instead of print
    post_url = full_path.replace("psky","bsky")
    if "staging" not in post_url:
        post_url = post_url.replace("bsky.app","staging.bsky.app")

    author = post_content.get("author")
    img_url=""
    try:
        img_url = post_content.get("embed").get("images")[0].get("fullsize")
    except:
        pass
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
    return html


@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def index(path):

    print(request.url)

    if ("favicon.ico" in str(request.url)):
        return ""

    # TODO @yafesdot or anyone listcomprehension this so the only inputs are psky and fxbsky
    if str(request.url) == "https://psky.app/" or \
       str(request.url) == "http://psky.app/"  or \
       str(request.url) == "https://fxbsky.app/" or \
       str(request.url) == "http://fxbsky.app/"  or \
       str(request.url) == "https://staging.fxbsky.app/" or \
       str(request.url) == "http://staging.fxbsky.app/"  or \
       str(request.url) == "https://staging.psky.app/"  or \
       str(request.url) == "http://staging.psky.app/":
        return redirect("https://github.com/ianklatzco/psky.app/")

    # https://staging.psky.app/profile/klatz.co/post/3ju6rnqcnig2c
    if request.method == "GET":
        # requests.get("https://example.com")
        # request comes in with a url
        # parse the URL, fetch the corresponding content from bsky, return it formatted

        print("PATH: ", end='')
        print(path)
        print("request.path: ", end='')
        print(request.path)

        html = generate_html("https://bsky.app/" + path)
    
        return html

if __name__ == "__main__":
    app.run(port=8081)
