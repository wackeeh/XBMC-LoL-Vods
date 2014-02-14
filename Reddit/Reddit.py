from xbmcswift2 import Plugin
import urllib2
import htmllib
import json
from collections import namedtuple
from BeautifulSoup import BeautifulSoup
from operator import attrgetter

# CONSTANTS
LOLEVENTURL = "http://www.reddit.com/r/loleventvods/new/.json"
LOLMATCHESURL = "http://www.reddit.com/r/loleventvods/comments/%s/.json"
ACTIVE_STRING = "In progress"
FINISHED_STRING = "Finished"
NOTSTREAMED_STRING = "**Not Streamed**"

class Reddit:


    def loadEvents(self, sortByStatus):
        req = urllib2.Request(LOLEVENTURL)
        response = urllib2.urlopen(req)

        events = []

        # Now lets parse results
        decoded_data = json.load(response)
        root = decoded_data['data']

        LoLEvent = namedtuple('LoLEvent', 'title status eventId')

        # For Each Item in Children
        for post in root['children']:

            status = 99
            if (post['data']['link_flair_text']== ACTIVE_STRING):
                status = 0

            if (post['data']['link_flair_text']== FINISHED_STRING):
                status = 1

            childEvent = LoLEvent(title = post['data']['title'],
                                  status = status,
                                  eventId = post['data']['id'])

            events.append(childEvent)


        if (sortByStatus):
            # sort
            return sorted(events, key=attrgetter('status'))
        else:
            return events

    def loadEventContent(self, eventId):

        LoLEventDay = namedtuple('LoLEventDay', 'dayId day matches')
        LoLEventMatch = namedtuple('LoLEventMatch', 'gameId team1 team2 videoLinks')

        url = LOLMATCHESURL % eventId

        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        # Now lets parse results
        decoded_data = json.load(response)

        selfText = decoded_data[0]['data']['children'][0]['data']['selftext_html']

        eventTitle = ''
        days = []

        soup = BeautifulSoup(self.unescape(selfText))

        # find all tables
        tables = soup.findAll("table")
        for idx, table in enumerate(tables):
            if (table is not None):

                titleLink = table.find("a", href="http://www.table_title.com")
                if (titleLink is not None):
                    eventTitle = titleLink['title']

                YouTubeColumns = []
                Team1Index = -1
                Team2Index = -1

                # Investigate the right columns for youtube links
                rows = table.find("thead").findAll("tr")
                for row in rows :
                    cols = row.findAll("th")
                    for i, col in enumerate(cols):
                     if (col.text == "YouTube"):
                         YouTubeColumns.append(i)
                     if (col.text == "Team 1"):
                         Team1Index = i
                     if (col.text == "Team 2"):
                         Team2Index = i

                #
                matches=[]

                rows = table.find("tbody").findAll("tr")
                for row in rows :
                    videos = []
                    cols = row.findAll("td")
                    if (cols is not None):
                        for yv in YouTubeColumns:
                            if (cols[yv] is not None):
                                if (cols[yv].a is not None):
                                    videos.append({'text' : cols[yv].a.text, 'link' : cols[yv].a['href']})

                    matches.append(LoLEventMatch(cols[0].text, cols[Team1Index].text, cols[Team2Index].text, videos))

                # for row in table_data:
                #     for i, col in enumerate(row):

                            # for YouTubeCol in YouTubeColumns:
                            # print cols[YouTubeCol-1]

                days.append(LoLEventDay(dayId = idx,
                                    day=eventTitle,
                                    matches = matches))
        return days

    def unescape(self, s):
        p = htmllib.HTMLParser(None)
        p.save_bgn()
        p.feed(s)
        return p.save_end()
