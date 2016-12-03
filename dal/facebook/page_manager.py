import settings
from core.dal import mdb_connect, fb_connect
from dal.facebook import feed_manager

URL = "{}?fields=about,picture,hometown,fan_count,bio,insights.limit(1),category,name"
# GROUP_URL = "{}?fields=description,email,icon,link,name,updated_time"


def insert_update_page(o, f_id, url="", check=False):
    update_rst = mdb_connect.insert_update(settings.PAGES, o['id'], data={'id': o['id'],
                                                                          'likes': o['fan_count'],
                                                                          'category': o['category'],
                                                                          'about': o['about'],
                                                                          'name': o['name'],
                                                                          'f_id': f_id,
                                                                          'picture': o['picture']['data']['url'],
                                                                          'url': url,
                                                                          })
    # fast assertion area (when prod should cp to Unit test?)
    return update_rst['ok'] == 1


def update_page_by_name(name):
    url = URL.format(name)
    o = fb_connect.get_facebook_page(url)
    if o:
        return insert_update_page(o, name, url, check=False)
    return False


def remove_page_by_id(page_id):
    mdb_connect.remove_item(settings.PAGES, page_id)


def update_multi_ids(ids, up_feeds=False):
    jobs = [update_page_by_name(id) for id in ids]
    if up_feeds:
        jobs += [update_feeds(id) for id in ids]
    return jobs


def update_feeds(page_id):
    return feed_manager.update_owner_feed(page_id)


def reset_db():
    mdb_connect.reset_db(settings.PAGES)


def get_page(f_url):
    return next(mdb_connect.get_collection(settings.PAGES, {"f_id": f_url}), 'Not found')


def get_pages():
    pages = {}
    for index, page in enumerate(mdb_connect.get_collection(settings.PAGES)):
        pages[page['id']] = page
    return pages
