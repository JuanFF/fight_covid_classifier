import sys
sys.path.append('../')
import re
import json
from colorama import Back, Fore, init
init()
from simple_term_menu import TerminalMenu


def colorString (string, color):
	
	palette = {
		'red': Fore.RED,
		'green': Fore.GREEN,
		'yellow': Fore.YELLOW,
		'blue': Fore.BLUE,
		'magenta': Fore.MAGENTA,
		'cyan': Fore.CYAN
	}

	return palette[color] + string + Fore.RESET


def colorAnnString(annStringToDisplay):
	return re.sub('(\[)(.+?)(\]_\S+)', Fore.MAGENTA + r'\1' + Fore.RESET + r'\2' + Fore.MAGENTA + r'\3' + Fore.RESET, annStringToDisplay)


def dropdown (key, annSchemeFilePath):
	
	with open(annSchemeFilePath, 'r', encoding = 'utf-8') as annSchemeFile:
		annScheme = json.load(annSchemeFile)

	selection = TerminalMenu([Fore.BLUE + i + Fore.RESET for i in annScheme[key]]).show()

	if annScheme[key][selection] == '<new>':
		newItem = input(colorString(key + ' > ', 'red'))
		print(colorString('+ ' + newItem, 'green'))
		annScheme[key].append(newItem)
		with open(annSchemeFilePath, 'w', encoding = 'utf-8') as annSchemeFile:
			json.dump(annScheme, annSchemeFile, ensure_ascii=False)
		return newItem
	else:
		print(colorString('+ ' + annScheme[key][selection], 'green'))
		return annScheme[key][selection]


def queryForNode (nodeFilePath, annSchemeFilePath):

	inputFrame = dropdown('frame', annSchemeFilePath)
	inputRole = dropdown('role', annSchemeFilePath)
	inputForms = input(colorString('forms > ', 'red'))
	inputForms = inputForms.split(',')
	print(colorString('+ ' + str(inputForms), 'green'))
	# inputContexts = queryWhLoop('context')
	# inputFeatures = queryWhLoop('feature')

	annInput = {
		'frame': inputFrame,
		'role': inputRole,
		'forms': inputForms
		# 'contexts': inputContexts,
		# 'features': inputFeatures
	}

	return annInput


def writeToNodeFile (annInput, targetFilePath):

	with open(targetFilePath, 'r', encoding = 'utf-8') as targetFile:
		fileData = json.load(targetFile)
	
	updateNode = False

	for i in range(len(fileData)):
		if annInput['frame'] == fileData[i]['frame']:
			if annInput['role'] == fileData[i]['role']:
				updateNode = True
				if annInput['forms']:
					for inputForm in annInput['forms']:
						if inputForm not in fileData[i]['forms']:
							fileData[i]['forms'].append(inputForm)

	if updateNode is False:
		annInput['id'] = len(fileData)
		fileData.append(annInput)

	with open(targetFilePath, 'w', encoding = 'utf-8') as targetFile:
		json.dump(fileData, targetFile, ensure_ascii=False)


def queryAndAddTrain (annString, trainFilePath, annSchemeFilePath):
	'''
	FastText format:  __label__positive text
	'''
	
	with open(trainFilePath, 'r', encoding = 'utf-8') as trainFile:
		training = [line.rstrip() for line in trainFile.readlines()]
	
	inputLabel = dropdown('frame', annSchemeFilePath)

	train = '__label__' + inputLabel + ' ' + annString

	if train in training:
		print(colorString('Train dupplicated', 'red'))
	else:
		with open(trainFilePath, 'a', encoding = 'utf-8') as trainFile:
			trainFile.write(train + '\n')
		print(colorString('+ ' + train, 'green'))