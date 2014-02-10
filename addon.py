from xbmcswift2 import Plugin
from Reddit import Reddit
from Reddit import LoLEventVODS

plugin = Plugin()


@plugin.route('/')
def index():
    items = []

    item  = { 'label': 'Reddit LoL Event VODS', 'path': plugin.url_for('show_events') }
    items.append(item)
    #item  = { 'label': 'Reddit LoL Event VODS', 'path': plugin.url_for('show_events') }
    #items.append(item)

    return items

@plugin.route('/loleventvods/')
def show_events():
    r = Reddit.Reddit()
    events = r.loadEvents()
    items = []

    for lolevent in events:
        if (lolevent.isEvent):
            item  = { 'label': lolevent.displayTitle(), 'path': plugin.url_for('show_event', eventId=lolevent.eventId) }
            items.append(item)

    return items

@plugin.route('/loleventvods/event/<eventId>')
#@plugin.cached(TTL=10)
def show_event(eventId):
    items = []

    r = Reddit.Reddit()
    r.loadEventContent(eventId)
    #loadEventMatches(eventId)

    return items

if __name__ == '__main__':
    plugin.run()
