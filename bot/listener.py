import sys
sys.path.append('../')
import tweepy, twitter_keys
from annotator_pkg import annotator
from classifier_pkg import classifier
import time
import re


queries = ['covid', 'covid-19', 'coronavirus', 'sars-cov-2']
queueFilePath = 'queue.txt'


def writeLogFile (label, status):
	
	if status.user.verified:
		twitterVerified = 'twitter_verified'
	else:
		twitterVerified = 'not_twitter_verified'

	if status.user.description:
		description = status.user.description
		description = description.replace('\n', ' ')
	else:
		description = 'no_description'

	with open('log.tsv', 'a', encoding = 'utf-8') as logFile:
		logFile.write(label + '\t' + status.text + '\t' + twitterVerified + '\t' + description + '\n')

		
def checkTooSimilar (inputString, queueFilePath):

	def cleanseString (string):
		string = re.sub('\s*http.+', '', string)
		string = re.sub('\s+vía http.+', '', string)
		string = re.sub('^RT @\S+\: ', '', string)
		string = string.lower()
		return string

	tooSimilar = False

	inputString = cleanseString(inputString)

	with open(queueFilePath, 'r', encoding = 'utf-8') as queueFile:
		queue = [line.split('\t', 2)[2].rstrip().lower() for line in queueFile.readlines()]

	from difflib import SequenceMatcher
	for message in queue:
		message = cleanseString(message)
		if SequenceMatcher(None, inputString, message).ratio() > 0.75:
			tooSimilar = True
			break
	
	return tooSimilar


def analyzeUser (status):

	# user is valid if account is 'Twitter verified'
	if status.user.verified == True:
		return True

	else:
	# must have 'description'
		description = status.user.description
		if description:

			# classifier doesn't work with '\n'
			if '\n' in description:
				return False
			
			# string must be long enough to be annotated
			descriptionAnnResult = annotator.annotator(description, '../annotator_pkg/lang_data/isSpecialist_nodes.json')
			if descriptionAnnResult:

				# classifier's label must be 'isSpecialist'
				label = classifier.classify(description_model, descriptionAnnResult[0])
				if label == 'isSpecialist':
					return True

		return False


def findQueries (queries, string):

	for query in queries:
		if query in string.lower():
			return True

	return False


def analyzeTweet (status, queries, queueFilePath):

	message = status.text

	# classifier doesn't work with '\n'
	if '\n' in message:
		return False

	# message must have queries
	if findQueries(queries, message) is False:
		return False
	
	# user must be Twitter verified or categorized as 'isSpecialist' (=True)
	userAnalysis = analyzeUser(status)
	if userAnalysis is True:

		# message must be less than 0.75 similar to queue's messages
		if checkTooSimilar(message, queueFilePath):
			return False

		# string must be long enough to be annotated
		messageAnnResult = annotator.annotator(message, '../annotator_pkg/lang_data/defeatVirus_nodes.json')
		if messageAnnResult:
			
			# write analysis to log file
			label = classifier.classify(message_model, messageAnnResult[0])
			writeLogFile(label, status)

			# classifier's label must be 'defeat'
			if label == 'defeat':
				print(message)
				return True

	return False


class CustomStreamListener(tweepy.StreamListener):

	def on_status(self, status):
		if status.lang == 'es':
			with open('queue.txt', 'a', encoding = 'utf-8') as queueFile:
				analysis = analyzeTweet(status, queries, queueFilePath)
				if analysis is True:
					queueFile.write(status.id_str + '\t' + status.user.screen_name + '\t' + status.text + '\n')

	
auth = tweepy.OAuthHandler(twitter_keys.consumer_key, twitter_keys.consumer_secret) 
auth.set_access_token(twitter_keys.access_token, twitter_keys.access_token_secret)
api = tweepy.API(auth) 


description_model = classifier.loadModel('../classifier_pkg/isSpecialist.train.txt', None)
message_model = classifier.loadModel('../classifier_pkg/defeatVirus.train.txt', '../classifier_pkg/covid.vec')


while True:
	# sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
	# sapi.filter(track = queries)

	try:
		print('\n' + 'Bot listening...')
		sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
		sapi.filter(track = queries)
	except:
		print('\n' + 'Pause in error...')
		time.sleep(25)
		continue