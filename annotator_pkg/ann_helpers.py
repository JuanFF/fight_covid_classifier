import re


def buildRegex (node):

	if len(node['forms']) > 1:
		sortedForms = sorted(node['forms'], key = lambda x: len(x), reverse = True)
		regex = '(' + '|'.join(sortedForms) + ')'
	else:
		regex = node['forms'][0]

	return regex


def regexMatch (source, regex):

	if '|' in regex:
		
		longestRegexChunk = (None, 0)

		regexChunks = regex.split('|')
		regexChunks[0] = regexChunks[0].lstrip('(')
		regexChunks[-1] = regexChunks[-1].rstrip(')')

		for regexChunk in regexChunks:
			regexChunkMatch = re.search(regexChunk, source, re.IGNORECASE)
			if regexChunkMatch:
				if regexChunkMatch.end() - regexChunkMatch.start() > longestRegexChunk[1]:
					longestRegexChunk = (regexChunkMatch, regexChunkMatch.end() - regexChunkMatch.start())
		
		if longestRegexChunk[0] is not None:
			return (longestRegexChunk[0].start(), longestRegexChunk[0].end())

	else:

		regexMatch = re.search(regexMatch, source, re.IGNORECASE)
		if regexMatch:
			return (regexMatch.start(), regexMatch.end())
	
	return None