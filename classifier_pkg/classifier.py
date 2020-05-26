import fasttext
import sys
sys.path.append('../')


def loadModel (trainingFilePath):
	return fasttext.train_supervised(input = trainingFilePath, lr=1.0, epoch=25)


def classify (model, annString):
	label = model.predict(annString)[0][0].split('__')[2]
	return label
	