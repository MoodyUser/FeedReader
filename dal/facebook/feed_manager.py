import settings
from core.dal import mdb_connect, fb_connect


URL = "{}"
OWNER_URL = "{}/feed?limit={}"


def insert_update_feed(o, owner_id=None, url="", check=False):
    if not (o.get('message', False) or o.get('story', False)):
        # only message or storys in our case.
        return False

    data = {'id': o['id'],
            'message': o.get('message', None),
            'story': o.get('story', None),
            'url': url,
            'created_time': o['created_time'],
            }

    if owner_id:
        # We don't want to update the owner id if none.
        data['owner_id'] = owner_id

    update_rst = mdb_connect.insert_update(settings.FEEDS, o['id'], data=data)
    return update_rst['ok'] == 1


def update_owner_feed(owner_id, limit=100):
    url = OWNER_URL.format(owner_id, limit)
    o = fb_connect.get_facebook_page(url)
    if o:
        feeds = [insert_update_feed(feed, owner_id, url, check=False) for feed in o['data']]
        return feeds
    return False


def update_feed_by_id(feed_id, owner_id=None):
    url = URL.format(feed_id)
    o = fb_connect.get_facebook_page(url)
    if o:
        return insert_update_feed(o, owner_id, url, check=False)
    return False


def remove_feed_by_id(feed_id):
    mdb_connect.remove_item(settings.FEED, feed_id)


def update_multi_ids(ids, owner_id):
    jobs = [update_feed_by_id(id, owner_id) for id in ids]
    return jobs


def reset_db():
    mdb_connect.reset_db(settings.FEED)


def get_feeds():
    feeds = {}
    for index, feed in enumerate(mdb_connect.get_collection(settings.FEED)):
        feeds[feed['id']] = feed
    return feeds
