import praw
import json
import requests
import tweepy
import time

access_token = 'YOUR ACCESS TOKEN'
access_token_secret = 'YOUR ACCESS TOKEN SECRET'
consumer_key = 'YOUR CONSUMER KEY'
consumer_secret = 'YOUR CONSUMER SECRET'

google_api_key = "YOUR GOOGLE API KEY"  

subreddit_name = "subredditsimulator"
tag_string= "#Python #reddit #bot"   #Place to put your hastags, etc. Must be <=114 char
num_tweets_before_stopping=20
tweet_delay= 10						#in minutes

def strip_title(title, tag_len):
	char_remaining=140-tag_len-26		# 26 = 24 for link + 2 for the spaces between concatenated strings
	if len(title) <= char_remaining:
		return title
	elif char_remaining >= 3:
		return title[:char_remaining-3] + "..."
	else:
		return ""	

def tweet_creator(subreddit_info):
	post_titles = []
	post_links = []
	post_ids = []
	print "[bot] Getting posts from Reddit"
	for submission in subreddit_info.get_hot(limit=20):
		post_id=submission.id
		post_link=submission.url
		post_title=strip_title(submission.title, len(tag_string))

		post_titles.append(post_title)
		post_links.append(post_link)
		post_ids.append(post_id)

		del post_title, post_link, post_id
	return post_titles, post_links, post_ids

def setup_connection_reddit(subreddit):
	print "[bot] setting up connection with Reddit"
	r = praw.Reddit('yasoob_python reddit twitter bot '
				'monitoring %s' %(subreddit)) 
	subreddit = r.get_subreddit(subreddit)
	return subreddit

def shorten(url):		# Adjusted to include google api key authentication
	try:
		headers = {'content-type': 'application/json'}
		payload = {"longUrl": url}
		googl_url = "https://www.googleapis.com/urlshortener/v1/url?key=%s" %(config_dict['google_api_key'])
		r = requests.post(googl_url, data=json.dumps(payload), headers=headers)
		url = json.loads(r.text)['id']
		print "[bot] Generating short link using goo.gl"
	except:
		print "[bot] improper google api key, defaulting to twitter's t.co shortner"
	return url

def duplicate_check(id):
	found = 0
	with open('posted_posts.txt', 'r') as file:
		for line in file:
			if id in line:
				found = 1
	file.close()			
	return found

def add_id_to_file(id):
	with open('posted_posts.txt', 'a') as file:
		file.write(str(id) + "\n")
	file.close()		

def main():
	count=0
	if len(tag_string) > 114:
		print "[bot] Trailing string of tags is too long, please limit to <100 char"
		return
	while count <= num_tweets_before_stopping:
		subreddit = setup_connection_reddit(subreddit_name)
		post_titles, post_links, post_ids = tweet_creator(subreddit)
		tweeter(post_titles, post_links, post_ids)
		print "[bot] waiting until next tweet"		
		time.sleep(tweet_delay*60)
		count+=1

def tweeter(post_titles, post_links, post_ids):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	index=0
	for post_title, post_link, post_id in zip(post_titles, post_links, post_ids):
		found = duplicate_check(post_id)
		if found == 0:
			tweet_content=post_title+" "+shorten(post_link)+" "+tag_string
			print "[bot] Posting this link on twitter"
			print tweet_content.encode("utf-8")
			try:
				api.update_status(tweet_content)
			except Exception, e:	
				print  "[bot] Error triggered when sending tweet content to twitter:"
				try:
					print "[Twitter] "+ e.args[0][0]['message']
				except:
					print "[bot] Error outside of communication with Twitter"	
				return	
			add_id_to_file(post_id)
			return
		else:
			print "[bot] ID for post #%d already collected" %(index)
			index+=1

if __name__ == '__main__':
	main()