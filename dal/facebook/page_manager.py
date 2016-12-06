import settings
from core.dal import mdb_connect, fb_connect
from dal.facebook import feed_manager
from enum import Enum


class PageType(Enum):
    page = 1
    group = 2


SEARCH = "search?q='{}'&type={}&limit=100"
URL = "{}?fields=about,picture,hometown,fan_count,bio,insights.limit(1),category,name"
GROUP_URL = "{}?fields=description,email,icon,link,name,updated_time"


def insert_update_page(o, f_id, url="", type=PageType.page, check=False):
    data = False
    if type is PageType.group.value:
        data = {
            'id': o['id'],
            'email': o.get('email', None),
            'updated_time': o.get('updated_time', None),
            'about': o.get('description', None),
            'picture': o.get('icon', None),
        }

    if type is PageType.page.value:
        data = {
            'likes': o['fan_count'],
            'category': o['category'],
            'about': o['about'],
            'picture': o['picture']['data']['url'],
        }

    if not data:
        assert False, 'Please implement new type'
    # Add the common fields
    data['id'] = o['id']
    data['name'] = o.get('name', None)
    data['f_id'] = f_id
    data['url'] = url
    data['type'] = type

    update_rst = mdb_connect.insert_update(settings.PAGES, o['id'], data=data)
    return update_rst['ok'] == 1


def update_page_by_name(name, p_type):
    print("updating page " + str(name))
    url = URL.format(name)
    if p_type is PageType.group.value:
        url = GROUP_URL.format(name)
    o = fb_connect.get_facebook_page(url)
    if o:
        return insert_update_page(o, name, url, type=p_type, check=False)
    return False


def update_pages_by_search(filter, p_type=PageType.page.value):
    base_url = URL
    url = SEARCH.format(filter, 'page')
    if p_type is PageType.group.value:
        url = SEARCH.format(filter, 'group')
        base_url = GROUP_URL
    o = fb_connect.get_facebook_page(url)
    if o:
        feeds = [insert_update_page(page, page['id'], base_url.format(page['id']), p_type, check=False) for page in
                 o['data']
                 if
                 page['privacy'] == "OPEN"]
        return feeds
    return False


def remove_page_by_id(page_id):
    mdb_connect.remove_item(settings.PAGES, page_id)


def update_multi_ids(ids, up_feeds=False):
    jobs = [update_page_by_name(id, type) for id, type in ids]
    if up_feeds:
        jobs += [update_feeds(id) for id, type in ids]
    return jobs


def update_feeds(page_id):
    return feed_manager.update_owner_feed(page_id)


def reset_db():
    mdb_connect.reset_db(settings.PAGES)


def get_pages():
    pages = {}
    for index, page in enumerate(mdb_connect.get_collection(settings.PAGES)):
        page['_id'] = str(page['_id'])
        pages[page['_id']] = page
    return pages
