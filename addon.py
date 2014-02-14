from xbmcswift2 import Plugin
from Reddit import Reddit
import re


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
@plugin.cached(TTL=10)
def show_events():
    r = Reddit.Reddit()
    events = r.loadEvents(True)
    items = []

    for lolevent in events:
        if (lolevent.status < 99):
            status = "In Progress"
            if (lolevent.status == 1):
                status = "Finished"
            item  = { 'label': lolevent.title + " (" + status + ")", 'path': plugin.url_for('show_event', eventId=lolevent.eventId) }
            items.append(item)

    return items

@plugin.route('/loleventvods/event/<eventId>')
@plugin.cached(TTL=10)
def show_event(eventId):
    items = []

    r = Reddit.Reddit()
    days = r.loadEventContent(eventId)
    #loadEventMatches(eventId)
    for day in days:
        item  = { 'label': day.day, 'path': plugin.url_for('show_matches', eventId=eventId, dayId = day.dayId) }
        items.append(item)

    return items

@plugin.route('/loleventvods/event/<eventId>/matches/<dayId>')
@plugin.cached(TTL=10)
def show_matches(eventId, dayId):
    items = []

    r = Reddit.Reddit()
    days = r.loadEventContent(eventId)

    day = days[int(dayId)]
    if (day is not None):
        for match in day.matches:
            item  = { 'label': match.team1 + " vs "+ match.team2, 'path': plugin.url_for('show_videos', eventId=eventId, dayId = dayId, gameId = match.gameId) }
            items.append(item)

    return items

@plugin.route('/loleventvods/event/<eventId>/matches/<dayId>/videos/<gameId>')
#@plugin.cached(TTL=10)
def show_videos(eventId, dayId, gameId):
    items = []

    r = Reddit.Reddit()
    days = r.loadEventContent(eventId)

    day = days[int(dayId)]
    if (day is not None):
        for match in day.matches:
            if (match.gameId == gameId):
                for video in match.videoLinks:
                    if (video is not None):
                        # We can iterate the video links
                        if (video['text'] is not None and video['link'] is not None):
                            videoLink = play_match(video['link'])
                            playable = (videoLink != "")
                            item  = { 'label': video['text'].replace('&amp;', '&'),
                                      'path': videoLink,
                                      'is_playable': playable}
                            items.append(item)

    return items

def play_match(url):
    #http://www.youtube.com/watch?v=nj7ySi24rRQ&amp;t=7h11m20s
    r = Reddit.Reddit()

    youtube_id = 'EMPTY'
    youtube_Time = ''
    matches = re.findall("(\?|\&)([^=]+)\=([^&]+)", url)
    if (matches is not None):
        for match in matches:
            if (match is not None):
                if (match[1] == "v"):
                    youtube_id = match[2]
                if (match[1] == "t"):
                    youtube_Time = match[2]

    if youtube_id != 'EMPTY':
        youtube_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtube_id
    else:
        youtube_url = ""

    return youtube_url

if __name__ == '__main__':
    plugin.run()
