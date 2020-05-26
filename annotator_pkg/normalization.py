import re


cleanseRules = [

	# http
	('\s*http.+', ''),
	
	# vía http
	('\s+vía http.+', ''),

	# retweets
	('^RT @\S+\: ', ''),

	# @elmundo
	('^(@\S+ )+', ''),

	# es así @elmundo @elpais @marca
	('( @\S+)+$', ''),

	# #Noticias | Hallan...
	('^\S+ \| ', ''),

	# estas son las claves #noticias #última_hora
	('( #\S+){2,}$', ''),

	# #noticias #última_hora estas son las claves
	('^(#\S+ ){2,}', ''),

	# estas son las #noticias de hoy
	('#(\S+) ', r'\1 '),

	# double space
	('\s{2,}', ' '),

	# ...
	('…$', '')

]


tokenizerRules = [

	# symbol next to the right
	('(\w{2,})(\,|\.|\?|\!|\:|\;)', r'\1' + ' ' + r'\2'),

	# symbol next to the left
	( '(\¡|\¿)(\w{2,})', r'\1' + ' ' + r'\2'),

	# () ""
	(' (\(|\"|\'|\“)(\w)', r' \2'),
	('(\w)(\)|\"|\'|\”) ', r'\1 ')

]


def normalizeTweet (tweetString):

	for cleaseRule in cleanseRules:
		tweetString = re.sub(cleaseRule[0], cleaseRule[1], tweetString)

	if len(tweetString.split()) < 5:
		return None

	for tokenizerRule in tokenizerRules:
		tweetString = re.sub(tokenizerRule[0], tokenizerRule[1], tweetString)

	tweetString = tweetString.strip()

	tweetString = tweetString.lower()

	return tweetString


# test
# print(
# 	normalizeTweet ('@LuisfePu239 @velardedaoiz2 Hay que aprender a convivir con el virus, porque éste no se va ir hasta que podamos ten…')
# )