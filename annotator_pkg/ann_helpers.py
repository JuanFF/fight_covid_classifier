import re


def buildRegex (node):

	if len(node['forms']) > 1:
		sortedForms = sorted(node['forms'], key = lambda x: len(x), reverse = True)
		regex = '(' + '|'.join(sortedForms) + ')'
	else:
		regex = node['forms'][0]

	return regex


def regexMatch (source, regex):
	
	regexMatch = re.search(regex, source, re.IGNORECASE)

	if regexMatch:
		return (regexMatch.start(), regexMatch.end())
	
	return None