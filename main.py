import requests, json
import atprototools, sys
# from aiohttp import web
from flask import Flask, request, redirect
from urllib.parse import urlparse, quote

urlencode = quote

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://disc"+"ord.com/api/web"+"hooks/110338283"+"6788084819/XNyc-N5bWsz160LM45v8"+"u9AjMv_GmAxPfpn3OAWYG1kBSY"+"t8ux5br4QRBk8xcdV5qLbK"
DISCORD_MONITOR_WEBHOOK_URL = "https://disc"+"ord.com/api/webh"+"ooks/11050580500"+"76852234/WVTQke61gVg-6Zy4OPVAYACe"+"crPwXpDInU1nxW8owWqcrbVEmpIATKFSeGFeWeIOY-32"

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

generate_embed_user_agents = [
    "facebookexternalhit/1.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 10.0; en-US; Valve Steam Client/default/1596241936; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 10.0; en-US; Valve Steam Client/default/0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.4 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.4 facebookexternalhit/1.1 Facebot Twitterbot/1.0", 
    "facebookexternalhit/1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; Valve Steam FriendsUI Tenfoot/0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36", 
    "Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0", 
    "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)", 
    "TelegramBot (like TwitterBot)", 
    "Mozilla/5.0 (compatible; January/1.0; +https://gitlab.insrt.uk/revolt/january)", 
    "Synapse (bot; +https://github.com/matrix-org/synapse)",
    "test"]


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
    global session
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

    global session
    post_content = session.get_bloot_by_url(full_path).json()
    post_content = post_content.get("posts")[0] # might error here? need to learn about the types
    author = post_content.get("author")
    displayName = author.get("displayName")

    img_url = None
    try:
        img_url = post_content.get("embed").get("images")[0].get("fullsize") # alterantively thumb
    except:
        pass

    post_url = full_path

    record = post_content.get("record")
    text = record.get("text")

    text = text.replace("<","").replace(">","").replace('"',"")

    html = f"""
    <html lang="en">
    <head>

    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    <meta content="#7FFFD4" name="theme-color" />
    <meta property="og:site_name" content="psky.app" />
    <meta property="og:title" content="{displayName} (@{author.get("handle")}" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{displayName} (@{author.get("handle")}) " />
    <meta name="twitter:image" content="{img_url}" />
    <meta name="twitter:creator" content="@{displayName}" />

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
    # fixes bug where profile previews wouldn't show if you used staging.psky.app on just a profile
    assert ("https://bsky.app/profile/" in full_path  or "https://staging.bsky.app/profile/" in full_path)

    global session

    username = get_username(full_path)
    # import pdb; pdb.set_trace()
    profile_json = session.getProfile(username).json()

    handle = profile_json.get("handle")
    bio = profile_json.get("description")
    displayName = profile_json.get("displayName")
    profile_url = full_path

    bio = bio.replace("<","").replace(">","")
    displayName = displayName.replace("<","").replace(">","")

    html = f"""
    <html lang="en">
    <head>

    <meta name="description" content="(target audience: students)">
    
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    <meta content="#7FFFD4" name="theme-color" />
    <meta property="og:site_name" content="psky.app" />
    <meta property="og:title" content="{displayName} (@{handle})" />

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
    </html>
    """
    return html

# TODO delete the distinction between image and text; the only difference is the image field so they can probabyl
# be the same html
def generate_html_textonly(full_path):
    assert ("https://bsky.app/profile/" in full_path  or "https://staging.bsky.app/profile/" in full_path)

    global session
    post_content = session.get_bloot_by_url(full_path).json()
    post_content = post_content.get("posts")[0] # might error here? need to learn about the types
    author = post_content.get("author")

    img_url = None

    post_url = full_path

    record = post_content.get("record")
    text = record.get("text")

    text = text.replace("<","").replace(">","").replace("\"","&#34;")
    displayName = author.get("displayName")
    displayName = displayName.replace("<","").replace(">","")

    html = f"""
    <html lang="en">
    <head>

    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    <meta content="#7FFFD4" name="theme-color" />
    <meta property="og:site_name" content="psky.app" />
    <meta property="og:title" content="{displayName} (@{author.get("handle")}" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{displayName} (@{author.get("handle")}) " />
    <meta name="twitter:image" content="{img_url}" />
    <meta name="twitter:creator" content="@{displayName}" />

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
    global session
    post_content = session.get_bloot_by_url(full_path).json()

    post_content = post_content.get("posts")[0]

    author = post_content.get("author")

    img_url = None 

    post_url = full_path

    record = post_content.get("record")

    text = record.get("text")

    embed = post_content.get('embed')

    embed_type = embed.get("$type")

    displayName = author.get("displayName")
    text = text.replace("<","").replace(">","").replace("\"","")
    displayName = displayName.replace("<","").replace(">","")

    try:
        # at this point it's either a image or something like a github embed card
        # there's a $type field we can split on
        embed_type = embed.get("$type")
        embed_text = embed.get('record').get('value').get('text')
        embed_text = embed_text.replace("<","").replace(">","").replace('"',"")
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
    <meta property="og:title" content="{displayName} (@{author.get("handle")}" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{displayName} (@{author.get("handle")}) " />
    <meta name="twitter:image" content="{img_url}" />
    <meta name="twitter:creator" content="@{displayName}" />

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

def generate_link_preview(full_path, request):
    assert ("https://bsky.app/profile/" in full_path  or "https://staging.bsky.app/profile/" in full_path)
    # TODO type to contain / enforce https://bsky.app/profile/DIDxorUSERNAME/post/RKEY
    # @chatgpt please write me a type

    global session 

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

        # if request.user_agent not in generate_embed_user_agents:
        #     return redirect("https://staging.psky.app/"+path)

        global session

        session = atprototools.Session(USERNAME,APP_PASSWORD)
        html = generate_link_preview("https://bsky.app/" + path, request)

        # resp = requests.post(DISCORD_MONITOR_WEBHOOK_URL, json={ 'content':"https://psky.app/"+path}, headers={'Content-Type': 'application/json'})
    
        return html


if __name__ == "__main__":
    app.run(port=8081)
