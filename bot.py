import tweepy, twitter_keys
from annotator_pkg import annotator
from classifier_pkg import classifier
from urllib3.exceptions import ProtocolError
import time
import re


def writeToFile (string):
	with open('tweets analysis.tsv', 'a', encoding = 'utf-8') as outFile:
		outFile.write(string + '\n')


def checkTooSimilar (string, storedMessages):

	tooSimilar = False

	from difflib import SequenceMatcher
	for storedMsg in storedMessages:
		if SequenceMatcher(None, string, storedMsg).ratio() > 0.75:
			tooSimilar = True
			break
	
	return tooSimilar


def analyzeUser (status):

	description = status.user.description
	if description:
		if '\n' in description:
			return False
		descriptionAnnResult = annotator.annotator(description, 'annotator_pkg/lang_data/isSpecialist_nodes.json')
		if descriptionAnnResult:
			descriptionLabel = classifier.classify(description_model, descriptionAnnResult[0])
			if descriptionLabel == 'isSpecialist':
				return True
	return False


def findQueries (queries, string):
	for query in queries:
		if query in string.lower():
			return True
	return False


def analyzeTweet (status, queries, storedMessages):

	message = status.text

	if '\n' in message:
		return False

	if findQueries(queries, message) is False:
		return False
	
	userAnalysis = analyzeUser(status)

	if userAnalysis is True:
		if checkTooSimilar(message.lower(), storedMessages) is True:
			return False
		messageAnnResult = annotator.annotator(message, 'annotator_pkg/lang_data/defeatVirus_nodes.json')
		if messageAnnResult:
			messageLabel = classifier.classify(message_model, messageAnnResult[0])
			if messageLabel == 'defeat':
				storedMessages.append(message)
				writeToFile(status.user.description + '\t' + 'defeat' + '\t' + message)
				return True
			#else:
				# writeToFile(status.user.description + '\t' + 'undefined' + '\t' + message)
	return False

	

class CustomStreamListener(tweepy.StreamListener):

	storedMessages = []

	def on_status(self, status): 
		if status.lang == 'es':
			analysis = analyzeTweet(status, queries, storedMessages)
			api.update_status(status)
			if analysis is True:
				if len(storedMessages) > 100:
					storedMessages.clear()
				try:
					print(status.text)
					#api.retweet(id = status.id)
				except tweepy.TweepError as error:
					print(error)


auth = tweepy.OAuthHandler(twitter_keys.consumer_key, twitter_keys.consumer_secret) 
auth.set_access_token(twitter_keys.access_token, twitter_keys.access_token_secret)
api = tweepy.API(auth) 

queries = ['covid', 'covid-19', 'coronavirus', 'sars-cov-2']

description_model = classifier.loadModel('classifier_pkg/isSpecialist.train.txt')
message_model = classifier.loadModel('classifier_pkg/defeatVirus.train.txt')

storedMessages = []

sapi = tweepy.streaming.Stream(auth, CustomStreamListener()) 

while True:
	try:
		sapi.filter(track = queries)
	except (ProtocolError):
		time.sleep(5)
		continue