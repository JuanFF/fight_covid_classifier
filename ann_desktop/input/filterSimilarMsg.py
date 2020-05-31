from difflib import SequenceMatcher

def getSimilarityScore (firstString, secondString):
	return SequenceMatcher(None, firstString, secondString).ratio()

accumulated = []

with open('tweets-domingo.txt', 'r', encoding = 'utf-8') as inFile:
	count = 0
	for line in inFile:
		line = line.rstrip()
		allowed = True
		count += 1
		print(count)
		for acMessage in accumulated:
			if getSimilarityScore(acMessage, line) >= 0.7:
				allowed = False
		if allowed:
			accumulated.append(line)

with open('filtrados.txt', 'w', encoding = 'utf-8') as outF:
	for acMessage in accumulated:
		outF.write(acMessage + '\n')

