import urllib2
import htmllib
import json
import time
import re
from collections import namedtuple
from operator import attrgetter

from BeautifulSoup import BeautifulSoup



# CONSTANTS
LOLEVENTURL = "http://www.reddit.com/r/loleventvods/new/.json"
LOLMATCHESURL = "http://www.reddit.com/r/loleventvods/comments/%s/.json"
ACTIVE_STRING = "In progress"
FINISHED_STRING = "Finished"
NOTSTREAMED_STRING = "**Not Streamed**"

class Reddit:


    def loadEvents(self, sortByStatus):
        req = urllib2.Request(LOLEVENTURL)
        response = None
        try:
            response = urllib2.urlopen(req)
        except:
            time.sleep(3)
            try:
                response = urllib2.urlopen(req)
            except:
                return None

        events = []

        # Now lets parse results
        decoded_data = json.load(response)
        root = decoded_data['data']

        LoLEvent = namedtuple('LoLEvent', 'title status eventId imageUrl')

        # For Each Item in Children
        for post in root['children']:
            html = post['data']['selftext_html']
            if (html is not None):
                soup = BeautifulSoup(self.unescape(html))

                imgUrl = ''
                link = soup.find('a', 'href=#EVENT_PICTURE')
                if (link is not None):
                    imgUrl = link.title

            status = 99
            if (post['data']['link_flair_text']== ACTIVE_STRING):
                status = 0

            if (post['data']['link_flair_text']== FINISHED_STRING):
                status = 1

            childEvent = LoLEvent(title = post['data']['title'],
                                  status = status,
                                  eventId = post['data']['id'],
                                  imageUrl = imgUrl)

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
        response = None
        try:
            response = urllib2.urlopen(req)
        except:
            time.sleep(3)
            try:
                response = urllib2.urlopen(req)
            except:
                return None
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
                     if (col.text.lower() == "youtube"):
                         YouTubeColumns.append(i)
                     if (col.text.lower() == "team 1"):
                         Team1Index = i
                     if (col.text.lower() == "team 2"):
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
                                    youTubeData = self.parseYouTubeUrl(cols[yv].a['href'])
                                    videos.append({'text' : cols[yv].a.text,
                                                   'videoId' : youTubeData['videoId'],
                                                   'time' : youTubeData['time'] })

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

    def parseYouTubeUrl(self, url):
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

        return {'videoId' : youtube_id,
                 'time' : youtube_Time}