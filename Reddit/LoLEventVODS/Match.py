import re

REG_EX = "##((.*\n)+)---"
REG_EX_DAYS = "##(.*)\n"

class Match:

    # This is the method that parses all the stuff in the text
    # using the REG_EX
    game_start_time = ""
    game_bans_time = ""

    game_start_videoId = ""
    game_bans_videoId = ""

    def __init__(self, inner_text):
        # Parse the string in inner_text
        matches = re.match(REG_EX_DAYS, inner_text, re.M)

