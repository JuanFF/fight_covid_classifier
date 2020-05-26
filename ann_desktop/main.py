import sys
sys.path.append('../')
from annotator_pkg import annotator
from ann_desktop import *
from classifier_pkg import classifier


with open('input/descriptions.txt', 'r', encoding = 'utf-8') as msgFile:
	messages = [line.rstrip() for line in msgFile.readlines()]

model = classifier.loadModel('../classifier_pkg/isSpecialist.train.txt')

for message in messages:

	annResult = annotator.annotator(message, '../annotator_pkg/lang_data/isSpecialist_nodes.json')
	if annResult is None:
		continue
	annString = annResult[0]
	annStringToDisplay = annResult[1]
	classifierResult = classifier.classify(model, annString)
	
	if classifierResult == 'notSpecialist':
		print('\n\n' + colorString(classifierResult, 'blue') + ' | ' + colorAnnString(annStringToDisplay))
	else:
		print('\n\n' + colorString(classifierResult, 'green') + ' | ' + colorAnnString(annStringToDisplay))

	choice = input(colorString('\n > ', 'red'))

	while choice == 'n' or choice == 't':

		if choice == 'n':
			print('\n')
			annInput = queryForNode('../annotator_pkg/lang_data/isSpecialist_nodes.json', '../annotator_pkg/lang_data/isSpecialist_ann_scheme.json')
			writeToNodeFile(annInput, '../annotator_pkg/lang_data/isSpecialist_nodes.json')
			annStringToDisplay = annotator.annotator(message, '../annotator_pkg/lang_data/isSpecialist_nodes.json')[1]
			print(colorString('>> ', 'green') + colorAnnString(annStringToDisplay))
			choice = input(colorString('\n > ', 'red'))

		if choice == 't':
			print('\n')
			annResult = annotator.annotator(message, '../annotator_pkg/lang_data/isSpecialist_nodes.json')
			annString = annResult[0]
			annStringToDisplay = annResult[1]
			queryAndAddTrain(annString, '../classifier_pkg/isSpecialist.train.txt', '../annotator_pkg/lang_data/isSpecialist_ann_scheme.json')
			print('\n')
			model = classifier.loadModel('../classifier_pkg/isSpecialist.train.txt')
			classifierResult = classifier.classify(model, annString)
			print('\n\n' + colorString(classifierResult, 'yellow') + ' | ' + colorAnnString(annStringToDisplay))
			choice = input(colorString('\n > ', 'red'))