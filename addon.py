from xbmcswift2 import Plugin

from Data import Reddit
from Data import Standings


plugin = Plugin()


@plugin.route('/')
def index():
    items = []

    item  = { 'label': 'Reddit LoL Event VODS', 'path': plugin.url_for('show_events') }
    items.append(item)
    item  = { 'label': 'Settings', 'path':plugin.url_for('open_settings')  }
    items.append(item)

    return items

# Settings
@plugin.route("/settings/")
def open_settings():
    plugin.open_settings()

# LOL EVENT VODS
@plugin.route('/loleventvods/')
@plugin.cached(TTL=10)
def show_events():

    events = Reddit.loadEvents(True)
    items = []

    for lolevent in events:
        if (lolevent.status < 99):
            status = "In Progress"
            if (lolevent.status == 1):
                status = "Finished"
            item  = { 'label': lolevent.title + " (" + status + ")", 'path': plugin.url_for('show_event', eventId=lolevent.eventId),
                      'thumbnail' : lolevent.imageUrl, 'icon' : lolevent.imageUrl  }
            items.append(item)

    return items

@plugin.route('/loleventvods/event/<eventId>')
@plugin.cached(TTL=10)
def show_event(eventId):
    items = []

    days = Reddit.loadEventContent(eventId)
    #loadEventMatches(eventId)
    for day in days:
        item  = { 'label': day.day.replace('&amp;', '&'), 'path': plugin.url_for('show_matches', eventId=eventId, dayId = day.dayId) }
        items.append(item)

    return items

@plugin.route('/loleventvods/event/<eventId>/matches/<dayId>')
@plugin.cached(TTL=10)
def show_matches(eventId, dayId):
    items = []

    days = Reddit.loadEventContent(eventId)

    day = days[int(dayId)]
    if (day is not None):
        for match in day.matches:
            recommended = ''
            # Add spoiler data?
            if (day.recommended.find(match.gameId) > -1 and plugin.get_setting('highlight_recommended_games', bool)):
                recommended = '*'

            # Add standings?
            t1standing = ''
            t2standing = ''
            try:
                if (plugin.get_setting('include_current_lcs_standings', bool)):
                    #Need to make this work using Standings Module
                    standingT1 = Standings.getLCSStandings(match.team1)
                    standingT2 = Standings.getLCSStandings(match.team2)
                    if (standingT1 is not None and standingT2 is not None):
                        t1standing = ' [#{0} ({1})]'.format(standingT1['standing'], standingT1['record'])
                        t2standing = ' [#{0} ({1})]'.format(standingT2['standing'], standingT2['record'])
            except:
                 t1standing = ''
                 t2standing = ''

            titleFormat = '{3}{0} - {1}{4} vs. {2}{5}'

            title = titleFormat.format(match.gameId, match.team1, match.team2, recommended, t1standing, t2standing)
            item  = { 'label': title,
                      'path': plugin.url_for('show_videos', eventId=eventId, dayId = dayId, gameId = match.gameId),
                      'thumbnail' : day.imageUrl, 'icon' : day.imageUrl
            }
            items.append(item)

    return items

@plugin.route('/loleventvods/event/<eventId>/matches/<dayId>/videos/<gameId>')
@plugin.cached(TTL=10)
def show_videos(eventId, dayId, gameId):
    items = []
    days = Reddit.loadEventContent(eventId)

    day = days[int(dayId)]
    if (day is not None):
        for match in day.matches:
            if (match.gameId == gameId):
                for video in match.videoLinks:
                    if (video is not None):
                        # We can iterate the video links
                        if (video['text'] is not None and video['videoId'] is not None):
                            if (video['videoId'] is not None and video['videoId'] != 'EMPTY'):
                                youtube_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video['videoId']
                            else:
                                youtube_url = ""

                            item  = { 'label': video['text'].replace('&amp;', '&') + " @" + video['time'] + "",
                                      'path': youtube_url,
                                      'is_playable': True}
                            items.append(item)

    return items

if __name__ == '__main__':
    plugin.run()
