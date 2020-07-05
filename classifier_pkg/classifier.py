import fasttext
import sys
sys.path.append('../')


def loadModel (trainingFilePath, vectorFilePath):
	if vectorFilePath:
		return fasttext.train_supervised(input = trainingFilePath, lr=1.0, epoch=25, pretrainedVectors = vectorFilePath)
	else:
		return fasttext.train_supervised(input = trainingFilePath, lr=1.0, epoch=25)		


def classify (model, annString):
	label = model.predict(annString)[0][0].split('__')[2]
	return label