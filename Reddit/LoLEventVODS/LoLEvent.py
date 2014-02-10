import re
import MatchSection

REG_EX = "##((.*\n*)+?)---"
REG_EX_LINES = "(.+)\n"
ACTIVE_STRING = "In progress"
FINISHED_STRING = "Finished"
NOTSTREAMED_STRING = "**Not Streamed**"

class LoLEvent:
    # Reddit LoL Event Holder
    # Contains a bunch of variables

    title = ""
    status = ""
    eventId = ""
    isEvent = False
    matchSections = []

    def __init__(self, json_data):

        # process the results
        root = json_data['data']

        # second tag we should get is the title
        self.title = root['title']
        self.status = root['link_flair_text']
        self.eventId = root['id']

        if (self.status == ACTIVE_STRING or self.status == FINISHED_STRING ):
            self.isEvent = True

    def displayTitle(self):
        return self.title + " (" + self.status +")"

    def __eq__(self, other):
        return self.eventId == other.eventId

    def parseText(self, text):

        matchDays = []

        # Parse the string in inner_text
        matchobj = re.findall(REG_EX, text, re.M)

        with open('bla.txt', 'w') as f:
            f.write(repr(matchobj))
        f.close

        with open('bla2.txt', 'w') as f:

            for g in matchobj:
                # The grouped string
                for s in g[0].splitlines():
                    s.strip()
                    #f.write(s)

                    matchDay = MatchSection.MatchSection(s)
                    matchDays.append(matchDay)

     #           if (not g.__contains__(NOTSTREAMED_STRING)):
                    # We got the entire string, including matches



                    # Match mapping


            return matchDays

        f.close


