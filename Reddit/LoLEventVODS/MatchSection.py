# Line for getting all match info?
#\| (.+) \|(.+)\| vs. \|(.+)\| (.+)\| (.+)\| (.+)\| (.+)
class MatchSection:

    # This is the method that parses all the stuff in the text
    # using the REG_EX
    title = ""
    matches = []

    def __init__(self, descr):
        # Maybe do some formatting here?
        # At least remove the ^ from the string, maybe add dates?
        #formatDescription = str.replace(descr, "^", "")
        self.title = descr

