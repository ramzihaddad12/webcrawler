# Web Crawler
# Approach 

My general approach for this project was that I started off figuring out how to post the login info into the login page. To do so, I needed to obtain the CSRF token before posting the login info. After that, I had to turn my attention on how to parse the HTML obtained from the page, mainly using html.parser, to look for the needed tags (the a-tags to redirect to other Fakebook users' pages) and to look for the secret flags. I had 3 different types of parsers: 
1. FriendParser: to find all the profile links to a user's friends
2. PageNumberParser: to find the number of pages in the friends profile of a Fakebook user so that I add all friends from all the different pages (not just the first) to the queue
3. SecretFlagParser: to find the secret flags in an HTML page if they exist

Finally, I focused my attention on the actual crawling mechanism which involved implementing Breadth First Search (BFS) to crawl Fakebook in search of the 5 needed secret flags and handling the different cases that could occur (connection closing mid-crawl, 301 redirecting, 400 & 500 status codes)

## Challenges faced
The main challenges I faced in this project are as follows: 
1. Getting the CSRF token from the Fakebook login page
2. Posting the correct data to the POST login request based on the name of the input tags of the login page
3. Handling 301, 403, 404, 500 responses from Fakebook
4. Parsing HTML proved to be difficult at first, especially considering BeautifulSoup is not allowed.
5. Handling the occasional scenario I encountered where the server was closing the connection mid-crawl. After debugging, I noticed that server would sometimes send a "Connection: close" message in the header, meaning I had to check for that and reconnect to the server when the connection was closed.
6. Parsing command line args. There seemed to be some confusion on what the command line args for this project 

## Testing Overview 
In order to test that my code and logic are correct, I underwent several iterations of code. During that process, I had many print statements across the code to make sure that the HTML pages were correctly being parsed, and I also had to manually check that I was producing the correct results. Once I was satisfied that my code was behaving in the appropriate way, I had to test for the some of the edge cases (getting 301, 403, 404, 500 responses from Fakebook) , and handle those cases appropriately.
