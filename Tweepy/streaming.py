import tweepy, twitter_keys
import sys
sys.path.append('../')
from annotator_pkg import annotator
from classifier_pkg import classifier

auth = tweepy.OAuthHandler(twitter_keys.consumer_key, twitter_keys.consumer_secret) 
auth.set_access_token(twitter_keys.access_token, twitter_keys.access_token_secret)
api = tweepy.API(auth) 


class CustomStreamListener(tweepy.StreamListener): 
	def on_status(self, status): 
		if status.lang == 'es':
			message = status.text
			if '\n' not in message.lower():
				if 'covid' in message.lower() or 'coronavirus' in message.lower():
					annResult = annotator.annotator(message, '../annotator_pkg/lang_data/nodes_defeat_virus.json')
					if annResult:
						label = classifier.classify(model, annResult[0])
						if label == 'defeat':
							print(message)


	def on_error(self, status_code): 
		print('Encountered error with status code:', status_code)
		return True # Don't kill the stream 

	def on_timeout(self): 
		print('Timeout...')
		return True # Don't kill the stream 


queries = ['covid', 'covid-19', 'coronavirus']

model = classifier.loadModel()

sapi = tweepy.streaming.Stream(auth, CustomStreamListener()) 
sapi.filter(track = queries)


# Write from the account

# api.update_status('¡Hola! Hoy es domingo 10 de mayo, del 2020')