import tweepy, twitter_keys
from annotator_pkg import annotator
from classifier_pkg import classifier
from urllib3.exceptions import ProtocolError
import time
import re


def writeFile (status):
	toPrint = ''
	if status.user.verified is True:
		toPrint += status.user.screen_name + '\t' + 'verified' + '\t'
	else:
		toPrint += status.user.description + '\t' + 'not verified' + '\t'
	toPrint += status.text
	print(status.text)
	with open('analysis.tsv', 'a', encoding = 'utf-8') as outFile:
		outFile.write(toPrint + '\n')


def cleanseString (tweetString):
	
	rules = [
		('\s*http.+', ''),
		('\s+vía http.+', ''),
		('^RT @\S+\: ', ''),
		('^\S+ \| ', ''),
		('^\S+\: ', ''),
		('^(@\S+ )+', ''),
		('( @\S+)+$', ''),
		('( #\S+){2,}$', ''),
		('^(#\S+ ){2,}', ''),
		('…$', '')
	]

	for rule in rules:
		tweetString = re.sub(rule[0], rule[1], tweetString)
	
	return tweetString


def analyzeUser (status):

	if status.user.verified is True:
		return True
	
	else:
		description = status.user.description
		if description:
			if '\n' in description:
				return False
			descriptionAnnResult = annotator.annotator(description, 'annotator_pkg/lang_data/isSpecialist_nodes.json')
			if descriptionAnnResult:
				descriptionLabel = classifier.classify(description_model, descriptionAnnResult[0])
				if descriptionLabel == 'isSpecialist':
					return True
				else:
					return False
			else:
				return False
		else:
			return False


def analyzeMessage (status):

	message = status.text

	if '\n' in message:
		return False

	cleansedMsg = cleanseString(message)
	if cleansedMsg.lower() in storedMessages:
		return False

	userAnalysis = analyzeUser(status)

	if userAnalysis is True:
		messageAnnResult = annotator.annotator(message, 'annotator_pkg/lang_data/defeatVirus_nodes.json')
		if messageAnnResult:
			messageLabel = classifier.classify(message_model, messageAnnResult[0])
			if messageLabel == 'defeat':
				storedMessages.append(message)
				return True
			else:
				return False
		else:
			return False
	else:
		return False

	

class CustomStreamListener(tweepy.StreamListener):

	def on_status(self, status): 
		if status.lang == 'es':
			analysis = analyzeMessage(status)
			if analysis is True:
				try:
					writeFile(status)
					# api.retweet(id = status.id)
				except tweepy.TweepError as error:
					print(error)


auth = tweepy.OAuthHandler(twitter_keys.consumer_key, twitter_keys.consumer_secret) 
auth.set_access_token(twitter_keys.access_token, twitter_keys.access_token_secret)
api = tweepy.API(auth) 

queries = ['covid', 'covid-19', 'coronavirus', 'el virus']

description_model = classifier.loadModel('classifier_pkg/isSpecialist.train.txt')
message_model = classifier.loadModel('classifier_pkg/defeatVirus.train.txt')

storedMessages = []

sapi = tweepy.streaming.Stream(auth, CustomStreamListener()) 

while True:
	try:
		sapi.filter(track = queries)
	except (ProtocolError):
		time.sleep(15)
		continue