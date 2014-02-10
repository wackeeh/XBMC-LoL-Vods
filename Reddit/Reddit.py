from xbmcswift2 import Plugin
import urllib2
import json
import re
import LoLEventVODS.LoLEvent
import LoLEventVODS.Match
import LoLEventVODS.MatchSection
from collections import namedtuple

# CONSTANTS
LOLEVENTURL = "http://www.reddit.com/r/loleventvods/new/.json"
LOLMATCHESURL = "http://www.reddit.com/r/loleventvods/comments/%s/.json"

class Reddit:

    def loadEvents(self):
        req = urllib2.Request(LOLEVENTURL)
        response = urllib2.urlopen(req)

        events = []

        # Now lets parse results
        decoded_data = json.load(response)
        root = decoded_data['data']

        # For Each Item in Children
        for post in root['children']:
            childEvent = LoLEventVODS.LoLEvent.LoLEvent(post)
            events.append(childEvent)

        return events

    def loadEventContent(self, eventId):
        url = LOLMATCHESURL % eventId

        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        # Now lets parse results
        decoded_data = json.load(response)

        selfText = decoded_data[0]['data']['children'][0]['data']['selftext']

        with open('bla.txt', 'w') as f:
            f.write(repr(selfText))
        f.close
        events = []

        # PARSE EVENT MATCHES
        REG_EX = "##((.*/\n*)+?)---"
        # For Each Item in Children
        # Parse the string in inner_text

        matchobj = re.findall(REG_EX, selfText, re.M|re.U)


        return