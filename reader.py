'''fb feed reader 1.0

This tool is design to keep track with feeds from facebook

Usage:
  reader  add_page <page_id> [--feeds] [--type=1]
  reader  list_pages
  reader  update <page_id> [--limit=100] [--feeds] [--type=1]
  reader  update_all [--feeds]
  reader  remove_page <page_id>
  reader  -h | --help
  reader  --version
  reader  --reset

Options:
    add_page <page_id>:  add <page_id> page id from facebook --type (1:page,2:group)
    list_pages :  all the pages in the db
    update <page_id>  [--limit=100] [--feeds] [--type=1]:  updating or adding the <page_id> page and update page feed with limit
    update_all [--feeds]:  updating the page latest feeds
    remove_page <page_id>:  remove <page_id> page from the database

'''
from pprint import pprint

from docopt import docopt

from dal.facebook import page_manager, feed_manager

if __name__ == "__main__":
    arguments = docopt(__doc__, version='agg_server 1.0')
    if arguments['update']:
        p_type = int(arguments['--type']) if arguments['--type'] else page_manager.PageType.page.value
        assert page_manager.update_page_by_name(arguments['<page_id>'], p_type)
        limit = arguments['--limit'] if arguments['--limit'] else 100
        feeds = arguments['--feeds'] if arguments['--feeds'] else False
        if feeds:
            assert all(page_manager.update_feeds(arguments['<page_id>'])), "Feeds didn't update"
    if arguments['update_all']:
        limit = arguments['--limit'] if arguments['--limit'] else 100
        feeds = arguments['--feeds'] if arguments['--feeds'] else False
        ids = [(id, page['type']) for id, page in page_manager.get_pages().items()]
        assert all(page_manager.update_multi_ids(ids, feeds)), "Update didn't fully complete"
    if arguments['add_page']:
        p_type = int(arguments['--type']) if arguments['--type'] else page_manager.PageType.page.value
        assert page_manager.update_page_by_name(arguments['<page_id>'], p_type), "Please enter a correct page id"
        feeds = arguments['--feeds'] if arguments['--feeds'] else False
        if feeds:
            assert all(page_manager.update_feeds(arguments['<page_id>'])), "Please enter a correct page id"
    if arguments['remove_page']:
        page_manager.remove_page_by_id(arguments['<page_id>'])
    if arguments['list_pages']:
        pprint(page_manager.get_pages())
    if arguments['--reset']:
        page_manager.reset_db()
        feed_manager.reset_db()
        pprint(page_manager.get_pages())
