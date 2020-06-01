import json
import re
import annotator_pkg.ann_helpers
from annotator_pkg.normalization import normalizeTweet


def parseNodesFile (nodeFilePath):

	with open(nodeFilePath, 'r', encoding = 'utf-8') as nodesFile:
		nodes = json.load(nodesFile)
		return nodes


def filterNodes (matchingNodes):

	allowedNodes = []

	filledPos = []

	# sort nodes by string length
	nodes = sorted(matchingNodes, key = lambda x: x['match']['length'], reverse = True)
	
	# add first node
	allowedNodes.append(nodes[0])
	for pos in range(nodes[0]['match']['start'], nodes[0]['match']['end'] + 1):
		filledPos.append(pos)

	# add node if positions are free
	for node in nodes[1:]:
		freePositions = []
		for pos in range(node['match']['start'], node['match']['end'] +1):
			if pos in filledPos:
				freePositions.append('False')
			else:
				freePositions.append(pos)
		if 'False' not in freePositions:
			filledPos += freePositions
			allowedNodes.append(node)

	return allowedNodes


def buildAnnString (source, allowedNodes):

	annString = ''
	annStringToDisplay = ''
	nodes = sorted(allowedNodes, key = lambda x: x['match']['start'])

	lastPos = -1

	for node in nodes:
		annString += source[lastPos+1:node['match']['start']]
		annStringToDisplay += source[lastPos+1:node['match']['start']]
		annString += node['role']
		annStringToDisplay += '[' + source[node['match']['start']:node['match']['end']] + ']_' + node['role']
		lastPos = node['match']['end'] -1
	
	annString += source[lastPos +1:]
	annStringToDisplay += source[lastPos +1:]

	return (annString, annStringToDisplay)
		

def regexMatch (source, regex):

	regexMatch = re.search(regex, source, re.IGNORECASE)
	if regexMatch:
		return (regexMatch.start(), regexMatch.end())
	
	return None


def annotator (source, nodeFilePath):

	source = normalizeTweet(source)
	if source is None:
		return None

	nodes = parseNodesFile(nodeFilePath)

	matchingNodes = []

	for node in nodes:
		match = regexMatch(source, node['form'])
		if match:
			node['match'] = {}
			node['match']['start'] = match[0]
			node['match']['end'] = match[1]
			node['match']['length'] = match[1] - match[0]
			matchingNodes.append(node)

	matchingNodesNumber = len(matchingNodes)

	if matchingNodesNumber == 0:
		return (source, source)

	elif matchingNodesNumber == 1:
		annResult = buildAnnString(source, matchingNodes)
		return annResult

	else:
		allowedNodes = filterNodes(matchingNodes)
		annResult = buildAnnString(source, allowedNodes)
		return annResult