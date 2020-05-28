import tweepy, twitter_keys
import sys
sys.path.append('../')
from annotator_pkg import annotator
from classifier_pkg import classifier

auth = tweepy.OAuthHandler(twitter_keys.consumer_key, twitter_keys.consumer_secret) 
auth.set_access_token(twitter_keys.access_token, twitter_keys.access_token_secret)
api = tweepy.API(auth) 

outF = open('tweets-jueves.txt', 'w', encoding = 'utf-8')

class CustomStreamListener(tweepy.StreamListener): 
	def on_status(self, status): 
		if status.lang == 'es':
			message = status.text
			description = status.user.description
			if description:
				if '\n' not in description.lower() and '\n' not in message.lower():
					if 'covid' in message.lower() or 'coronavirus' in message.lower():
						description_annResult = annotator.annotator(description, '../annotator_pkg/lang_data/isSpecialist_nodes.json')
						if description_annResult:
							description_label = classifier.classify(description_model, description_annResult[0])
							if description_label == 'isSpecialist':
								message_annResult = annotator.annotator(message, '../annotator_pkg/lang_data/defeatVirus_nodes.json')
								if message_annResult:
									message_label = classifier.classify(message_model, message_annResult[0])
									if message_label == 'defeat':
										outF.write(message_label + '\t' + message + '\n')
										print(message)


	def on_error(self, status_code): 
		print('Encountered error with status code:', status_code)
		return True # Don't kill the stream 

	def on_timeout(self): 
		print('Timeout...')
		return True # Don't kill the stream 


queries = ['covid', 'covid-19', 'coronavirus']

description_model = classifier.loadModel('../classifier_pkg/isSpecialist.train.txt')
message_model = classifier.loadModel('../classifier_pkg/defeatVirus.train.txt')

sapi = tweepy.streaming.Stream(auth, CustomStreamListener()) 
sapi.filter(track = queries)


# Write from the account

# api.update_status('¡Hola! Hoy es domingo 10 de mayo, del 2020')