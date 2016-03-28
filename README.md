Reddit-Twitter Bot
=======

This bot copies posts along with their links from /r/Python (or whatever subreddit of your choosing) and posts them to Twitter. Posts will be reformatted to fit within 140 characters, and post IDs are tracked to prevent duplicate tweets.

Since this bot was first posted to Github, Google and Twitter have both adjusted how links are shortened. This bot has now been updated to address issues caused by this change. Some additional features and customizability were also added, so please feel free to take a second look!

Required libraries
-----------
A few additional libraries are required to run this bot, they can be downloaded through [pip](https://pypi.python.org/pypi/pip):

- PRAW
  * Reddit API wrapper for Python
  * install via pip:  ```pip install praw```
- Tweepy
  * Twitter API wrapper for Python
  * install via pip: ```pip install tweepy```
- Requests
  * Python HTTP library
  * install via pip: ```pip install requests```

Access Tokens and API Keys
-----------
To get started you will need a set of acess codes from Twitter. You can easily get them by going to dev.twitter.com/apps and registering an app. After registering you will have to change the access premissions of your app under the settings tab. After you get your access tokens and everything else just paste them in the fields provided at the beginning of the script .

Google now requires an API key to access its URL shortener tool. To get this access code you will have to register at [this page for URL-Shortener authorization](https://developers.google.com/url-shortener/v1/getting_started#OAuth2Authorizing).

Even if you use Google's link shortening tool, Twitter will still process your link though its t.co's shortener. Twitter does this for all links, even if they fit inside the tweet's 140 characters without shortening. Ultimately it is recommended to default to Twitter's url shortener by setting the google api key variable to "" (a blank string).

Documentation
-----------
I have written a blogpost about how I made this and what everything means. You can read that [here](http://freepythontips.wordpress.com/2013/09/14/making-a-reddit-twitter-bot/)

Recent Changes and New Features
-----------

1. As previously mentioned, this bot now allows for Google developer verification so that the Google URL-Shortener can still be used.

2. The previous method for collecting posts stored them in a dict, and then iterated through that dict. Since dicts are implemented via hash tables, this resulted in posts being sent to twitter out of order to their current reddit ranking. This has been corrected  by saving posts from reddit in lists.

3. You can now specify what hashtags you would like include at the top of the script. The script tracks characters remaining and accommodates space for whatever ending message you decide to use- so long as you don't go past a character limit of 114. It's best to keep your ending messages or hastages short so you don't crowd out content from reddit.

4. An issue with how the script checked for duplicate posts, which could have lead to false positives, was corrected. Previously if the id of a collected post was within the longer id of a new post, it would have been flagged as a duplicate.

5. Some smaller error checking features were added, and an issue where the script would be unable to convert certain unicode characters to ascii  was corrected (achieved by encoding to unicode).



