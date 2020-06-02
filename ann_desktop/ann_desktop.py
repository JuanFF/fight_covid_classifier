import sys
sys.path.append('../')
import re
import json
from colorama import Back, Fore, init
init()

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


def queryForNode (nodeFilePath, annSchemeFilePath):

	with open(annSchemeFilePath, 'r', encoding = 'utf-8') as annSchemeFile:
		annScheme = json.load(annSchemeFile)

	inputFrame = input(colorString('frame > ', 'blue'))
	while inputFrame not in annScheme['frame']:
		print(colorString('! ' + 'Not in annotation schemme', 'red'))
		inputFrame = input(colorString('frame > ', 'blue'))
	print(colorString('+ ' + inputFrame, 'green'))

	inputRole = input(colorString('role > ', 'blue'))
	while inputRole not in annScheme['role']:
		print(colorString('! ' + 'Not in annotation schemme', 'red'))
		inputRole = input(colorString('role > ', 'blue'))
	print(colorString('+ ' + inputRole, 'green'))

	inputForms = input(colorString('form > ', 'blue'))
	inputForms = inputForms.split(',')
	print(colorString('+ ' + str(inputForms), 'green'))

	annInputs = []

	for inputForm in inputForms:
		annInput = {
			'frame': inputFrame,
			'role': inputRole,
			'form': inputForm
		}
		annInputs.append(annInput)

	return annInputs


def writeToNodeFile (annInputs, targetFilePath):

	with open(targetFilePath, 'r', encoding = 'utf-8') as targetFile:
		fileData = json.load(targetFile)
	
	for annInput in annInputs:
		allForms = [node['form'] for node in fileData]
		if annInput['form'] not in allForms:
			fileData.append(annInput)

	with open(targetFilePath, 'w', encoding = 'utf-8') as targetFile:
		json.dump(fileData, targetFile, ensure_ascii=False, indent=4)


def queryAndAddTrain (annString, trainFilePath, annSchemeFilePath):
	'''
	FastText format:  __label__positive text
	'''

	with open(annSchemeFilePath, 'r', encoding = 'utf-8') as annSchemeFile:
		annScheme = json.load(annSchemeFile)

	with open(trainFilePath, 'r', encoding = 'utf-8') as trainFile:
		training = [line.rstrip() for line in trainFile.readlines()]
	
	inputLabel = input(colorString('label > ', 'blue'))
	while inputLabel not in annScheme['frame']:
		print(colorString('! ' + 'Not in annotation schemme', 'red'))
		inputLabel = input(colorString('label > ', 'blue'))


	train = '__label__' + inputLabel + ' ' + annString

	if train in training:
		print(colorString('Train dupplicated', 'red'))
	else:
		with open(trainFilePath, 'a', encoding = 'utf-8') as trainFile:
			trainFile.write(train + '\n')
		print(colorString('+ ' + train, 'green'))