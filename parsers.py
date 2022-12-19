from html.parser import HTMLParser
import re

# parser to find the secret flags in an HTML page if they exist
class SecretFlagParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.secret_flags = [] # secret flags list 
        self.capture = False
    
    # handle the start tag of an HTML element
    def handle_starttag(self, tag, attrs):
        # we only care if the tag is <h2> since secret flags are only in <h2> tags
        if tag in ('h2'): 
            if len(attrs) == 2: 
                name, value = attrs[0]
                # if the class = "secret_flag" in a h2 tag then the data contains a secret flag that needs to be captured 
                if name == "class" and value == "secret_flag":
                    self.capture = True

    # handle the end tag of an HTML element
    def handle_endtag(self, tag):
        if tag in ('h2'):
            self.capture = False

    # handle/process data from tag 
    def handle_data(self, data):
        # if data needs to be captured 
        if self.capture:
            if "FLAG: " in data: 
                # remove the "FLAG: " portion of the data 
                SECRET_FLAG = data[data.index(':') + 2: ]
                # add the secret flag to the list of secret flags 
                self.secret_flags.append(SECRET_FLAG)
                # print the secret flag 
                print(SECRET_FLAG)
                

# parser to find all the profile links to a user's friends
class FriendParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.friends_links = [] # list of the extracted friends links

    # handle the start tag of an HTML element
    def handle_starttag(self, tag, attrs):
        # we only care if the tag is <a> since links to other user profiles are in <a> tags
        if tag in ('a'): 
            for name, value in attrs:
            # if name of the tag is href, then there is a user profile to be extracted/parsed 
                if name == "href":
                    # no need for the main page ("/") or the /friends page of the current page or the logout page
                    if "/friends/" not in value and "/accounts/logout" not in value and len(value) > 1:
                         self.friends_links.append(value)

# parser to find the number of friends pages in the friends profile of a Fakebook user
class PageNumberParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.data = []
        self.num_of_pages = -1

    # handle the start tag of an HTML element
    def handle_starttag(self, tag, attrs):
        # we only care if the tag is <p> since  the info about the number of pages is in <p> tags
        if tag in ('p'): 
            self.capture = True

    # handle the end tag of an HTML element
    def handle_endtag(self, tag):
        if tag in ('p'):
            self.capture = False

    # handle/process data from tag 
    def handle_data(self, data):
        # if data needs to be captured 
        if self.capture:
            # knowing that the first extracted <p> tag will contain the total number of pages information, we only need the first captured data 
            if (len(self.data) < 1):
                self.data.append(data)
                # parse "page {?} of {num_of_pages}"" so that we only get num_of_pages
                result = re.search('of(.*)\n', data)
                if result == None: 
                    self.num_of_pages = "0"
                else:
                    self.num_of_pages = (result.group(1))