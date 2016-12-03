import requests
import facebook
import settings

URL = "https://graph.facebook.com/oauth/access_token"


def get_facebook_page(url):
    try:
        graph = facebook.GraphAPI(access_token=settings.APP_TOKEN, version='2.5')
        o = graph.get_object(url)
    except facebook.GraphAPIError as e:
        o = False
    return o


# When we load for the first time we want to set the TOKEN
r = requests.get(URL, {
    'client_id': settings.APP_ID,
    'client_secret': settings.APP_SECRET,
    'grant_type': 'client_credentials',
})
r.raise_for_status()
key, value = r.text.split("=")
assert key == "access_token"
settings.APP_TOKEN = value
