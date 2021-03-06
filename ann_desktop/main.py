import sys
sys.path.append('../')
from os import system
from annotator_pkg import annotator
from ann_desktop import *
from classifier_pkg import classifier
import random

corpusName = input(colorString('\ncorpus file name > ', 'blue'))

corpusPath = 'input/' + corpusName
modelPath = '../classifier_pkg/defeatVirus.train.txt'
vectorPath = None
# vectorPath = '../classifier_pkg/covid.vec'
nodesPath = '../annotator_pkg/lang_data/defeatVirus_nodes.json'
annSchemePath = '../annotator_pkg/lang_data/defeatVirus_ann_scheme.json'


with open(corpusPath, 'r', encoding = 'utf-8') as msgFile:
	messages = [line.rstrip() for line in msgFile.readlines()]
	random.shuffle(messages)

model = classifier.loadModel(modelPath, vectorPath)

for message in messages:

	annResult = annotator.annotator(message, nodesPath)
	if annResult is None:
		continue
	annString = annResult[0]
	annStringToDisplay = annResult[1]
	classifierResult = classifier.classify(model, annString)
	
	if classifierResult == 'undefined':
		print('\n\n' + colorString(classifierResult, 'red') + ' | ' + colorAnnString(annStringToDisplay))
	else:
		print('\n\n' + colorString(classifierResult, 'green') + ' | ' + colorAnnString(annStringToDisplay))

	choice = input(colorString('\n > ', 'blue'))

	while choice == 'n' or choice == 't':

		if choice == 'n':
			print('\n')
			annInputs = queryForNode(nodesPath, annSchemePath)
			writeToNodeFile(annInputs, nodesPath)
			annStringToDisplay = annotator.annotator(message, nodesPath)[1]
			print(colorString('>> ', 'green') + colorAnnString(annStringToDisplay))
			choice = input(colorString('\n > ', 'blue'))

		if choice == 't':
			print('\n')
			annResult = annotator.annotator(message, nodesPath)
			annString = annResult[0]
			annStringToDisplay = annResult[1]
			queryAndAddTrain(annString, modelPath, annSchemePath)
			print('\n')
			model = classifier.loadModel(modelPath, vectorPath)
			classifierResult = classifier.classify(model, annString)
			print('\n\n' + colorString(classifierResult, 'yellow') + ' | ' + colorAnnString(annStringToDisplay))
			choice = input(colorString('\n > ', 'blue'))

	system('clear')