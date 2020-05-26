import tweepy, twitter_keys

auth = tweepy.OAuthHandler(twitter_keys.consumer_key, twitter_keys.consumer_secret) 
auth.set_access_token(twitter_keys.access_token, twitter_keys.access_token_secret)
api = tweepy.API(auth)


api.update_status('¡Hola! Hoy es domingo 10 de mayo, del 2020')