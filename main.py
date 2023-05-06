import requests, json
import atprototools, sys
# from aiohttp import web
from flask import Flask, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://disc"+"ord.com/api/web"+"hooks/110338283"+"6788084819/XNyc-N5bWsz160LM45v8"+"u9AjMv_GmAxPfpn3OAWYG1kBSY"+"t8ux5br4QRBk8xcdV5qLbK"

def my_exception_handler(type, value, traceback):
    # Here, you can define how you want to handle the exception.
    # In this example, we'll just print the type and value of the exception.
    a = f"Caught {type.__name__}: {value}"
    print(a)
    print(traceback)
    resp = requests.post(DISCORD_WEBHOOK_URL, json={ 'content':a}, headers={'Content-Type': 'application/json'})
    # resp = requests.post(DISCORD_WEBHOOK_URL, json={ 'content':traceback}, headers={'Content-Type': 'application/json'})


# Set the excepthook to our custom exception handler.
sys.excepthook = my_exception_handler

# Here's some code that raises an exception.
# raise ValueError("Something went wrong!")


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

session = None


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

def contains_embed(full_path):
    assert "https://bsky.app/profile/" in full_path 
    # really more like "record contains another"
    # what does a quotebloot look like in the json?
    resp = session.get_bloot_by_url(full_path)
    #  thread -> post -> embed -> notNote
    try:
        ff = resp.json().get('posts')[0].get('record').get('embed')
    except:
        resp = requests.post(DISCORD_WEBHOOK_URL, json={ 'content':"naughty url that failed: <"+full_path+">\n\n" + str(resp.json())}, headers={'Content-Type': 'application/json'})
        raise ValueError("failed for some reason?")
    return ff != None


def generate_html_with_image(full_path):
    assert "https://bsky.app/profile/" in full_path 

    post_content = session.get_bloot_by_url(full_path).json()
    post_content = post_content.get("posts")[0] # might error here? need to learn about the types
    author = post_content.get("author")

    img_url = None
    try:
        img_url = post_content.get("embed").get("images")[0].get("fullsize") # alterantively thumb
    except:
        pass

    post_url = full_path.replace("bsky.app","staging.bsky.app")

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

def generate_html_profileonly(full_path):
    assert "https://bsky.app/profile/" in full_path 

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

def generate_html_textonly(full_path):
    assert "https://bsky.app/profile/" in full_path 

    post_content = session.get_bloot_by_url(full_path).json()
    post_content = post_content.get("posts")[0] # might error here? need to learn about the types
    author = post_content.get("author")

    img_url = None

    post_url = full_path.replace("bsky.app","staging.bsky.app")

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

def generate_html_qrt(full_path):
    '''
    # qrts can have an image in the QRT or the undertweet.
    # discord and telegram will only show 1-4 images.
    # i'm not sure which of the two is best?
    # should probably be "prefer undertweet over QRT but do at least one"
    ''' # TODO /fileanissue from_docstring
    post_content = session.get_bloot_by_url(full_path).json()

    post_content = post_content.get("posts")[0]

    author = post_content.get("author")

    img_url = None 

    post_url = full_path.replace("bsky.app","staging.bsky.app")

    record = post_content.get("record")

    text = record.get("text")

    embed = post_content.get('embed')

    embed_type = embed.get("$type")

    try:
        # at this point it's either a image or something like a github embed card
        # there's a $type field we can split on
        embed_type = embed.get("$type")
        embed_text = embed.get('record').get('value').get('text')
        embed_author = embed.get('record').get('author').get('handle')
        embed_image = None # TODO
    except:
        print("embed fetching failed")

    if img_url == None:
        try:
            img_url = embed.get('record').get('embeds')[0].get('images')[0].get('fullsize')
        except:
            pass

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

    <meta property="og:description" content="{text}

    = QRT  @ {embed_author} =================================================
    {embed_text}
    " />

    <!-- TODO what on earth is this -->
    <!-- <link rel="alternate" href="https://vxtwitter.com/oembed.json?desc=Ian%20Klatzco&user=Twitter&link=https%3A//twitter.com/ian5v&ttype=photo" type="application/json+oembed" title="Ian Klatzco"> -->
    <meta http-equiv="refresh" content="0; url = {post_url}" />
    </head>
    <body>
        Redirecting you to the tweet in a moment. <a href="{post_url}">Or click here.</a>
    </body>
    """

    return html

def generate_link_preview(full_path):
    assert "https://bsky.app/profile/" in full_path 
    # TODO type to contain / enforce https://bsky.app/profile/DIDxorUSERNAME/post/RKEY
    # @chatgpt please write me a type

    if is_just_profile_url(full_path):
        return generate_html_profileonly(full_path)

    if not contains_embed(full_path): # text post with no image or qrt
        return generate_html_textonly(full_path)

    if contains_embed(full_path):
        embed = session.get_bloot_by_url(full_path).json().get('posts')[0].get('record').get('embed')
        embed_type = embed.get("$type")
        if embed_type == "app.bsky.embed.record": # qrt
            return generate_html_qrt(full_path)
        elif (embed_type == "app.bsky.embed.images"):
            return generate_html_with_image(full_path)
        else: # external
            # TODO fetch the image from the external embed
            # but it's possible some external embed don't have images
            # in which case simply displaying the link might be best
            return generate_html_textonly(full_path)


@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def index(path):

    print(request.url) # TODO flask log instead of print

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

        # print("PATH: ", end='')
        # print(path)
        # print("request.path: ", end='')
        print(request.path)

        global session

        session = atprototools.Session(USERNAME,APP_PASSWORD)
        html = generate_link_preview("https://bsky.app/" + path)
    
        return html


if __name__ == "__main__":
    app.run(port=8081)
