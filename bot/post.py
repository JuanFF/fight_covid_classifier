import tweepy, twitter_keys
import time


auth = tweepy.OAuthHandler(twitter_keys.consumer_key, twitter_keys.consumer_secret) 
auth.set_access_token(twitter_keys.access_token, twitter_keys.access_token_secret)
api = tweepy.API(auth) 


print('Bot publishing...')


while True:

	with open('posted_ids.txt', 'r', encoding = 'utf-8') as postedIdsFile:
		postedIds = [line.rstrip() for line in postedIdsFile]

	with open('queue.txt', 'r', encoding = 'utf-8') as queueFile:
		queue = [line.rstrip() for line in queueFile.readlines()]

	count = 0
	for tweet in queue:
		count += 1
		tweetId = tweet.split('\t', 2)[0]
		if tweetId not in postedIds:
			message = tweet.split('\t', 2)[2]
			try:
				api.retweet(int(tweetId))
				with open('posted_ids.txt', 'a', encoding = 'utf-8') as postedIdsFile:
					postedIdsFile.write(tweetId + '\n')
				print('\n[' + str(len(queue) - count) + ' left] ' + message)
				break
			except:
				continue
	
	time.sleep(900)